/**
 * Created by zengchunyun on 16/8/12.
 */

define(function (require, exports, module) {
    var $ = require('jquery');
    //启动app入口点


    //导入主机组模型
    var MonitorModel = require('../models/monitor/monitor_model');

    //导入集合
    var MonitorCollection = require('../collections/monitor/monitor_collection');


    //监控首页app
    var DashboardApp = function (element, options) {
        options.model = MonitorModel.CommonModel;
        var monitorCollection = new MonitorCollection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/monitor/monitor_index_list_view'], function (MonitorView) {
            var monitorView = new MonitorView({
                el: $(element),
                collection: monitorCollection,
                url: options.url,
                options: options
            });
        });
    };


    //实例化APP, 主机组搜索app
    var HostGroupsApp = function (element, options) {
        options.model = MonitorModel.GroupsModel;
        var monitorCollection = new MonitorCollection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/monitor/monitor_groups_list_view'], function (MonitorView) {
            var monitorView = new MonitorView({
                el: $(element),
                collection: monitorCollection,
                url: options.url,
                options: options
            });
        });
    };

    //具体主机app
    var HostInfoApp = function (element, options) {
        options.model = MonitorModel.CommonModel;
        var monitorCollection = new MonitorCollection(options);
        require(['../views/monitor/monitor_host_list_view'], function (MonitorView) {
            var monitorView = new MonitorView({
                el: $(element),
                collection: monitorCollection,
                url: options.url,
                options: options
            });
        });
    };

    //告警页面app
    var EventApp = function (element, options) {
        options.model = MonitorModel.CommonModel;
        var monitorCollection = new MonitorCollection(options);
        require(['../views/monitor/monitor_event_list_view'], function (MonitorView) {
            var monitorView = new MonitorView({
                el: $(element),
                collection: monitorCollection,
                url: options.url,
                options: options
            });
        })
    };

    //配置主机组app
    var ConfigHostGroupsApp = function (element, options) {
        options.model = MonitorModel.CommonModel;
        var monitorCollection = new MonitorCollection(options);
        require(['../views/monitor/monitor_config_host_groups_list_view'], function (MonitorHostView) {
            var monitorView = new MonitorHostView({
                el: $(element),
                collection: monitorCollection,
                url: options.url,
                options: options
            });
        })
    };

    //配置主机组app
    var ConfigHostApp = function (element, options) {
        options.model = MonitorModel.CommonModel;
        var monitorCollection = new MonitorCollection(options);
        require(['../views/monitor/monitor_config_host_list_view'], function (MonitorHostView) {
            var monitorView = new MonitorHostView({
                el: $(element),
                collection: monitorCollection,
                url: options.url,
                options: options
            });
        })
    };

     //实例化APP, 默认报表app
    var ReportDefaultApp = function (element, options) {
        options.model = MonitorModel.CommonModel;
        var monitorCollection = new MonitorCollection(options);
        //导入视图,这种方式引入方式可以避免其它地方因为没有依赖而被加载进来
        require(['../views/monitor/monitor_report_default_list_view'], function (MonitorView) {
            var monitorView = new MonitorView({
                el: $(element),
                collection: monitorCollection,
                url: options.url,
                options: options
            });
        });
    };

    return {
        triggerDashboardApp: DashboardApp,
        triggerHostGroupsApp: HostGroupsApp,
        triggerHostInfoApp: HostInfoApp,
        triggerEventApp: EventApp,
        triggerConfigHostGroupsApp: ConfigHostGroupsApp,
        triggerConfigHostApp: ConfigHostApp,
        triggerReportDefaultApp: ReportDefaultApp
    };
});