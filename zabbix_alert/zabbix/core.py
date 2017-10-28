#_coding:utf-8_*_
# import django
# import os
# import time
# from Free import settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Free.settings")
# django.setup()
from api.SaltStackApi.salt_pycurl_https import SaltApi
from api.Zabbix.api import ZabbixApi
from zabbix.models import Hosts, Graphs, Groups, Templates, Triggers, Items, Proxy
from api.models import SaltInfo
import time


class Zabbix(object):
    def __init__(self):

        self.api = ZabbixApi(url='http://127.0.0.1:8001', username='xiaosong', password='qaz199539')

    def update_group(self):

        '''更新主机组入库'''

        groupall = self.api.select_groups_all()
        for group in groupall:
            print group
            groupsql = Groups.objects.filter(groupid=group['groupid'])
            if groupsql:
                '''(groupid=group['groupid'], name=group['name'],flags=group['flags'],internal=group['internal'])'''
                groupsql.update(**group)
            else:
                obj = Groups.objects.create(**group)
                obj.save()

    def update_proxy(self):

        '''更新代理入库'''
        try:
            zero = Proxy.objects.get(proxyid=0, host=0, name=0)
        except:
            zero = Proxy.objects.create(proxyid=0, host=0, name=0)
            zero.save()
        proxyall = self.api.select_proxy_all()
        for proxy in proxyall:
            print proxy['proxyid']
            proxysql = Proxy.objects.filter(proxyid=proxy['proxyid'])
            if proxysql:
                proxysql.update(proxyid=proxy['proxyid'], host=proxy['host'], name=proxy['name'])
            else:
                obj = Proxy.objects.create(proxyid=proxy['proxyid'], host=proxy['host'], name=proxy['name'])
                obj.save()

    def update_template(self):

        '''更新模版入库'''

        templateall = self.api.select_template_all()
        for template in templateall:
            print template['templateid']
            templatesql = Templates.objects.filter(templateid=template['templateid'])
            if templatesql:
                templatesql.update(templateid=template['templateid'],
                                   host=template['host'],
                                   name=template['name'])
            else:
                obj = Templates.objects.create(templateid=template['templateid'],
                                               host=template['host'],
                                               name=template['name'])
                obj.save()

    def updatehost(self):
        hostall = self.api.select_host_list_detail()
        for host in hostall:
            try:
                hostdic = {
                           "hostid":host['hostid'],
                           "host":host['host'],
                           "name":host['name'],
                           "proxyid_id":host['proxy_hostid'],
                           "flags":host['flags'],
                           "status":host['status'],
                           "interfaces":host['interfaces'][0]['ip'],
                           "groupid_id":host['groups'][0]['groupid'],
                           "templateid_id":host['parentTemplates'][0]['templateid']
                           if len(host['parentTemplates']) else None,
                           "templatenum":len(host['parentTemplates']),
                           "itemsnum":len(host['items']),
                           "triggernum":len(host['triggers']),
                           "graphsnum":len(host['graphs']),
                           "screensid":len(host['screens']),
                           "applicationsnum":len(host['applications'])
                            }
                print hostdic
                hostsql = Hosts.objects.filter(hostid=host['hostid'])
                if hostsql:
                    hostsql.update(**hostdic)
                else:
                    try:
                        obj = Hosts.objects.create(**hostdic)
                        obj.save()
                    except Exception as  e:
                        print 'error', e
                        return e
            except Exception as  e:
                print 'error',e
                return e

    def updateitem(self):

        '''更新监控项入库暂不使用'''

        itemall = self.api.select_item_all()
        for item in itemall:
            try:
                itemsql = Items.objects.filter(itemid=item['itemid'])
                if itemsql:
                    itemsql.update(itemid=item['itemid'],
                                               key=item['key_'],
                                               type=item['type'],
                                               delay=item['delay'],
                                               history=item['history'],
                                               trends=item['trends'],
                                               hostid_id=item['hostid'],
                                               lastclock=item['lastclock'],
                                               status=item['status'],
                                               name=item['name'],
                                               data_type=item['data_type'],)
                else:
                    obj = Items.objects.create(itemid=item['itemid'],
                                               key=item['key_'],
                                               type=item['type'],
                                               delay=item['delay'],
                                               history=item['history'],
                                               trends=item['trends'],
                                               hostid_id=item['hostid'],
                                               lastclock=item['lastclock'],
                                               status=item['status'],
                                               name=item['name'],
                                               data_type=item['data_type'],
                                               )
                    obj.save()
            except:
                return 'error'


    def update_graph(self):

        '''更新grpah入库'''

        graph = self.api.select_graph_all(hostid='10105')
        for i in graph:
            print i['name']
            print i['graphid']
        pass

    def update_trigger(self):

        '''更新触发器入库'''

        pass
        # for i in trigger:
        #     print i['status']
        #     print i['description']
        #     print i['templateid']
        #     print i['triggerid']
        #     print i['comments']
        #     print i['expression']

    def updateuser(self):
        pass

    def createhost(self, host, ip, groupid, templateid, proxyid):
        try:
            name = Groups.objects.get(groupid=groupid).name
        except:
            name = ''
        if '_' in host:
            name = host.replace(host.split('_')[0],name)
        else:
            name = name + host

        res = self.api.create_host(host=host,
                                   groupid=groupid,
                                   templateid=templateid,
                                   iplist=ip,
                                   name=name,
                                   proxy_hostid=proxyid)
        if res:
            #可以创建完主机先入本地库 功能未写
            return "主机%s创建成功，ID为%s."%(host,res['hostids'])
        else:
            return "主机%s创建失败"%host

    def creategroup(self, groupname):

        group = Groups.objects.filter(name=groupname)
        if group:
            return "主机组%s创建失败"%groupname
        else:
            res = self.api.create_group(groupname=groupname)
            if res:
                obj = Groups.objects.create(name=groupname,groupid=res['groupids'][0])
                obj.save()
                return "主机组%s创建成功，ID为%s." % (groupname, res['groupids'][0])
            else:
                return "主机组%s创建失败"%groupname

    def select_item(self,hostid):
        itemlist = self.api.select_item_all(hostid=hostid)
        for item in itemlist:
            item['lastclock'] = time.strftime('%Y/%m/%d %H:%M', time.localtime(float(item['lastclock'])))
        return itemlist

    def select_graph(self,hostid):
        graph = self.api.select_graph_all(hostid=hostid)
        return graph

    def select_history(self,itemid,data_type):
        value = []
        clock = []
        item = self.api.select_item_all(itemid=itemid)[0]
        host = self.api.select_host_list_detail(hostid=item['hostid'])[0]
        historylist = self.api.select_history_all(itemid,int(data_type))
        for history in historylist:
            value.append(float(history['value']))
            clock.append(time.strftime('%Y/%m/%d %H:%M', time.localtime(float(history['clock']))))
        return value,clock,item,host