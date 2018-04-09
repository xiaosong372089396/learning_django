# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.views.generic import View, ListView, DetailView, TemplateView
from django.http import JsonResponse, QueryDict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
import inception
from django.shortcuts import render
from .models import *

'''
class inception_commit(TemplateView):
    template_name = 'sqlmng/inception_commit.html'
    def post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        print webdata
        inception.table_structure(webdata['sqlcontent'])
        return JsonResponse({'status':0})
'''

@method_decorator(login_required, name='dispatch')
class inception_commit(TemplateView):
    template_name = 'sqlmng/inception_commit.html'
    model = dbconf
    def post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        username = request.user.get_username()
        print webdata, 111
        # inception.table_structure(webdata['sqlcontent'])
        # 通过前端的数据 dbname, env, sqlcontent, note，拼接目标地址
        # --user=root;--password=123456;--host=192.168.1.233;--port=3306
        obj = self.model.objects.get(name=webdata.get('dbname'))
        dbaddr = '--user=%s; --password=%s; --host=%s; --port=%s; --enable-check;' % (obj.user, obj.password, obj.host, obj.port)
        sql_review = inception.table_structure(dbaddr, obj.name, webdata['sqlcontent'])
        for perrz in sql_review:
            if perrz[4] != 'None':
                return JsonResponse({'status': -2, 'msg': perrz[4]})
        # check通过的sql，保存
        userobj = request.user
        webdata['commiter'] = username
        # webdata['treater'] = username
        sqlobj = InceptSql.objects.create(**webdata)
        treaterobj = User.objects.get_or_create(username=webdata['treater'])[0]
        sqlobj.sqlusers.add(userobj, treaterobj)  # 提交人,执行人
        print sql_review     # 审核通过后，最后CHECK检测所有结果
        return JsonResponse({'status': 0})





'''
class dbconfig(View):
    model = dbconf
    template_name = 'sqlmng/dbconfig.html'
    def get(self,request, **kwargs):
        return render(request, self.template_name )

    def post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        name = webdata.get('name')
        env = webdata.get('env')
        dbqs = self.model.objects.filter(name=name, env=env)
        if dbqs:
            return JsonResponse({'status': -1})
        self.model.objects.create(**webdata)
        return JsonResponse({'status':0})


'''

class dbconfig(ListView):
    model = dbconf
    template_name = 'sqlmng/dbconfig.html'
    paginate_by = 5
    context_object_name = 'res_data'

    def get_queryset(self):
        qs = self.model.objects.all()
        souword = self.request.GET.get('souword')
        if souword:
            qs = qs.filter(name__contains=souword)
        return qs

    def post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        name = webdata.get('name')
        env = webdata.get('env')
        # 判断name env 的数据是不重复的
        dbqs = self.model.objects.filter(name=name, env=env)
        if dbqs:
            return JsonResponse({'status': -1})
        self.model.objects.create(**webdata)
        return JsonResponse({'status': 0})

    def put(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        pk = kwargs.get('pk')
        print webdata, pk
        self.model.objects.filter(id=pk).update(**webdata)
        return JsonResponse({'status': 0})

    def delete(self, request, **kwargs):
        pk = kwargs.get('pk')
        self.model.objects.get(pk=pk).delete()
        return JsonResponse({'status': 0})


class autoselect(View):
    def post(self, request):
        webdata = QueryDict(request.body).dict()
        env = webdata.get('env')
        dbs = [obj.name for obj in dbconf.objects.filter(env=env)]
        # 根据环境和用户角色 ：返回执行人和数据库
        # 根据用户的身份，返回执行人数据：研发 返回他的经理，经理以上 返回自己的数据
        userobj = request.user
        if userobj.is_superuser:
            mngs = [userobj.username]
            return JsonResponse({'status': 0, 'dbs': dbs, 'mngs': mngs})
        role = userobj.userprofile.role
        if env == '1':
            if role == '3':
                # 获取所在group的经理名单
                ug = userobj.groups.first()
                if not ug:
                    mngs = []
                else:
                    mngs = [u.username for u in ug.user_set.all() if u.userprofile.role == '2']
                print mngs
            else:
                mngs = [userobj.username]
        else:
            mngs = [userobj.username]
        return JsonResponse({'status': 0, 'dbs': dbs, 'mngs': mngs})


class inception_result(ListView):
    template_name = 'sqlmng/inception_result.html'
    paginate_by = 10
    model = InceptSql
    dbmodel = dbconf
    context_object_name = 'res_data'

    def get_queryset(self):
        # 根据用户身份，返回和他有关系的sql
        userobj = self.request.user
        if userobj.is_superuser:
            return userobj.inceptsql_set.all()
        role = userobj.userprofile.role
        if role == '1':  # 总监，返回他组内的所有人的sql
            qs = userobj.inceptsql_set.all()
            g = userobj.groups.first()
            for u in g.user_set.all():
                sqlret = u.inceptsql_set.all()
                qs = qs | sqlret
        else:  # 研发或经理
            qs = userobj.inceptsql_set.all()
        return qs

    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        actiontype = kwargs.get('actiontype')
        sqlobj = self.model.objects.get(pk=pk)
        ret = {'status': 0}
        if actiontype == 'execute':
            # 根据id获取sql的内容，执行
            sqlcontent = sqlobj.sqlcontent
            dbobj = self.dbmodel.objects.get(name=sqlobj.dbname)
            dbaddr = '--user=%s; --password=%s; --host=%s; --port=%s; --enable-execute' % (
            dbobj.user, dbobj.password, dbobj.host, dbobj.port)
            exerz = inception.table_structure(dbaddr, dbobj.name, sqlcontent)  # 在这一步，已经执行完了
            print exerz
            affected_rows = 0
            exe_time = 0
            opidlist = []
            for i in exerz:  # 分析执行完的结果
                successcode = i[4]
                if successcode != 'None':  # 执行失败的
                    sqlobj.status = 2
                    ret['status'] = -1
                    break
                else:
                    opidlist.append(i[7])
                    affected_rows += i[6]
                    exe_time += float(i[9])
                    sqlobj.rollbackdb = i[8]
                    sqlobj.status = 0
                    ret['status'] = 0
            sqlobj.rollbackopid = opidlist
        elif actiontype == 'rollback':
            rollbackopid = sqlobj.rollbackopid  # 获取sql的回滚id集合
            rollbackdb = sqlobj.rollbackdb      # 取出回滚库名
            # 后期更改获取数据库环境，匹配地址
            # env = sqlobj.env

            # 根据选择的数据环境，匹配地址
            # dbobj = dbconf.objects.filter(name=dbname, env=env)
            # pc = prpcrypt(crykey)
            # dbpasspwd = pc.decrypt(dbobj.password)
            # end

            # 第一步：拼接获取回滚语句
            backsqls = ''
            for opid in eval(rollbackopid)[1:]:  # 遍历回滚id，拼接回滚语句
                # 对每个回滚id，在$_$Inception_backup_information$_$里获取它的操作的表
                sql = 'select tablename from $_$Inception_backup_information$_$ where opid_time = %s' % (opid)
                baktable = inception.getbak(sql, rollbackdb)[0][0]
                # 每个回滚id获取到的回滚语句（可能是多条）
                rollbacksql = 'select rollback_statement from %s where opid_time = %s' % (baktable, opid)
                perback = inception.getbak(rollbacksql, rollbackdb)  # 每条语句的回滚结果
                '''
                    (( u'DELETE FROM `inc_test2`.`mytable1` WHERE id=38; ',),)
                '''
                #3. 循环回滚语句集合，拼接成一个字符串
                for baksql in perback:  # 对可能多条的回滚语句，取出每一个
                    backsqls += baksql[0]
            print backsqls  #
            '''
              DELETE FROM `inc_test`.`mytable1` WHERE id=12534;DELETE FROM `inc_test`.`mytable1` WHERE id=12535;DELETE FROM `inc_test`.`mytable1` WHERE id=12536;DELETE FROM `inc_test`.`mytable1` WHERE id=12537;DELETE FROM `inc_test`.`mytable1` WHERE id=12538;

            '''
            #  第二步：执行回滚语句
            dbobj = self.dbmodel.objects.get(name=sqlobj.dbname)
            dbaddr = '--user=%s; --password=%s; --host=%s; --port=%s; --enable-execute' % (
            dbobj.user, dbobj.password, dbobj.host, dbobj.port)
            exerz = inception.table_structure(dbaddr, dbobj.name, backsqls)
            # 后期更改更改回滚状态显示
            # sqlobj.status = -3
            # roll_affected_rows = len(exerz) - 1
            # dbobj.roll_affected_rows = roll_affected_rows
            # ret['rollnum'] = roll_affected_rows    # 执行回滚语句的结果，除去第一个USE 数据库的
            # if username != dbobj.treater:
            #     note = dbobj.note + '   [' + username + '代回滚']'
            #     dbobj.note = note

            print exerz
        sqlobj.save()
        return JsonResponse(ret)
