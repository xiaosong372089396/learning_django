#-*-coding:utf-8-*-
import time
import datetime
import json
import traceback
import logging
import re
from django.shortcuts import render,HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import TemplateView, ListView, View
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from assets import utils
from assets.utils import LoginRequiredMixin, control_permission, control_permission_context, send_alarm
from django.template import RequestContext
from comptroller.models import OperationModel
from assets import aliyun_api
from assets.qcloud import *
from assets.models import *
from assets.info import *
from assets.tasks import update_data

logger = logging.getLogger("free")
PER_PAGE_NUM = 10


class ServerList(TemplateView):
    '''阿里云服务器列表'''
    template_name = 'assets/server_list.html'

    def __init__(self):
        self.server_type = "aliyun"

    def get_context_data(self, **kwargs):
        context = super(ServerList, self).get_context_data(**kwargs)
        custom_info = self.request.META['HTTP_USER_AGENT']

        if 'iPhone' in custom_info or 'Android' in custom_info:
            phone_status = True
        else:
            phone_status = False
        page_num = self.request.GET.get('page', 1)
        query_key = self.request.GET.get('query_key', '')
        query_value = self.request.GET.get('query_value', '')
        #query_dict = {'name': '实例名称', 'id':'实例ID', 'private_ip': '内网IP', 'publice_ip': '外网IP', 'death_line': '即将到期'}
        results, query_item, query_value = utils.get_servers(query_key, query_value, self.server_type)
        groups = ServersGroup.objects.all()

        p = Paginator(results, PER_PAGE_NUM)
        try:
            page = p.page(int(page_num))
        except:
            page = p.page(1)
        context['page'] = page
        context["groups"] = groups
        context['phone_status'] = phone_status
        context['query_item'] = query_item
        context['query_key'] = query_key
        context['query_value'] = query_value
        return context


class QcloudServers(ServerList):
    '''腾讯云服务器列表'''
    template_name = "assets/qcloud_server.html"

    def __init__(self):
        self.server_type = "qcloud"


class ServerDetail(TemplateView):
    '''服务器详情'''
    template_name = 'assets/server_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ServerDetail, self).get_context_data(**kwargs)
        instanceid = self.request.GET.get('instanceid', '')
        instance = ServersModel.objects.get(instanceid=instanceid)
        groups = ServersGroup.objects.all()
        context['server'] = instance
        context['groups'] = groups
        return context


#更新数据库中服务器信息
def update_data(request):
    try:
        aliyun_api.deal_server()
    except Exception, e:
        logger.error(traceback.format_exc())
    return HttpResponse(json.dumps('bingo'), content_type='application/json')

#更新数据库中腾讯云的服务器
def update_qcloud(request):
    try:
        deal_qcloud()
    except Exception, e:
        logger.error(traceback.format_exc())
    return HttpResponse(json.dumps('bingo'), content_type='application/json')

#更新两种云的数据库
def update_rds(request):
    try:
        get_rds()
    except Exception, e:
        logger.error(traceback.format_exc())
    try:
        aliyun_api.get_rds()
    except Exception, e:
        logger.error(traceback.format_exc())
    return HttpResponse(json.dumps('bingo'), content_type='application/json')


class ServerChangeName(TemplateView):
    """修改服务器名称，腾讯云和阿里云共用一个类，通过服务器类型进行判断修改修改。"""
    template_name = "assets/server_change_name.html"

    @control_permission_context(2)
    def get_context_data(self, **kwargs):
        context = super(ServerChangeName, self).get_context_data(**kwargs)
        instanceid = self.request.GET.get('instanceid')
        instance = ServersModel.objects.get(instanceid=instanceid)
        context['server_type'] = instance.server_from
        context["instanceid"] = instanceid
        return context

    @control_permission(2)
    def post(self, *args, **kwargs):
        instanceid = self.request.POST.get('instanceid')
        name = self.request.POST.get('server_name')
        description = self.request.POST.get('server_description')
        try:
            instance = ServersModel.objects.get(instanceid=instanceid)
            regionid = instance.region_id

            if instance.server_from == "aliyun":
                if utils.check_name(name): #通过正则验证阿里云服务器名称是否合法
                    return HttpResponse("name error名称不合要求", content_type="applications/json")
                result = aliyun_api.change_name(instanceid, name, description, regionid)
            else:
                if len(name) > 50 :
                    return HttpResponse("名称长度请在50个字符以内", content_type="applications/json")
                result = qcloud_change_name(instanceid, "ModifyInstanceAttributes", regionid, name)
            OperationModel.objects.create(pro=self.request.user.profile, user_name=self.request.user.profile.name, opt_type='操作记录', opt_content='修改服务器名称')
            logger.error(str(self.request.user) + "对服务器: " + instanceid + " 执行了操作: " + action)
        except Exception, e:
            logger.error('修改服务器名称失败:' + traceback.format_exc())

        if "Message" in result:
            OperationModel.objects.create(pro=self.request.user.profile, user_name=self.request.user.profile.name, opt_type='操作记录', opt_content='修改服务器名称失败')
            return HttpResponse(json.dumps("修改失败"), content_type="applications/json")
        else:
            #直接修改本地，查询成功后，会自动同步
            instance.instance_name = name
            instance.description = description
            instance.save()
            return HttpResponse(json.dumps("修改成功"), content_type="applications/json")
        

class ServerStop(View):
    """停止服务器"""
    @control_permission(3)
    def get(self, request):
        instance_id = request.GET.get('instanceid', '')
        error_status = False
        try:
            instance = ServersModel.objects.get(instanceid=instance_id)
            if instance.status in ("Stopped", '已关机'):
                return HttpResponse(json.dumps("只可停止running状态的服务器"))
            if instance.server_from == "aliyun":
                result = aliyun_api.handle_server(self,instance_id, "StopInstance", instance.region_id)
                if "Message" in result:
                    error_status = True
            elif instance.server_from == 'qcloud':
                result = op_server(instance_id, "StopInstances", instance.region_id)
                if 'Success' not in json.dumps(result):
                    error_status = True
            else:
                return HttpResponse(json.dumps('lack of server from !'), content_type="application/json")
            content ='关闭服务器: ' + str(instance.id)
            OperationModel.objects.create(pro=self.request.user.profile, user_name=self.request.user.profile.name, opt_type='操作记录', opt_content=content)
            if error_status:
                logger.error('stop server fail. instance_id: ' + instance_id + 'result is :' + json.dumps(result) + time.strftime("%Y-%m-%d %H:%m:%s") )
                return HttpResponse(json.dumps('stop server failed !'), content_type="application/json")
            else:
                return HttpResponse(json.dumps("已关闭，请两分钟后刷新查看"), content_type="applications/json")
        except Exception, e:
            logger.error(traceback.format_exc() + ' \n , stop server error ' + time.strftime("%Y-%m-%d %H:%m:%s"))


class ServerStart(View):
    """启动服务器"""
    @control_permission(2)
    def get(self, request):
        try:
            instanceid = request.GET.get('instanceid', '')
            instance = ServersModel.objects.get(instanceid=instanceid)
            error_status = False
            if instance.status in ("Running", '运行中'):
                return HttpResponse(json.dumps("只可启动stop状态的服务器"))
            if instance.server_from == "aliyun":
                result =aliyun_api.handle_server(self, instanceid, "StartInstance", instance.region_id)
                if 'Message' in result:
                    error_status = True
            elif instance.server_from == 'qcloud':
                result = op_server(instanceid, "StartInstances", instance.region_id)
                if 'Success' not in json.dumps(result):
                    error_status = True
            else:
                return HttpResponse(json.dumps('lack of server from !'), content_type="application/json")
            content = '启动服务器:' + str(instanceid)  
            OperationModel.objects.create(pro=self.request.user.profile, user_name=self.request.user.profile.name, opt_type='操作记录', opt_content=content)
            if error_status:
                logger.error('start server fail. instance_id: ' + instanceid + 'result is :' + json.dumps(result) + time.strftime("%Y-%m-%d %H:%m:%s"))
                return HttpResponse(json.dumps('启动失败,请联系管理员 !'), content_type="application/json")
            else:
                return HttpResponse(json.dumps("启动成功!请两分钟后刷新查看"), content_type="applications/json")
        except Exception, e:
            print traceback.format_exc()


class ServerReboot(View):
    '''重启服务器'''
    @control_permission(3)
    def get(self, request):
        instanceid = request.GET.get('instanceid', '')
        instance = ServersModel.objects.get(instanceid=instanceid)
        if instance.status == "Stopped":
            return HttpResponse(json.dumps("只可重启running状态的服务器"))
        error_status = False
        if instance.server_from == "aliyun":
            result = aliyun_api.handle_server(self, instanceid, "RebootInstance", instance.region_id)
            if "Message" in result:
                error_status = True
        elif instance.server_from == 'qcloud':
            result = op_server(instanceid, "RestartInstances", instance.region_id)
            if 'Success' not in json.dumps(result):
                error_status = True
        else:
            return HttpResponse(json.dumps('lack of server from !'), content_type="application/json")
        content = '重启服务器:' + str(instanceid)
        OperationModel.objects.create(pro=self.request.user.profile, user_name=self.request.user.profile.name, opt_type='操作记录', opt_content=content)
        if error_status:
            logger.error('reboot server fail. instance_id: ' + instanceid + 'result is :' + result + time.strftime("%Y-%m-%d %H:%m:%s"))
            return HttpResponse(json.dumps('start server failed !'), content_type="application/json")
        else:
            return HttpResponse(json.dumps("重启成功,请两分钟后刷新"), content_type="applications/json")        

        

class CreateImage(View):
    """创建镜像"""
    def get(self, request):
        instanceid = request.GET.get('instanceid')
        instance = ServersModel.objects.get(instanceid=instanceid)
        result = aliyun_api.create_image(instanceid, instance.region_id)
        if 'Message' in result.keys():
            logger.error('create image fail. instance_id: ' + instanceid + 'result is :' + result + time.strftime("%Y-%m-%d %H:%m:%s"))
            return HttpResponse(json.dumps('create image failed !'), content_type="application/json")
        else:
            return HttpResponse(json.dumps("create image success!"), content_type="applications/json")


class GetImage(TemplateView):
    '''获取阿里云所有的镜像'''
    template_name = 'assets/image_list.html'
    
    def get_context_data(self, **kwargs):
        context =  super(GetImage, self).get_context_data(**kwargs)
        images = aliyun_api.get_images()
        context['images'] = images
        return context


class ServerGroups(TemplateView):
    """阿里云服务器分组列表"""
    template_name = 'assets/aliyun_groups.html'
    def get_context_data(self, **kwargs):
        context = super(ServerGroups, self).get_context_data(**kwargs)
        groups = ServersGroup.objects.all()
        context['groups'] = groups
        context["server_url"] = '/assets/add_group/'
        return context


class ServerType(TemplateView):
    '''服务器类型，展示阿里云和腾讯云的概况'''
    template_name = "assets/server_type.html"

    def get_context_data(self, **kwargs):
        context = super(ServerType, self).get_context_data(**kwargs)
        server_count = ServersModel.objects.filter(server_from="aliyun").count()
        aliyun_group_count = ServersGroup.objects.filter(server_type='aliyun').count
        qcloud_group_count = ServersGroup.objects.filter(server_type='qcloud').count
        date_server = ServersModel.objects.filter(status_color='red', server_from="aliyun").count()
        context['aliyun'] = {'data_server': date_server, 'server_count': server_count, 'aliyun_group_count': aliyun_group_count}
        qcloud_count = ServersModel.objects.filter(server_from="qcloud").count()
        qcloud_server = ServersModel.objects.filter(server_from="qcloud", status_color="red").count()
        context["qcloud"] = {"data_server": qcloud_server, "server_count": qcloud_count, 'qcloud_group_count': qcloud_group_count}
        return context


class QcloudGroups(LoginRequiredMixin, TemplateView):
    template_name = "assets/qcloud_groups.html"
    def get_context_data(self, **kwargs):
        context = super(QcloudGroups, self).get_context_data(**kwargs)
        groups = ServersGroup.objects.filter(server_type='qcloud')
        results = []
        num = 0
        for one in groups:
            results.append([])
            index = num/4
            all_count = ServersModel.objects.filter(server_group=one, server_from="qcloud").count()
            date_count = ServersModel.objects.filter(server_group=one, status_color='red',server_from="qcloud").count()
            results[index].append({'name': one.name, 'count': all_count, 'date_count': date_count})
        context['server_url'] = '/assets/add_group/'
        context['server_type'] = 'qcloud'
        context['groups'] = results 
        return context


class AliyunGroups(TemplateView):
    '''阿里云服务器的分组'''
    template_name = "assets/aliyun_groups.html"

    def get_context_data(self, **kwargs):
        context = super(AliyunGroups, self).get_context_data(**kwargs)
        groups = ServersGroup.objects.filter(server_type='aliyun')
        results = []
        num = 0
        for one in groups:
            results.append([])
            index = num/4
            all_count = ServersModel.objects.filter(server_group=one, server_from="aliyun").count()
            date_count = ServersModel.objects.filter(server_group=one, status_color='red',server_from="aliyun").count()
            results[index].append({'name': one.name, 'count': all_count, 'date_count': date_count})
        context['server_url'] = '/assets/add_group/'
        context['groups'] = results 
        return context


class AddGroup(View):
    '''添加分组'''

    #@control_permission(2)
    def get(self, request):
        try:
            name = request.GET.get('name', '')
            server_type = request.GET.get('server_type', 'aliyun')
            group = ServersGroup.objects.filter(name=name)
            if group:
                return HttpResponse(json.dumps('该名称已存在.'), content_type='application/json')
            else:
                group = ServersGroup.objects.create(name=name, server_type=server_type)
                content = '添加服务器分组,组名为:' + str(name)
                OperationModel.objects.create(pro=request.user.profile, user_name=request.user.profile.name, opt_type='操作记录', opt_content=content)
                group.save()
                return HttpResponse(json.dumps('成功!'), content_type='application/json')
        except Exception, e:
            logger.error(traceback.format_exc())
            return HttpResponse(json.dumps('失败,快去找万能的管理员吧!'), content_type='application/json')
            

class BatchGroup(View):

    def post(self, request):
        query_value = request.POST.get('query_value', '')
        name = request.POST.get('group_name', '')
        query_key = request.POST.get('query_key', '')
        if query_key == '实例名称':
            results = ServersModel.objects.filter(instance_name__contains=query_value)
        else:
            return HttpResponse(json.dumps('只支持根据实例名修改'), content_type='applications/json')
        group = ServersGroup.objects.get(name=name)
        for one in results:
            one.server_group = group
            one.save()
        return HttpResponse(json.dumps('成功!'), content_type='application/json')
        


class ChangeGroup(View):
    '''修改分组名称'''

    def get(self,request):
        name = request.GET.get('server_name', '')
        server_id = request.GET.get('server_id', '')
        if not name:
            return HttpResponse(json.dumps('fail, name error'), content_type='applicaton/json')
        else:
            try:
                if name != "None":
                    group = ServersGroup.objects.get(name=name)
                server = ServersModel.objects.get(instanceid=server_id)
                content = '修改服务器分组, 将服务器:'+ server.instance_name + ' 的分组,由' + str(server.server_group) + '改为' + str(group)
                OperationModel.objects.create(pro=self.request.user.profile, user_name=self.request.user.profile.name, opt_type='操作记录', opt_content=content)
                server.server_group = group
                server.save()
            except Exception, e:
                logger.error('修改服务器组名失败,服务器id:' + str(instance_id) + traceback.format_exc())
                return HttpResponse(json.dumps("修改失败"), content_type="application/json")
                print traceback.format_exc()

            return HttpResponse(json.dumps('修改完成!'), content_type='application/json')


class EmpList(TemplateView):
    '''内部资产：员工列表'''
    template_name = "assets/emp_infos.html"

    def get_context_data(self, **kwargs):
        context = super(EmpList, self).get_context_data(**kwargs)
        query_name = self.request.GET.get("query", "")
        department_name = self.request.GET.get("query_name", "")
        emp_status = self.request.GET.get('status', '')
        page_num = self.request.GET.get("page", 1)
        if department_name:
            department = Department.objects.get(name=department_name)
            emps = EmpLoyeeModel.objects.filter(department=department)
        else:
            emps = EmpLoyeeModel.objects.filter()
        if query_name:
            emps = emps.filter(name__contains=query_name)
        if emp_status and emp_status == 'False':
            emps = emps.filter(status=False)
        elif emp_status and emp_status == "True":
            emps = emps.filter(status=True)

        p = Paginator(emps, PER_PAGE_NUM)
        try:
            page = p.page(int(page_num))
        except:
            page = p.page(1)
        context["page"] = page
        context["department"] = department_name
        context["query"] = query_name
        return context


class AddDepartment(View):
    '''添加内部资产部门'''
    @control_permission(2)
    def get(self, request):
        name = request.GET.get('name', '')
        depart = Department.objects.filter(name=name)
        if depart:
            return HttpResponse(json.dumps('该部门名称已存在'), content_type='application/json')

        else:
            depart = Department.objects.create(name=name)
            depart.save()
            return HttpResponse(json.dumps('部门添加成功'), content_type='application/json')

class EmpDepartment(TemplateView):
    '''内部资产：按不同部门分组展示'''
    template_name = "assets/emp_department.html"

    def get_context_data(self, **kwargs):
        context = super(EmpDepartment, self).get_context_data(**kwargs)
        departs = Department.objects.all()
        department = []
        num = 0
        for one in departs:
            department.append([])
            index = num/4
            count = EmpLoyeeModel.objects.filter(department=one, status=True).count()
            over_count = EmpLoyeeModel.objects.filter(department=one,status=False).count()
            department[index].append({'name': one.name, 'count': count, 'over_count': over_count})

        emp_count = EmpLoyeeModel.objects.filter().count()
        over_count = EmpLoyeeModel.objects.filter(status=False).count()
        item_count = ItemList.objects.filter().count()
        item_return = ItemList.objects.filter(is_return=True).count()

        context["emp_info"] = {"emp_count": emp_count, "over_count": over_count}
        context["item_info"] = {"item_count": item_count, "item_return": item_return}
        context["departments"] = department
        return context


class CreateEmp(View):
    '''内部资产：创建员工资产列表'''
    
    def get(self, request):
        name = request.GET.get('name', '')
        department = request.GET.get("department", "")
        try:
            department = Department.objects.get(name=department)
            emp = EmpLoyeeModel.objects.create(name=name, department=department)
        except Exception, e:
            logger.error("create emp is:" + traceback.format_exc())
            return HttpResponse(json.dumps('error!'), content_type="application/json")
        
        return HttpResponse(json.dumps('success!'), content_type="application/json")


class EmpDetail(TemplateView):
    '''某个员工的详细物品单信息'''
    template_name = "assets/emp_detail.html"

    def get_context_data(self, **kwargs):
        context = super(EmpDetail, self).get_context_data(**kwargs)
        employee = self.request.GET.get("employee", "")
        query_value = self.request.GET.get("query_types", "")
        page_num = self.request.GET.get("page", 1)
        query_item_types = ["全部", '电脑整机', '电脑配件', '外设产品', '游戏设备', '网络产品', '办公设备', '数码设备', '其他类']
        if employee:
            employee = EmpLoyeeModel.objects.get(pk=employee)
            item_list = ItemList.objects.filter(employee=employee).order_by()
        else:
            item_list, query_item_types = utils.get_item(query_value, query_item_types)
            is_return = self.request.GET.get("is_return", '')
            if is_return == "True":
                item_list = item_list.filter(is_return=True)
        p = Paginator(item_list, PER_PAGE_NUM)
        try:
            page = p.page(int(page_num))
        except:
            page = p.page(1)

        context["page"] = page
        context["employee"] = employee
        context["query_item_types"] = query_item_types
        return context


class CreateItem(View):
    '''给物品单中添加出借物品详情'''
    
    def get(self, request):
        try:
            name = request.GET.get("name", "")
            item_type = request.GET.get("item_type", "")
            item_num = request.GET.get('item_num', "")
            note = request.GET.get("note", "")
            employee = request.GET.get("employee", "")
            employee = EmpLoyeeModel.objects.get(pk=int(employee))
            is_ex = ItemList.objects.filter(item_num=item_num)
            if is_ex:
                return HttpResponse(json.dumps('该编号已存在，请重新添加'), content_type='application/json')
            item = ItemList.objects.create(name=name, item_type=item_type, item_num=item_num, note=note, employee= employee)
            return HttpResponse(json.dumps("添加成功"), content_type="application/json")
        except Exception, e:
            logger.error("create item " + traceback.format_exc())                


class EmpDeparture(View):
    '''员工离职'''
    def get(self, request):
        try:
            empid = request.GET.get('empid', '')
            emp = EmpLoyeeModel.objects.get(pk=str(empid))
            items = ItemList.objects.filter(employee=emp)
            for one in items:
                if one.is_return == False:
                    return HttpResponse(json.dumps('离职失败，有物品未归还，请查看'), content_type="application/json")
            emp.status = False
            emp.save()
            return HttpResponse(json.dumps('成功'), content_type="application/json")
        except Exception, e:
            print traceback.format_exc()


class ItemReturn(View):
    '''内部资产： 归还物品'''

    def get(self, request):
        try:
            item_id = request.GET.get("item_id")
            item = ItemList.objects.get(pk=item_id)
            item.is_return = True
            item.return_time = time.strftime("%Y-%m-%d %H:%m:%S")
            item.save()
            return HttpResponse(json.dumps("归还成功"), content_type="application/json")
        except Exception, e:
            print traceback.format_exc()


class CreateAliyun(TemplateView):
    '''购买阿里云服务器'''
    template_name = "assets/create_instance.html"

    @control_permission_context(2)
    def get_context_data(self, **kwargs):
        context = super(CreateAliyun, self).get_context_data(**kwargs)
        images = ServerConf.objects.filter(server_type='aliyun', info_type='image')
        context["images"] = ServerConf.objects.filter(server_type='aliyun', info_type='image')
        context['instance_types'] = ServerConf.objects.filter(server_type='aliyun', info_type='server_type')
        context['io_instance_types'] = ServerConf.objects.filter(server_type='aliyun', info_type='io_server_type')
        return context

    @control_permission(2)
    def post(self, request):
        result = {}
        try:
            for key, value in request.POST.items():
                result.update({key: value})
            result.update({'passwd1': "XianLai@!2016"})# 统一默认密码，不再从页面输入。保留逻辑是怕产品改主意。
            passwd = result['passwd1']
            re_passwd = re.match(ur'(?=^.{8,30}$)(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?!\W+$).*$', passwd)
            if not re_passwd:
                return HttpResponse(json.dumps("失败,密码格式错误，请重新输入"), content_type="application/json")
            else:
                result.update({'Password': result['passwd1']})
            content = "购买阿里云服务器,参数见备注"
            memo = json.dumps(result)
            OperationModel.objects.create(pro=self.request.user.profile, user_name=self.request.user.profile.name, opt_type='购买记录', opt_content=content, memo=memo)
            result = aliyun_api.create_instance(result, server_group="未初始化")
        except Exception, e:
            print traceback.format_exc()
            logger.error(traceback.format_exc())
            result = "失败，请联系管理员"
        return HttpResponse(json.dumps(result), content_type="application/json")


class CreateAliyunTemplate(LoginRequiredMixin, ListView):
    model = AliyunTemplate
    context_object_name = 'template_list'
    template_name = 'assets/create_aliyun_template.html'


def create_template(request):
    try:
        tem_id = request.POST.get("server_id", '')
        return HttpResponse(json.dumps("暂未开通"), content_type-"application/json")
    except Exception as e:
        print traceback.format_exc()



class CreateQcloud(TemplateView):
    '''购买腾讯云服务器'''
    template_name = "assets/create_qcloud.html"
    
    @control_permission_context(2)
    def get_context_data(self, **kwargs):
        context = super(CreateQcloud, self).get_context_data(**kwargs)
        context["images"] = ServerConf.objects.filter(server_type='qcloud', info_type='image')
        context['g2'] = ServerConf.objects.filter(server_type='qcloud', info_type='zone_g2')
        context['g3'] = ServerConf.objects.filter(server_type='qcloud', info_type='zone_g3')
        context["s1"] = ServerConf.objects.filter(server_type='qcloud', info_type='zone_s1')
        context['b1'] = ServerConf.objects.filter(server_type='qcloud', info_type='zone_b1')
        context['x1'] = ServerConf.objects.filter(server_type="qcloud", info_type="zone_x1")
        return context

    @control_permission(2)
    def post(self, request):
        result = {}
        for key, value in request.POST.items():
            result.update({key: value})
        try:
            result.update({'passwd1': "XianLai@!2016"})# 统一默认密码，不再从页面输入。保留逻辑是怕产品改主意。
            content = "购买腾讯云服务器,参数见备注"
            memo = json.dumps(result)
            OperationModel.objects.create(pro=self.request.user.profile, user_name=self.request.user.profile.name, opt_type='购买记录', opt_content=content, memo=memo)
            print 11111,result
            #result = create_qcloud(result)
        except Exception, e:
            result = "程序出错啦，快联系管理员吧"
            print traceback.format_exc()
        return HttpResponse(json.dumps(result), content_type="application/json")


class RdsType(LoginRequiredMixin, TemplateView):
    template_name = 'assets/rds_type.html'
    '''获取云平台的数据库信息'''
    def get_context_data(self, **kwargs):
        context = super(RdsType, self).get_context_data(**kwargs)
        qrds = RdsModel.objects.filter(server_type='qcloud')
        ards = RdsModel.objects.filter(server_type='aliyun')
        context['qrds'] = qrds
        context['ards'] = ards
        return context


class RdsDetail(LoginRequiredMixin, DetailView):
    '''服务器详情页面'''
    model = RdsModel
    context_object_name = 'rds_info'
    template_name = 'assets/rds_detail.html'


class CreateRds(TemplateView):
    """购买数据库"""
    template_name = 'assets/create_rds.html'
    @control_permission_context(2)
    def get_context_data(self, **kwargs):
        context = super(CreateRds, self).get_context_data(**kwargs)
        context['zone'] = ServerConf.objects.filter(server_type='qcloud', info_type='zone')
        context["aliyun_zone"] = ServerConf.objects.filter(server_type='aliyun', info_type='zone')
        context['aliyun_class'] = ServerConf.objects.filter(server_type='aliyun', info_type='rds_class')
        return context

    @control_permission(2)
    def post(self, request):
        server_type = request.POST.get('server_type', '')
        if server_type == 'qcloud':
            months = request.POST.get('qcloud_months', '')
            num = request.POST.get('qcloud_num', '')
            mem = request.POST.get('mem', '')
            volume = request.POST.get('volume', '')
            zone = request.POST.get('zone', '')
            content = "购买腾讯云数据库,参数见备注"
            memo = json.dumps({'months': months, 'num': num, 'mem': mem, 'volume':volume, 'zone': zone})
            OperationModel.objects.create(pro=self.request.user.profile, user_name=self.request.user.profile.name, opt_type='购买记录', opt_content=content, memo=memo)
            result = create_qcloud_rds(months, num, mem, volume, zone)
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            zone = request.POST.get("zone", '')
            db_class = request.POST.get("db_class", '')
            db_storage = request.POST.get("aliyun_storage", '')
            net_type = request.POST.get("net_type", '')
            months = request.POST.get("aliyun_months", '')
            num = request.POST.get('aliyun_num', '')
            ip_list = request.POST.get('ip_list', '')
            pay_type = request.POST.get('PayType', '')
            content = "购买阿里云数据库,参数见备注"
            memo = json.dumps({'months': months, 'num': num, 'db_class':db_class, 'zone': zone, 
                'db_storage': db_storage, 'ip_list': ip_list, 'net_type': net_type})
            OperationModel.objects.create(pro=self.request.user.profile, user_name=self.request.user.profile.name, opt_type='购买记录', opt_content=content, memo=memo)
            result = aliyun_api.create_rds(pay_type, zone, db_class, db_storage, net_type, months, num, ip_list)
            return HttpResponse(json.dumps(result), content_type="application/json")


def check_date(request):
    try:
        try:
            aliyun_api.check_dns()
        except Exception as e:
            send_alarm('检查域名过期失败', phone='18513950766')

        servers = ServersModel.objects.all()
        rds = RdsModel.objects.all()
        for one in servers:
            if one.status_color == 'red' and '不续费' not in one.instance_name:
                for _ in range(2):
                    send_alarm("大事不好啦!名为" + one.instance_name + ', ID 为:' + one.instanceid + '的' + one.server_from + '服务器还有十五天就到期了,赶快续费吧!')
        for one in rds:
            if one.status_color == 'red' and '不续费' not in one.instance_name:
                for _ in range(2):
                    send_alarm("大事不好啦!名为" + one.instance_name + ', ID 为:' + one.instanceid + '的' + one.server_type + '数据库还有十五天就到期了,赶快续费吧!')
        return HttpResponse(json.dumps('检查完成'), content_type='application/json')
    except Exception, e:
        logger.error('check data error: : : ' + traceback.format_exc())
        send_alarm('检查服务器过期失败', phone='18513950766')


class CreateProject(LoginRequiredMixin, TemplateView):
    """创建整个项目"""
    template_name = "assets/create_project.html"
    def get_context_data(self, **kwargs):
        context = super(CreateProject, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", '')
        instance_type = self.request.GET.get('type', '')
        templates = AliyunTemplate.objects.filter(tem_type=instance_type)
        context['instance_type'] = instance_type
        context['name'] = name
        context['templates'] = templates
        return context

    def post(self, request):
        try:
            server_type = request.POST.get('instance_type', '')
            templates = AliyunTemplate.objects.filter(tem_type=server_type)

            if server_type == "aliyun":
                servers = {}
                for key, value in request.POST.items():
                    servers.update({key: value})

                ori_name = request.POST.get('name', "")
                ori_name = ori_name.strip(' ')
                success_num = 0
                for one in templates:
                    try:
                        server_num = int(servers[one.name])
                    except Exception as e:
                        return HttpResponse(json.dumps('失败，台数请输入数字'), content_type="application/json")
                    for n in range(server_num):
                        n += 1
                        name = ori_name + one.name
                        name = name[:-1] + str(n)

                        param = {'Password': 'XianLai@!2016', 'passwd1': 'XianLai@!2016', u'Description': u'', u'change_instance_type': u'instanceType', u'many_servers': u'',
                             u'SecurityGroupId': u'sg-236rhp1p5', u'InstanceChargeType': u'PostPaid', u'no_InstanceType': u'ecs.s2.small', u'Period': u'1', u'InternetMaxBandwidthOut': u'100',
                             u'num': u'1', u'DataDisk.1.Size': u'', u'SystemDisk.Size': u'100', u'InternetChargeType': u'PayByTraffic', u'csrfmiddlewaretoken': u'pLwm7ilVppqSU9pFQYFD4v2Cvv0xANKk',
                             u'ZoneId': u'cn-hangzhou-c', u'InstanceName': u'InstanceName',u'io_InstanceType': u'ecs.n1.medium', u'ImageId': u'm-bp1iakpxgd7f1uyt0oo2'}
                        instance_type =  str(one.cpu) + '核' + str(one.mem) + "G"
                        instance_type = ServerConf.objects.get(info_type="server_type", value=instance_type)
                        param.update({"InstanceName": name, "no_InstanceType": instance_type.key})
                        result = "成功"
                        result = aliyun_api.create_instance(param, server_group="未初始化")
                        if '成功' in result:
                            success_num += 1
                return HttpResponse(json.dumps('创建成功' + str(success_num) + '台机器'), content_type="application/json")
            else:
                success_num = 0
                for one in templates:
                    param = {u'region_b1': u'1-1', u'region_x1': u'2-2', u'goodsNum': u'1', u'rootSize': u'20', u'period': u'1', u'imageId': u'img-7fwdvfur', u'bandwidth': u'100',
                        u'region_s1': '', u'change_region_cvm': u'200001', u'region_g3': u'1-1', u'region_g2': u'1-1', u'csrfmiddlewaretoken': u'9k3t3ORr0bVo42pMGF2Jht1QeaysnPci',
                        u'storageSize': u'100', 'passwd1': 'XianLai@!2016', u'bandwidthType': u'PayByTraffic'}
                    param.update({"region_s1": str(one.cpu) + '-' + str(one.mem)})
                    result = create_qcloud(param)
                    if "成功" in result:
                        success_num += 1
                return HttpResponse(json.dumps('创建成功' + str(success_num) + '台机器'), content_type="application/json")

        except Exception as e:
            logger.error('创建项目失败:, 原因:' + traceback.format_exc())
            print '创建项目失败:, 原因:' + traceback.format_exc()
            return HttpResponse(json.dumps('失败了,找管理员查查吧'), content_type='application/json')


class Online(LoginRequiredMixin, View):
    def get(self, request):
        server_id = request.GET.get('server_id', '')
        try:
            server = ServersModel.objects.get(pk=server_id)
        except Exception as e:
            return HttpResponse(json.dumps("该服务器不存在"), content_type="applications/json")
        server.mem = ""
        server.save()
        return HttpResponse(json.dumps("修改完成"), content_type="applications/json")   
