#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.QcloudApi.qcloudapi import QcloudApi
import json
import sys
import datetime
import traceback
import logging
import re
from utils import send_alarm
from models import ServersModel, RdsModel, ServerConf
from Free.settings import QCLOUD_KEY, QCLOUD_VALUE

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger("free")

STATUS_CH = {'1': '故障', '2': '运行中', '3': '创建中', '4': '已关机', '5': '已退还', '6': '退还中', '7': '重启中', '8': '开机中', '9': '关机中', '10': '密码重置中', '11': '格式化中', '12': '镜像制作中', '13': '带宽设置中', '14': '重装系统中', '15': '域名绑定中', '16': '域名解绑中', '17': '负载均衡绑定中', '18': '负载均衡解绑中', '19': '升级中', '20': '秘钥下发中', '21': '维护中'}
PAY_TYPE = {'0': '按月结算的后付费', '1': "包年包月", "2": '按量计费'}
NET_PAY = {'0': '按月结算的后付费', '1': '包年包月', '2': '按流量', '3': "按带宽"}


#腾讯给的调用api的SDK
def qcloud(module, action, region, params):
    config = {
        'Region': region,
        'secretId': QCLOUD_KEY,
        'secretKey': QCLOUD_VALUE,
        'method': 'post'
    }

    try:
        service = QcloudApi(module, config)
        response = service.call(action, params)
        obj = json.loads(response)
        return obj
    except Exception, e:
        print 'exception:', e


#获取上海，广州，北京的服务器信息，且存入数据库
def deal_qcloud():
    all_keys = []
    for regi in ("sh", "gz", "bj"):
        result = qcloud('cvm', 'DescribeInstances', regi, {'limit': 99})
        if 'instanceSet' in result:
            result = result.pop('instanceSet')
        else:
            continue
        for item in result:
            all_keys.append(item['unInstanceId'])
            one = {}
            for key in item.keys():
                if isinstance(item[key], dict):
                    for n_key in item[key].keys():
                        one.update({str(key) + '_' + str(n_key): str(item[key][n_key])})
                else:
                    if key == "status":
                        item[key] = STATUS_CH[str(item[key])]
                    if isinstance(item[key], list):
                        item[key] = item[key][0]
                    try:
                        one.update({str(key): str(item[key])})
                    except Exception, e:
                        one.update({str(key): item[key]})
            change = {"status": STATUS_CH, "cvmPayMode": PAY_TYPE, "networkPayMode": NET_PAY}
            for t_name, t_value in change.items():
                try:
                    one[t_name] = t_value[one[t_name]]
                except Exception, e:
                    continue
            atime = one["deadlineTime"].split(' ')
            atime = atime[0].split('-')
            d3 = datetime.datetime(int(atime[0]), int(atime[1]), int(atime[2]))
            if 0 <= (d3 - datetime.datetime.now()).days < 10:
                date_color = 'red'
            elif (d3 - datetime.datetime.now()).days < 0:
                date_color = 'black'
            else:
                date_color = 'green'
            server = ServersModel.objects.filter(instanceid=one["unInstanceId"])
            if server:
                try:

                    server.update(server_from='qcloud', dick_root=one["diskInfo_rootSize"], dick_storage=one["diskInfo_storageSize"],
                            create_time = one["createTime"], expired_time = one["deadlineTime"],
                            eip_intercharge_type = one["networkPayMode"], internet_charge_type = one["networkPayMode"], image_id = one["os"],
                            instance_name = one["instanceName"], status = one["status"], instanceid = one["unInstanceId"],zone_id = one["zoneName"],
                            cpu = one["cpu"], instance_charge_type = one["cvmPayMode"], memory = one["mem"], public_ip = one["wanIpSet"],
                            region_id = one["Region"], eip_bandwidth = one["bandwidth"], inner_ip = one["lanIp"], status_color= date_color)
                except Exception, e:
                    logger.error(traceback.format_exc())
            else:
                one = ServersModel.objects.create(server_from='qcloud', dick_root=one["diskInfo_rootSize"], dick_storage=one["diskInfo_storageSize"],
                            create_time = one["createTime"], expired_time = one["deadlineTime"],
                            eip_intercharge_type = one["networkPayMode"], internet_charge_type = one["networkPayMode"], image_id = one["os"],
                            instance_name = one["instanceName"], status = one["status"], instanceid = one["unInstanceId"],zone_id = one["zoneName"],
                            cpu = one["cpu"], instance_charge_type = one["cvmPayMode"], memory = one["mem"], public_ip = one["wanIpSet"],
                            region_id = one["Region"], eip_bandwidth = one["bandwidth"], inner_ip = one["lanIp"], status_color= date_color)
                one.save()
    all_servers = ServersModel.objects.filter(server_from="qcloud")
    for one in all_servers:
        if one.instanceid not in all_keys:
            one.delete()



# 对腾讯云服务器的操作：包括启动，停止和重启。这个api允许一次执行多个实例的，但页面上没有实现
def op_server(instanceid, action, region):
    result = qcloud("cvm", action, region, {"instanceIds.1": instanceid})
    return result


#修改腾讯云服务器名称
def qcloud_change_name(instanceid, action, region, new_name):
    result = qcloud("cvm", action, region, {"instanceId": instanceid, "instanceName": new_name})
    return result


#购买腾讯云服务器实例
def create_qcloud(data):
    region = data.pop("change_region_cvm")
    params = {"wanlp": "1", "needSecurityAgent": "1", "needMonitorAgent": "1", "storageType": '2'}
    passwd = data['passwd1']
    match = re.match(ur'^([a-z,A-z,0-9]{8,16}|[0-9,\W]{8,16}|[a-z,A-Z,\W]{8,16}|[a-z,A-Z,0-9,\W]{8,16})$', passwd)
    if not match:
        return "密码格式有误，请按要求输入"
    else:
        params.update({"password": passwd})

    for key, value in {"100002": "region_g2", "100003": "region_g3", "200001": "region_s1", "800001": "region_b1", "300001": "region_x1"}.items():
        if region == key:
            config = data[value]
            config = config.split("-")
            params.update({"cpu": config[0]})
            params.update({"mem": config[1]})
            params.update({"zoneId": region})
            break
    region_change = {"100002": "gz", "100003": "gz", "200001": "sh", "800001": "bj", "300001": 'xg'}
    for key, value in data.items():
        if key in ("region_g2", 'region_g3', "region_s1", "region_b1", "region_x1", "passwd1", "passwd2", "csrfmiddlewaretoken"):
            continue
        params.update({key: value})
    logger.error('购买腾讯云服务器,参数: ' + json.dumps(params))
    result = qcloud("cvm", "RunInstances", region_change[region], params)
    logger.error('购买完成,result is : ' + json.dumps(result))
    if result["message"] == "":
        result = "购买成功"
    else:
        result = result["message"]
    return result


#获取服务器信息
def get_rds():
    try:
        result = qcloud('cdb', 'DescribeCdbInstances', 'sh', {})
        TAST_TRAN = {'0': '没有任务', '1': '升级中', '2': '数据导入中', '3': '开放Slave中', '4': '外网访问开通中', '5': '批量操作执行中',
            '6': '回档中', '7':'外网访问关闭中', '8': '密码修改中', '9': '实例名修改中', '10': '重启中', '12': '自建迁移中', '13': '删除库表中','14': '灾备实例创建同步中'}
        PAY_TRAN = {'0': '包年包月', '1': '按量计费', '2': '后付费月结'}
        results = result['cdbInstanceSet']
        all_keys = []
        for one in results:
            all_keys.append(one["uInstanceId"])
            one['taskStatus'] = TAST_TRAN[str(one['taskStatus'])]
            one['payType'] = PAY_TRAN[str(one['payType'])]
            zone = ServerConf.objects.get(server_type='qcloud', info_type='zone', key=one['zoneId'])
            one['zoneId'] = zone.value
            if one['status'] == 1:
                one['status'] ='运行中'
            else:
                one['status'] = '创建中'
            for key,value in one.items():
                one[key] = str(value)

            atime = one["cdbInstanceDeadlineTime"].split(' ')
            atime = atime[0].split('-')
            d3 = datetime.datetime(int(atime[0]), int(atime[1]), int(atime[2]))
            if 0 <= (d3 - datetime.datetime.now()).days < 10:
                date_color = 'red'
            elif (d3 - datetime.datetime.now()).days < 0:
                date_color = 'black'
            else:
                date_color = 'green'

            rds = RdsModel.objects.filter(instanceid=one['uInstanceId'])
            if rds:
                new_rds = rds.update(instanceid=one['uInstanceId'], engine_version= 'mysql' + one['engineVersion'], instance_type=one['cdbType'],
                        instance_name=one['cdbInstanceName'], vpcid=one['vpcId'], instance_vpcid=one['cdbInstanceVip'],
                        status=one['status'], task_status=one['taskStatus'], pay_type=one['payType'], zone_id=one['zoneId'],
                        storage_size=one['storageSize'], mem=one['memory'], volume=one['volume'], autoRenew=one['autoRenew'],
                        max_query=one['maxQueryCount'], type_set=one['cdbTypeSet'], vport=one['cdbInstanceVport'],
                        deadline_time=one['cdbInstanceDeadlineTime'], create_time=one['cdbInstanceCreateTime'],status_color=date_color)
            else:
                new_rds = RdsModel.objects.create(instanceid=one['uInstanceId'], engine_version= 'mysql' + one['engineVersion'], instance_type=one['cdbType'],
                        instance_name=one['cdbInstanceName'], vpcid=one['vpcId'], instance_vpcid=one['cdbInstanceVip'],
                        status=one['status'], task_status=one['taskStatus'], pay_type=one['payType'], zone_id=one['zoneId'],
                        storage_size=one['storageSize'], mem=str(one['memory']), volume=one['volume'], autoRenew=one['autoRenew'],
                        max_query=one['maxQueryCount'], type_set=one['cdbTypeSet'], vport=one['cdbInstanceVport'],
                        deadline_time=one['cdbInstanceDeadlineTime'], create_time=one['cdbInstanceCreateTime'], status_color=date_color)
                new_rds.save()
        all_servers = RdsModel.objects.filter(server_type='qcloud')
        for one in all_servers:
            if one.instanceid not in all_keys:
                one.delete()
    except Exception, e:
        print traceback.format_exc()


#购买数据库
def create_qcloud_rds(months, num, mem, volume, zone):
    params = {'cdbType': 'CUSTOM', 'engineVersion': '5.6', 'period': months, 'goodsNum': num, 'memory': mem, 'volume': volume, 'zoneId': zone}
    result = qcloud('cdb', 'CreateCdb', 'sh', params)
    #result = {'message': 'just try'}
    logger.error('购买腾讯云数据库,参数为: ' + json.dumps(params))
    logger.error('购买结果为: ' + json.dumps(result))
    if 'Success' in json.dumps(result):
        return '购买成功'
    else:
        return '可能出错了,请联系管理员.'
