#-*-coding:utf-8-*-
try: import httplib
except ImportError:
    import http.client as httplib

from django.forms.models import model_to_dict
import sys
import urllib
import urllib2
import time
import random
import json
import itertools
import mimetypes
import base64
import hmac
import uuid
import traceback
from hashlib import sha1
from models import ServersModel, RdsModel
import datetime
import logging
from utils import send_alarm, send_mail
from Free.settings import ALIYUN_KEY, ALIYUN_SECRET

logger = logging.getLogger("free")

class AliyunMonitor:
    '''调用阿里云服务器的公共类'''

    def __init__(self, url, access_id, access_secret, version='2014-05-26', time_stamp="TimeStamp"):
        self.time_stamp = time_stamp
        self.access_id = access_id
        self.access_secret = access_secret
        self.url = url
        self.version = version
    ##签名
    def sign(self,accessKeySecret, parameters):
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''
        for (k,v) in sortedParameters:
            canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)

        stringToSign = 'GET&%2F&' + self.percent_encode(canonicalizedQueryString[1:]) #使用get请求方法

        h = hmac.new(accessKeySecret + "&", stringToSign, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature

    def percent_encode(self,encodeStr):
        encodeStr = str(encodeStr)
        res = urllib.quote(encodeStr.decode('UTF-8').encode('utf8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    def make_url(self,params):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        parameters = {
            'Format' : 'JSON',
            'Version' : self.version,
            'AccessKeyId' : self.access_id,
            'SignatureVersion' : '1.0',
            'SignatureMethod' : 'HMAC-SHA1',
            'SignatureNonce' : str(uuid.uuid1()),
            self.time_stamp : timestamp,
        }
        for key in params.keys():
            parameters[key] = params[key]

        signature = self.sign(self.access_secret,parameters)
        parameters['Signature'] = signature
        url = self.url + "/?" + urllib.urlencode(parameters)
        return url

    def do_request(self,params):
        url = self.make_url(params)
        request = urllib2.Request(url)
        try:
            conn = urllib2.urlopen(request)
            response = conn.read()
        except urllib2.HTTPError, e:
            return e.read().strip()
        try:
            obj = json.loads(response)
        except ValueError, e:
            return SystemExit(e)
        return obj


def get_one_instance_info(instanceid):
    try:
        T = AliyunMonitor("https://ecs.aliyuncs.com", ALIYUN_KEY, ALIYUN_SECRET)
        instanceid = str(instanceid.strip(' '))
        data = {"RegionId":'cn-hangzhou',"Action":"DescribeInstances","InstanceIds": [instanceid, ]}
        server = T.do_request(data)
        return server
    except Exception as e:
        logger.error("get one instance error: " + traceback.format_exc())

#通过api获取所有得服务器信息，然后处理成字典的形式
def get_ecs_status_list(action,instanceId="",regionId="cn-hangzhou", pageNumber=1, pageSize=99, startTime="2016-06-13T15:00Z", endTime="2016-11-22T15:00Z"):
    T = AliyunMonitor("https://ecs.aliyuncs.com", ALIYUN_KEY, ALIYUN_SECRET)
    result = T.do_request({"RegionId":regionId,"Action":action,"InstanceId":instanceId,"PageNumber":str(pageNumber),"PageSize":str(pageSize),
                            "StartTime":str(startTime),"EndTime":endTime})

    final = {}
    for key, item in result.items():
        if isinstance(item ,dict):
            for ins_key, ins_item in item.items():
                if isinstance(ins_item, list) and ins_key == 'Instance':
                    num = 0
                    for one in ins_item:
                        num += 1
                        final.update({num: {}})
                        for n_key, n_item in one.items():
                            if isinstance(n_item, dict):
                                for m_key, m_item in n_item.items():
                                    if isinstance(m_item, dict):
                                        for f_key, f_item in m_item.items():
                                            if isinstance(f_item, list):
                                                f_item = ','.join(f_item)
                                            final[num].update({n_key + '_' + m_key + '_' + f_key: f_item})
                                    else:
                                        if m_item and isinstance(m_item, list) and isinstance(m_item[0], unicode):
                                            m_item = ','.join(m_item)
                                        final[num].update({n_key + '_' + m_key: m_item})
                            else:
                                if isinstance(n_item, list):
                                    n_item = ','.n_item
                                final[num].update({n_key: n_item})
        else:
            pass
            #final.update({key: item})
    return final

#查询阿里云的信息，更新到数据库
def deal_server():
    results = []
    pay_type = {'PrePaid': '包年包月', 'PostPaid': '按量付费'}
    zone_name = {"cn-beijing-a": "华北 2 可用区 A", "cn-beijing-c": "华北 2 可用区 C", "cn-beijing-b": "华北 2 可用区 B", "cn-hongkong-b": "香港可用区B", "cn-hongkong-c": "香港可用区C",
                 "cn-hongkong-a": "香港可用区A", "cn-qingdao-b": "华北 1 可用区 B", "cn-qingdao-a": "华北 1 可用区 A", "cn-shenzhen-a": "华南 1 可用区 A",
                 "cn-shenzhen-b": "华南 1 可用区 B", "ap-southeast-1a": "新加坡可用区 A", "ap-southeast-1b": "新加坡可用区 B", "cn-hangzhou-d": "华东 1 可用区 D",
                 "cn-hangzhou-e": "华东 1 可用区 E", "us-east-1a": "美东 1 可用区 A", "cn-hangzhou-a": "华东 1 可用区 A", "cn-hangzhou-b": "华东 1 可用区 B",
                 "cn-hangzhou-c": "华东 1 可用区 C", "cn-shanghai-a": "华东 2 可用区 A", "cn-shanghai-c": "华东 2 可用区 C", "cn-shanghai-b": "华东 2 可用区 B",
                 "us-west-1a": "美西 1 可用区 A", "us-west-1b": "美西 1 可用区 B"}
    chargetype_bandwith = {'PayByBandwidth': '按固定带宽', 'PayByTraffic': '按流量付费', "[]": "[]", "": ""}
    endTime = time.strftime("%Y-%m-%d") + "T15:00Z"
    try:
        for region in ("cn-beijing", "cn-qingdao", "cn-hangzhou", "cn-shenzhen", "cn-shanghai", "cn-hongkong"):
            for num in range(1,15):
                result = get_ecs_status_list("DescribeInstances", pageNumber=num, regionId=region, endTime=endTime)
                results = results + result.values()
    except Exception, e:
        logger.error('查询阿里云服务器信息失败: ' + traceback.format_exc())

    #更新服务器信息详情
    many_keys = []
    for one in results:
        many_keys.append(one["InstanceId"])
        change_item = {"ZoneId": zone_name, "InstanceChargeType": pay_type, "InternetChargeType": chargetype_bandwith}
        for key, value in change_item.items():
            if key in one.keys():
                try:
                    one[key] = value[one[key]]
                except Exception as e:
                    pass
                
                
        for key in ('CreationTime', 'ExpiredTime'):
            atime = one[key]
            atime = atime.split('T')
            atime = atime[0].split('-')

            d1 = datetime.datetime(int(atime[0]), int(atime[1]), int(atime[2]))
            d3 = d1 + datetime.timedelta(days=1)
            one[key] = d3.strftime('%Y-%m-%d') + ' 00:00'
            if key == 'ExpiredTime':
                if 0 <= (d3 - datetime.datetime.now()).days < 15:
                    date_color = 'red'
                elif (d3 - datetime.datetime.now()).days < 0:
                    one["Status"] = 'Stopped'
                    date_color = 'black'
                else:
                    date_color = 'green'
        server = ServersModel.objects.filter(instanceid=one["InstanceId"])
        if server:
            server.update(server_from="aliyun", vpc_vpcid = one["VpcAttributes_VpcId"], host_name = one["HostName"], instance_family = one["InstanceTypeFamily"],
                    create_time = one["CreationTime"], expired_time = one["ExpiredTime"], io_optimized = one["IoOptimized"], instance_type = one["InstanceType"],
                    eip_intercharge_type = one["EipAddress_InternetChargeType"], internet_charge_type = one["InternetChargeType"], image_id = one["ImageId"],
                    instance_name = one["InstanceName"], status = one["Status"], description = one["Description"], instanceid = one["InstanceId"],zone_id = one["ZoneId"],
                    vpc_private_ip = one["VpcAttributes_PrivateIpAddress_IpAddress"], vpc_vswitchid = one["VpcAttributes_VSwitchId"], cpu = one["Cpu"],
                    eip_address_ip = one["EipAddress_IpAddress"], instance_charge_type = one["InstanceChargeType"], memory = one["Memory"], public_ip = one["PublicIpAddress_IpAddress"],
                    security_group_id = one["SecurityGroupIds_SecurityGroupId"], region_id = one["RegionId"], eip_bandwidth = one["InternetMaxBandwidthOut"],
                    inner_ip = one["InnerIpAddress_IpAddress"], status_color= date_color)
        else:
            server = ServersModel.objects.create(server_from="aliyun", vpc_vpcid = one["VpcAttributes_VpcId"], host_name = one["HostName"], instance_family = one["InstanceTypeFamily"],
                    create_time = one["CreationTime"], expired_time = one["ExpiredTime"], io_optimized = one["IoOptimized"], instance_type = one["InstanceType"],
                    eip_intercharge_type = one["EipAddress_InternetChargeType"], internet_charge_type = one["InternetChargeType"], image_id = one["ImageId"],
                    instance_name = one["InstanceName"], status = one["Status"], description = one["Description"], instanceid = one["InstanceId"],zone_id = one["ZoneId"],
                    vpc_private_ip = one["VpcAttributes_PrivateIpAddress_IpAddress"], vpc_vswitchid = one["VpcAttributes_VSwitchId"], cpu = one["Cpu"],
                    eip_address_ip = one["EipAddress_IpAddress"], instance_charge_type = one["InstanceChargeType"], memory = one["Memory"], public_ip = one["PublicIpAddress_IpAddress"],
                    security_group_id = one["SecurityGroupIds_SecurityGroupId"], region_id = one["RegionId"], eip_bandwidth = one["InternetMaxBandwidthOut"],
                    inner_ip = one["InnerIpAddress_IpAddress"], status_color= date_color)
            server.save()
    all_servers = ServersModel.objects.filter(server_from="aliyun")
    for one in all_servers:
        if one.instanceid not in many_keys:
            server = get_one_instance_info(one.instanceid)
            print server['Instances']['Instance']
            if len(server['Instances']['Instance']) != 1:
                one.delete()


def change_group_info(instanceid):
    try:
        T = AliyunMonitor("https://ecs.aliyuncs.com", ALIYUN_KEY, ALIYUN_SECRET)
        instanceid = str(instanceid.strip(' '))
        data = {"RegionId":'cn-hangzhou',"Action":"DescribeInstances","InstanceIds": [instanceid, ]}
        server = T.do_request(data)
        server = get_one_instance_info(instanceid)
        if len(server['Instances']['Instance']) == 1:
            one = server['Instances']['Instance'][0]
            server = ServersModel.objects.create(server_from="aliyun", create_time = one["CreationTime"], expired_time = one["ExpiredTime"], instance_type = one["InstanceType"],
                    image_id = one["ImageId"],instance_name = one["InstanceName"], status = one["Status"], instanceid = instanceid, zone_id = one["ZoneId"],
                    cpu = one["Cpu"], instance_charge_type = one["InternetChargeType"], memory = one["Memory"], public_ip = "creating",
                    region_id = one["RegionId"], eip_bandwidth = one["InternetMaxBandwidthOut"], inner_ip = "creating", status_color= 'green', mem='未初始化')
            server.save()

    except Exception as e:
        logger.error('批量创建项目,修改分组名失败:' + traceback.format_exc())


#pay attention to my account and company account
def change_name(instanceid, name, description, regionId="cn-hangzhou"):
    endTime = time.strftime("%Y-%m-%d") + "T15:00Z"
    T = AliyunMonitor("https://ecs.aliyuncs.com", ALIYUN_KEY, ALIYUN_SECRET)
    result = T.do_request({"RegionId":regionId,"Action":"ModifyInstanceAttribute","InstanceId":instanceid,"InstanceName":name,
                            "Description": description,"EndTime":endTime})
    return result

#对服务器执行的操作，包括启动，停止，重启三项行为
def handle_server(self, instanceid, action, regionId="cn-beijing"):
    endTime = time.strftime("%Y-%m-%d") + "T15:00Z"
    T = AliyunMonitor("https://ecs.aliyuncs.com", ALIYUN_KEY, ALIYUN_SECRET)
    result = 'hehe'
    logger.error(str(self.request.user) + "对服务器: " + instanceid + " 执行了操作: " + action)
    result = T.do_request({"RegionId":regionId,"Action":action,"InstanceId":instanceid,"EndTime":endTime})
    return result


#新建镜像
def create_image(instanceid, regionId="cn-beijing"):
    T = AliyunMonitor("https://ecs.aliyuncs.com", ALIYUN_KEY, ALIYUN_SECRET)
    result = T.do_request({"RegionId": regionId, "Action": "CreateImage", "InstanceId": instanceid})
    return result


#购买服务器
def create_instance(data, server_group=''):
    server_infos = data['many_servers']
    nums = {}
    if data['InstanceName']:
        if data['InstanceName'] not in server_infos:
            name = data.pop('InstanceName')
            if 'num' in data.keys():
                num = data.pop('num')
            else:
                num = 1
            nums.update({name:num})

    infos = server_infos.split(',')
    for one in infos:
        one = one.strip(' ')
        if one :
            one = one.replace('台', '')
            one = one.split('服务器')
            nums.update({one[0]: one[1]})
    instance_io_type = data['change_instance_type']
    for key,value in nums.items():
        param = data
        param.update({'InstanceName': key, 'num': value, 'change_instance_type': instance_io_type})
        result = create_aliyun_instance(param, server_group=server_group)
    return result



def create_aliyun_instance(data, server_group=''):
    params = {'InstanceChargeType': 'PrePaid', 'Action': 'CreateInstance'}

    #如果是io优化得实例类型，需要加上io优化的参数。
    instance_io_type = data.pop('change_instance_type')
    times = data.pop('num')
    if instance_io_type == u"io_instanceType":
        type_result = data["io_InstanceType"]
        params.update({"InstanceType": type_result})
        params.update({"IoOptimized": "optimized"})
    elif instance_io_type == u'instanceType':
        type_result = data["no_InstanceType"]
        params.update({'InstanceType': type_result})

    for key ,value in data.items():
        if key in ('passwd1', 'passwd2', 'csrfmiddlewaretoken', 'num', 'no_InstanceType', 'io_instanceType', 'io_InstanceType'):
            continue
        if key == "ZoneId":
            RegionId = data['ZoneId'].split('-')
            params.update({'RegionId': RegionId[0] + '-' + RegionId[1]})
        params.update({key: value})
    if 'InstanceChargeType' in params.keys() and params['InstanceChargeType'] == 'PostPaid':
        if 'Period' in params.keys():
            params.pop('Period')
    T = AliyunMonitor("https://ecs.aliyuncs.com", ALIYUN_KEY, ALIYUN_SECRET)
    try:
        results = []
        for n in range(int(times)):
            time.sleep(1)
            result = T.do_request(params)
            results.append(result)
            logger.debug("to buy aliyun instance:" + json.dumps(params))
            logger.debug("the result is : " + json.dumps(result))
        time.sleep(2)
        for one in results:
            print 'get public IP for server : ', one
            if server_group:
                change_group_info(one['InstanceId'])
            result = get_public_ip(one['InstanceId'])
            logger.debug('have get public IP , the server is: ' + str(one) + ', result is : ' + str(result))
        result = "购买成功，请去服务器列表页面启动服务器"
    except Exception, e:
        logger.error(traceback.format_exc())
        result = "失败，请联系管理员"
    return result


#通过api创建得服务器，需要调用这个接口申请公网IP
def get_public_ip(instanceid):
    T = AliyunMonitor("https://ecs.aliyuncs.com", ALIYUN_KEY, ALIYUN_SECRET)
    result = T.do_request({"Action":"AllocatePublicIpAddress","InstanceId":instanceid})
    return result


#获取数据库信息进数据库
def get_rds():
    T = AliyunMonitor("https://rds.aliyuncs.com", ALIYUN_KEY, ALIYUN_SECRET, version='2014-08-15')
    re = T.do_request({"Action":"DescribeDBInstances","RegionId":"cn-hangzhou"})
    pay_type = {'Postpaid': '按量付费', 'Prepaid': '预付费'}
    instance_type = {'Primary': '主实例', 'ReadOnly': '只读实例', 'Readonly': '只读实例', 'Guard': '灾备实例', 'Temp': '临时实例'}
    db_net_type = {'Internet': '外网', 'Intranet': '内网'}
    try:
        ids = ''
        for one in re['Items']["DBInstance"]:
            ids = ids + ',' + one["DBInstanceId"]
        ids = ids.strip(',')

        result = T.do_request({'Action': 'DescribeDBInstanceAttribute', 'DBInstanceId': ids})
        detail = result['Items']['DBInstanceAttribute']
        all_keys = []
        for one in detail:
            all_keys.append(one["DBInstanceId"])
            rds = RdsModel.objects.filter(instanceid=one['DBInstanceId'])
            one['PayType'] = pay_type[one['PayType']]
            one['DBInstanceType'] = instance_type[one['DBInstanceType']]
            one["DBInstanceNetType"] = db_net_type[one['DBInstanceNetType']]

            if one['ZoneId'] == "cn-hangzhou-MAZ1(b,c)":
                one['ZoneId'] = '华东1可用区B+可用区C'
            elif one['ZoneId'].startswith('cn-hangzhou'):
                one['ZoneId'] = one['ZoneId'].replace('cn-hangzhou', '华东1可用区')
            if 'CreationTime' in one.keys():
                one.update({'CreateTime': one['CreationTime']})
            if 'DBInstanceDescription' not in one.keys():
                one.update({"DBInstanceDescription": ''})

            atime = one['ExpireTime']
            if atime:
                atime = atime.split('T')
                atime = atime[0].split('-')
                d1 = datetime.datetime(int(atime[0]), int(atime[1]), int(atime[2]))
                d3 = d1 + datetime.timedelta(days=1)
                one['ExpireTime'] = d3.strftime('%Y-%m-%d') + ' 00:00'
                if 0 <= (d3 - datetime.datetime.now()).days < 15:
                    date_color = 'red'
                elif (d3 - datetime.datetime.now()).days <0:
                    one["Status"] = 'Stopped'
                    date_color = 'black'
                else:
                    date_color = 'green'
            else:
                date_color = 'green'

            if rds:
                new_rds = rds.update(server_type='aliyun', engine_version=one['Engine'] + one['EngineVersion'],instance_type=one['DBInstanceType'],
                    instanceid=one['DBInstanceId'], instance_name=one['DBInstanceDescription'],status=one['DBInstanceStatus'],
                    pay_type=one['PayType'], zone_id=one['ZoneId'],net_type=one['InstanceNetworkType'],db_net_type=one['DBInstanceNetType'],
                    connect_mode=one['ConnectionMode'],deadline_time=one['ExpireTime'], create_time=one['CreateTime'],
                    storage_size=one['DBInstanceStorage'],mem=one['DBInstanceMemory'], vport=one['Port'],max_query=one['MaxIOPS'],
                    cpu=one['DBInstanceCPU'], status_color=date_color)
                server = rds[0]
            else:
                new_rds = RdsModel.objects.create(server_type='aliyun', engine_version=one['Engine'] + one['EngineVersion'],instance_type=one['DBInstanceType'],
                    instanceid=one['DBInstanceId'], instance_name=one['DBInstanceDescription'],status=one['DBInstanceStatus'],
                    pay_type=one['PayType'], zone_id=one['ZoneId'],net_type=one['InstanceNetworkType'],db_net_type=one['DBInstanceNetType'],
                    connect_mode=one['ConnectionMode'],deadline_time=one['ExpireTime'], create_time=one['CreateTime'],
                    storage_size=one['DBInstanceStorage'],mem=one['DBInstanceMemory'], vport=one['Port'],max_query=one['MaxIOPS'],
                    cpu=one['DBInstanceCPU'], status_color=date_color)
                new_rds.save()
        all_servers = RdsModel.objects.filter(server_type="aliyun")
        for one in all_servers:
            if one.instanceid not in all_keys:
                one.delete()
    except Exception, e:
        logger.error(traceback.format_exc())
        logger.error(json.dumps(one))


# 购买阿里云数据库
def create_rds(pay_type ,zone,db_class, db_storage, net_type, months, num, ip_list):
    T = AliyunMonitor("https://rds.aliyuncs.com", ALIYUN_KEY, ALIYUN_SECRET, version='2014-08-15')
    clinet_token = time.strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999)) # 唯一值,保证幂等性 
    params = {"Action":"CreateDBInstance","RegionId":"cn-hangzhou", 'Engine': "MySQL", 'ZoneId': zone, 'EngineVersion': '5.6',
        'DBInstanceClass': db_class, 'DBInstanceStorage': db_storage, 'DBInstanceNetType': net_type, 'SecurityIPList': ip_list,
        'PayType': pay_type, 'Period': 'Month', 'UsedTime': months, 'ClientToken': clinet_token}
    if params['PayType'] == 'Postpaid':
        params.pop('Period')
        params.pop('UsedTime')
    logger.error('购买阿里云数据库参数:' + json.dumps(params))
    re = T.do_request(params)
    logger.error('购买结果:' + json.dumps(re))
    return '购买成功'


#验证阿里云域名过期
def check_dns():
    T = AliyunMonitor("https://alidns.aliyuncs.com", ALIYUN_KEY, ALIYUN_SECRET, version='2015-01-09', time_stamp="Timestamp")
    dnses = T.do_request({"PageSize": '99',"Action":"DescribeDomains"})
    data = dnses['Domains']['Domain']
    num = 0
    for one in data:
        num += 1
        try:
            dns = one['PunyCode']
            result = T.do_request({"DomainName": dns,"Action":"DescribeDomainWhoisInfo"})
            now = datetime.datetime.utcnow()
            if isinstance(result, str):
                continue
            if 'ExpirationDate' in result.keys():
                date = result['ExpirationDate']
            else:
                date = "2017-02-23T5"

            date, _ = date.split("T")
            atime = date.split('-')
            ex_date = datetime.datetime(int(atime[0]), int(atime[1]), int(atime[2]))
            days =  ex_date - now
            days = days.days
            if days < 365:
                content = "您的域名:" + dns + "还有" + str(days) + "天就要过期了,不要忘了续费哟!"
                send_alarm(content, "18513950766")
                send_alarm(content, "18500040230")
        except Exception as e:
            logger.error(traceback.format_exc())

    data = T.do_request({"PageSize": '99',"Action":"DescribeDnsProductInstances"})
    data = data['DnsProducts']['DnsProduct']
    for one in data:
        date = one['EndTime']
        date, _ = date.split("T")
        atime = date.split('-')
        ex_date = datetime.datetime(int(atime[0]), int(atime[1]), int(atime[2]))
        now = datetime.datetime.utcnow()
        days =  ex_date - now
        days = days.days
        if days < 365:
            content = "您的云解析VIP产品:" + one['InstanceId'] + "还有" + str(days) + "天就要过期了,不要忘了续费哟!"
            send_alarm(content, "18513950766")
            send_alarm(content, "18500040230")


