# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import Department
import random


class ServersGroup(models.Model):
    '''服务器组别'''
    name = models.CharField(max_length=64,verbose_name='名称',null=True, blank=True)
    server_type = models.CharField(max_length=20, default="aliyun", verbose_name="服务器类型")
    description = models.CharField(max_length=2000, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '服务器组别'
        verbose_name_plural = '服务器组别列表'


class ServersModel(models.Model):
    '''服务器详情'''
    server_from = models.CharField(max_length=20, default='aliyun', verbose_name='阿里云/腾讯云')
    server_group = models.ForeignKey(ServersGroup, verbose_name='所属组别', null=True, blank=True)
    instanceid = models.CharField(max_length=50, unique=True, verbose_name="ecs id")
    instance_name = models.CharField(max_length=90, verbose_name="ecs name")
    region_id = models.CharField(max_length=20, verbose_name="地域")
    zone_id = models.CharField(max_length=20, verbose_name="所在可用区域")
    host_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="名称")
    io_optimized = models.BooleanField(default=False)
    cpu = models.IntegerField(verbose_name="CPU")
    memory = models.IntegerField(verbose_name="内存")
    dick_root = models.CharField(max_length=10, null=True, blank=True, verbose_name="系统盘")
    dick_storage = models.CharField(max_length=10, blank=True, null=True, verbose_name="数据盘")
    eip_bandwidth = models.CharField(max_length=9, verbose_name="带宽")
    create_time = models.CharField(max_length=25, verbose_name="创建时间")
    expired_time = models.CharField(max_length=25, verbose_name="到期时间")
    status = models.CharField(max_length=15, verbose_name="状态")
    description = models.CharField(max_length=300, null=True, blank=True, verbose_name="描述")
    image_id = models.CharField(max_length=50, verbose_name="镜像ID")
    public_ip = models.CharField(max_length=20, verbose_name="外网IP")
    inner_ip = models.CharField(max_length=20, verbose_name="内网IP")
    eip_address_ip = models.CharField(max_length=20, blank=True, null=True, verbose_name="弹性公网IP")
    instance_type = models.CharField(max_length=20, verbose_name="实例规格")
    instance_charge_type = models.CharField(max_length=15, verbose_name="付费方式")
    vpc_vpcid = models.CharField(max_length=30, blank=True, null=True, verbose_name="专有网络")
    vpc_private_ip = models.CharField(max_length=30, blank=True, null=True, verbose_name="私有IP")
    vpc_vswitchid = models.CharField(max_length=30, blank=True, null=True, verbose_name="虚拟交换机")
    instance_family = models.CharField(max_length=30, blank=True, null=True, verbose_name="实例规格族")
    security_group_id = models.CharField(max_length=200, blank=True, null=True, verbose_name="安全组ID")
    eip_intercharge_type = models.CharField(max_length=30, blank=True, null=True, verbose_name="网络交换方式")
    internet_charge_type = models.CharField(max_length=30, blank=True, null=True, verbose_name="宽带计费方式")
    eip_is_supportUnassociate = models.BooleanField(default=False, verbose_name="弹性公网IP是否支持解绑")
    status_color = models.CharField(max_length=15, default='black', verbose_name='是否快到期')
    send_alarm = models.BooleanField(default=False, verbose_name="是否发送报警")
    modify_time = models.DateTimeField(auto_now=True)
    mem = models.CharField(max_length=256, default=True, null=True, verbose_name="备注")

    def __unicode__(self):
        return self.instance_name

    class Meta:
        verbose_name = '服务器信息'
        verbose_name_plural = '服务器信息列表'
        ordering = ['-id']


class RdsModel(models.Model):
    """云服务器的数据库"""

    SERVER_TYPR =(
        ('阿里云', 'aliyun'),
        ('腾讯云', 'qcloud'),
        )
    server_type = models.CharField(max_length=20, choices=SERVER_TYPR, default='qcloud', verbose_name='平台类型')
    engine_version = models.CharField(max_length=30, verbose_name='数据库版本')
    instance_type = models.CharField(max_length=20, verbose_name='数据库类型')
    instanceid = models.CharField(max_length=50, verbose_name='实例ID')
    instance_name = models.CharField(max_length=64, verbose_name='实例名称')
    vpcid = models.CharField(max_length=32, blank=True, null=True, verbose_name='访问ID')
    instance_vpcid = models.CharField(max_length=32, blank=True, null=True, verbose_name='私有ID')
    status = models.CharField(max_length=15, verbose_name='状态')
    task_status = models.CharField(max_length=16, blank=True, null=True, verbose_name='qcloud任务状态')
    pay_type = models.CharField(max_length=10, verbose_name='付款方式')
    zone_id = models.CharField(max_length=25, verbose_name='可用区域')
    net_type = models.CharField(max_length=15, verbose_name='网络类型')
    db_net_type = models.CharField(max_length=15, verbose_name='aliyun外网or内网')
    connect_mode = models.CharField(max_length=15, verbose_name='连接模式')
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name='描述')
    storage_size = models.CharField(max_length=20, verbose_name='存储容量')
    cpu = models.CharField(max_length=10, blank=True, null=True, verbose_name='cpu')
    mem = models.CharField(max_length=10, blank=True, null=True, verbose_name='内存')
    volume = models.CharField(max_length=16, blank=True, null=True, verbose_name='硬盘大小')
    autoRenew = models.CharField(max_length=5, blank=True, null=True, verbose_name='qcloud自动续费')
    max_query = models.CharField(max_length=10, blank=True, null=True, verbose_name='最大连接数,次/秒')
    type_set = models.CharField(max_length=32, blank=True, null=True, verbose_name='qcloud实例类型的序号')
    vport = models.CharField(max_length=10, default='3306', verbose_name='端口号')
    deadline_time = models.CharField(max_length=25, verbose_name='到期时间')
    status_color = models.CharField(max_length=15, default='black', verbose_name='是否快到期')
    send_alarm = models.BooleanField(default=False, verbose_name="是否发送报警")
    create_time = models.CharField(max_length=25, verbose_name='创建时间')

    def __unicode__(self):
        return self.instanceid

    class Meta:
        verbose_name = '数据库信息'
        verbose_name_plural = '数据库列表'
        ordering = ['-id']          

    def get_absolute_url(self):
        return '/assets/rds_detail/%i' % self.id


class EmpLoyeeModel(models.Model):
    name = models.CharField(max_length=20, verbose_name="姓名")
    department = models.ForeignKey(Department, verbose_name="部门")
    status = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '员工资产信息'
        verbose_name_plural = '员工资产信息列表'
        ordering = ['-id']


class ItemList(models.Model):
    name = models.CharField(max_length=20, verbose_name="物品名")
    employee = models.ForeignKey(EmpLoyeeModel, verbose_name="员工归属", blank=True, null=True)
    item_type = models.CharField(max_length=10, verbose_name='物品类别')
    item_num = models.CharField(max_length=15, verbose_name="物品编号")
    return_time = models.CharField(max_length=30, null=True, blank=True, verbose_name= "归还时间")
    is_return = models.BooleanField(default=False)
    note = models.CharField(max_length=300, verbose_name="备注")
    creat_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '物品信息'
        verbose_name_plural = '物品信息列表'
        ordering = ['id']      


class AliyunTemplate(models.Model):
    '''购买阿里云服务器的模板'''
    name = models.CharField(max_length=32, verbose_name="模板名称")
    zone_id = models.CharField(max_length=20, verbose_name='可用区域')
    cpu = models.CharField(max_length=3, verbose_name='Cpu')
    mem = models.CharField(max_length=9, verbose_name='内存')
    image = models.CharField(max_length=50, verbose_name='镜像')
    bandwidth_paytype = models.CharField(max_length=20, verbose_name='宽带付费方式')
    bandwidth = models.CharField(max_length=9, verbose_name='带宽')
    root_disk = models.CharField(max_length=9, verbose_name='系统盘')
    data_disk = models.CharField(max_length=9, verbose_name='数据盘')
    tem_type = models.CharField(max_length=16, default='aliyun', verbose_name='模板类型')

    def __unicode__(self):
        return self.image

    class Meta:
        verbose_name = '阿里云模板'
        verbose_name_plural = '阿里云模板列表'
        ordering = ['id']


class QcloudTemplate(models.Model):
    '''购买腾讯云服务器的模板'''
    zone_id = models.CharField(max_length=20, verbose_name='可用区域')
    cpu = models.CharField(max_length=3, verbose_name='Cpu')
    mem = models.CharField(max_length=9, verbose_name='内存')
    image = models.CharField(max_length=50, verbose_name='镜像')
    bandwidth_paytype = models.CharField(max_length=20, verbose_name='宽带付费方式')
    bandwidth = models.CharField(max_length=9, verbose_name='带宽')
    root_disk = models.CharField(max_length=9, verbose_name='系统盘')
    data_disk = models.CharField(max_length=9, verbose_name='数据盘')

    def __unicode__(self):
        return self.image

    class Meta:
        verbose_name = '腾讯云模板'
        verbose_name_plural = '腾讯云模板列表'
        ordering = ['id']


class ServerConf(models.Model):
    '''购买服务器时的相关配置'''
    TYPES = (('aliyun', 'aliyun'),
            ('qlcoud', 'qcloud'))
    server_type = models.CharField(max_length=20, choices=TYPES, verbose_name='服务器类型')
    info_type = models.CharField(max_length=20, verbose_name='配置类型')
    key = models.CharField(max_length=60, verbose_name='参数')
    value = models.CharField(max_length=60, verbose_name='显示值')

    def __unicode__(self):
        return self.info_type

    class Meta:
        verbose_name = '服务器配置信息'
        verbose_name_plural = '服务器配置信息列表'
        ordering = ['id']
