#-*-coding:utf-8-*-
from django.conf.urls import url,include
from django.contrib.auth.decorators import login_required
from assets import views

urlpatterns = [
    url(r'server_list/$', login_required(views.ServerList.as_view())),
    url(r'qcloud_list/$', login_required(views.QcloudServers.as_view()), name="one"),
    url(r'server_detail/$', login_required(views.ServerDetail.as_view())),
    url(r'update_data/$', views.update_data),
    url(r'update_qcloud/$', views.update_qcloud),
    url(r'update_rds/$', views.update_rds),
    url(r'reboot/$', login_required(views.ServerReboot.as_view())),
    url(r'start/$', login_required(views.ServerStart.as_view())),
    url(r'stop/$', login_required(views.ServerStop.as_view())),
    url(r'server_change_name/$', login_required(views.ServerChangeName.as_view())),
    #url(r'server_groups/$', login_required(views.ServerGroups.as_view())),
    url(r'server_type/$', login_required(views.ServerType.as_view())),
    url(r'aliyun_groups/$', login_required(views.AliyunGroups.as_view())),
    url(r'qcloud_groups/$', views.QcloudGroups.as_view()),
    url(r'add_group/$', login_required(views.AddGroup.as_view())),
    url(r'change_group/$', login_required(views.ChangeGroup.as_view())),
    url(r'create_aliyun_template/$', views.CreateAliyunTemplate.as_view()),
    url(r'create_template/$', views.create_template),

    url(r'online/$', views.Online.as_view()),
    url(r'rds_type/$', views.RdsType.as_view()),
    url(r'rds_detail/(?P<pk>[0-9]+)/$', views.RdsDetail.as_view()),
    url(r'create_rds/$', login_required(views.CreateRds.as_view())),
    url(r'batch_group/$', views.BatchGroup.as_view()),
    url(r'check_date/$', views.check_date),
    url(r'create_project/$', views.CreateProject.as_view()),

    url(r'emp_department/$', login_required(views.EmpDepartment.as_view())),
    url(r'add_department/$', login_required(views.AddDepartment.as_view())),
    url(r'emp_list/$', login_required(views.EmpList.as_view())),
    url(r'create_emp/$', login_required(views.CreateEmp.as_view())),
    url(r'emp_detail/$', login_required(views.EmpDetail.as_view())),
    url(r'create_item_detail/$', login_required(views.CreateItem.as_view())),
    url(r'item_return/$', login_required(views.ItemReturn.as_view())),
    url(r'create_aliyun/$', login_required(views.CreateAliyun.as_view())),
    url(r'create_qcloud/$', login_required(views.CreateQcloud.as_view())),
    url(r'emp_departrue/$', login_required(views.EmpDeparture.as_view())),
]
