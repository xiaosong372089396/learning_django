#_coding:utf-8_*_
from django.shortcuts import render,HttpResponseRedirect, HttpResponse
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View, ListView, TemplateView
from zabbix.core import Zabbix
from zabbix import models

zabbixapi = Zabbix()


class Index(TemplateView):

    template_name = 'zabbix/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context


class Hostlist(TemplateView):

    template_name = 'zabbix/hostlist.html'

    def get_context_data(self, **kwargs):
        context = super(Hostlist, self).get_context_data(**kwargs)
        context['request'] = self.request
        host = models.Hosts.objects.all()
        group = models.Groups.objects.all()
        template = models.Templates.objects.all()
        proxy = models.Proxy.objects.all()
        limit = 10
        paginator = Paginator(host, limit)
        page = self.request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        context['contacts'] = contacts
        context['group'] = group
        context['template'] = template
        context['proxy'] = proxy
        return context


class CreateHost(View):

    def post(self, request):
        return HttpResponse('不接受post请求')

    def get(self, request):
        host = request.GET.get('host', '')
        ip = request.GET.get('ip', '')
        groupid = request.GET.get('groupid', '')
        templateid = request.GET.get('templateid', '')
        proxyid = request.GET.get('proxyid', '')
        res = zabbixapi.createhost(host=host, ip=ip, groupid=groupid, templateid=templateid, proxyid=proxyid)
        return JsonResponse(res,safe=False)


class Grouplist(TemplateView):

    template_name = 'zabbix/grouplist.html'

    def get_context_data(self, **kwargs):
        context = super(Grouplist, self).get_context_data(**kwargs)
        context['request'] = self.request
        group = models.Groups.objects.all()
        limit = 10
        paginator = Paginator(group, limit)
        page = self.request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        context['contacts'] = contacts
        return context

class CreateGroup(View):

    def post(self, request):
        return HttpResponse('不接受post请求')

    def get(self, request):
        groupname = request.GET.get('groupname', '')
        res = zabbixapi.creategroup(groupname=groupname)
        return JsonResponse(res,safe=False)


class Templateist(TemplateView):

    template_name = 'zabbix/templatelist.html'

    def get_context_data(self, **kwargs):
        context = super(Templateist, self).get_context_data(**kwargs)
        context['request'] = self.request
        template = models.Templates.objects.all()
        limit = 10
        paginator = Paginator(template, limit)
        page = self.request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        context['contacts'] = contacts
        return context


class ItemLlist(TemplateView):

    template_name = 'zabbix/itemlist.html'

    def get_context_data(self, **kwargs):
        context = super(ItemLlist, self).get_context_data(**kwargs)
        context['request'] = self.request
        host = models.Hosts.objects.all()
        context['host'] = host
        hostid = self.request.GET.get('hostid','')
        item = zabbixapi.select_item(hostid=hostid)
        itemurl = "http://127.0.0.1:8001/chart.php"
        context['item'] = item
        context['itemurl'] = itemurl
        return context

class Graphlist(TemplateView):

    template_name = 'zabbix/graphlist.html'

    def get_context_data(self, **kwargs):
        context = super(Graphlist, self).get_context_data(**kwargs)
        context['request'] = self.request
        host = models.Hosts.objects.all()
        context['host'] = host
        hostid = self.request.GET.get('hostid', '')
        graph = zabbixapi.select_graph(hostid=hostid)
        graphurl = "http://127.0.0.1:8001/chart2.php"
        context['graph'] = graph
        context['graphurl'] = graphurl
        return context


class Triggerlist(TemplateView):
    pass


class Historylist(TemplateView):

    template_name = 'zabbix/history.html'

    def get_context_data(self, **kwargs):
        context = super(Historylist, self).get_context_data(**kwargs)
        context['request'] = self.request
        itemid = self.request.GET.get('itemid', '')
        data_type = self.request.GET.get('data_type', '0')
        value, clock, item, host = zabbixapi.select_history(itemid=itemid,data_type=data_type)
        context['value'] = value
        context['clock'] = clock
        context['item'] = item
        context['host'] = host
        return context