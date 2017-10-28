/**
 * Created by liuyao
 */
require.config({
    baseUrl: "/static/monitor/js/afca/",
    shim: {
      'underscore': {
          exports: '_'
      },
      'backbone': {
          deps: ['underscore', 'jquery'],
          exports: 'Backbone'
      },
        "jquery.cookies": {
          deps: ["jquery"]
        },
      "slimScroll": {
          deps: ['jquery']
      },
       "jvectormap": {
          deps: ['jquery']
      },
        "bootstrap": {
          deps: ["jquery"],
          exports: 'jquery'
        },
        "bootstrap_table": {
          deps: ["bootstrap"],
          exports: 'jquery'
        },
        "bootstrap_table_locale": {
          deps: ["bootstrap_table"],
          exports: 'jquery'
        },
        "datetimepicker": {
            deps: ["bootstrap"]
        },
        "daterangepicker": {
          deps: ["jquery","moment"]
        },
       "jvectormap-world": {
          deps: ['jquery', "jvectormap"]
      },
       "bootstrap-slider": {
          deps: ["bootstrap"]
       },
       "bootstrap-wysihtml5": {
           deps: ["bootstrap"]
       },
        "bootstrap_switch": {
           deps: ["jquery"]
        },
        "app": {
           deps: ["jquery", "bootstrap"]
        },
        "demo": {
            deps: ["app"]
        },
        "dashboard": {
            deps: ["demo", "chartjs", "fastclick", "sparkline", "jvectormap", "jvectormap-world", "slimScroll"]
        },
        "echarts": {
            exports: "echarts"
        },
        "datatables" :{
            deps: ["bootstrap", "jquery.datatable"]
        },
        "tableExport":{
            deps:["jquery"]
        },
        "jquery.base64":{
          deps: ["tableExport"]
        },
        "html2canvas": {
          deps:["jquery.base64"]
        },
        "sprintf":{
          deps:["html2canvas"]
        },
        "jspdf":{
            deps:["sprintf"]
        },
        "base64":{
            deps: ["jspdf"]
        },
        "jqueryui":{
            deps: ["jquery"]
        }
    },
    paths: {
        "underscore": "require-module/libs/underscore/1.8.3/underscore-min",
        "backbone": "require-module/libs/backbone/1.3.3/backbone-min",
        "bootstrap": "require-module/libs/bootstrap/js/bootstrap.min",
        "bootstrap_table": "require-module/afca/bootstrap-table/bootstrap-table",
        "bootstrap_table_locale": "require-module/afca/bootstrap-table/locale/bootstrap-table-zh-CN",
        "bootstrap_switch": "require-module/afca/bootstrap-switch/dist/js/bootstrap-switch.min",
        "bootstrap-wysihtml5": "require-module/afca/bootstrap-wysihtml5/bootstrap3-wysihtml5.all",
        "bootstrap-slider": "require-module/afca/bootstrap-slider/bootstrap-slider",
        "chartjs": "require-module/afca/chartjs/Chart.min",
        "domReady": "require-module/requirejs/domReady",
        "daterangepicker":"require-module/afca/daterangepicker/daterangepicker",
        "datetimepicker": "/static/monitor/js/afca/require-module/afca/bootstrap-datetimepicker/js/bootstrap-datetimepicker.min",
        "datatables": "require-module/afca/datatables/dataTables.bootstrap.min",
        "echarts": "require-module/afca/echarts/echarts.min",
        "fastclick": "require-module/afca/fastclick/fastclick",
        "jquery": "require-module/libs/jquery/1.12.4/jquery-min",
        "jquery.datatable": "require-module/afca/datatables/jquery.dataTables.min",
        "jvectormap": "require-module/afca/jvectormap/jquery-jvectormap-1.2.2.min",
        "jvectormap-world": "require-module/afca/jvectormap/jquery-jvectormap-world-mill-en",
        "jquery.cookies": "require-module/afca/jquery-cookie/jquery.cookie",
        "moment":"require-module/afca/daterangepicker/moment",
        "slimScroll": "require-module/afca/slimScroll/jquery.slimscroll",
        "sweetalert":"require-module/afca/sweetalert/sweetalert.min",
        "sparkline": "require-module/afca/sparkline/jquery.sparkline",
        "text": "require-module/requirejs/text",

        "tableExport":"require-module/afca/jquery-tableExport/tableExport",
        "jquery.base64":"require-module/afca/jquery-tableExport/jquery.base64",
        "html2canvas":"require-module/afca/jquery-tableExport/html2canvas",
        "sprintf":"require-module/afca/jquery-tableExport/jspdf/libs/sprintf",
        "jspdf":"require-module/afca/jquery-tableExport/jspdf/jspdf",
        "base64":"require-module/afca/jquery-tableExport/jspdf/libs/base64",
        "jqueryui": "require-module/afca/jQueryUI/js/jquery-ui.min",

        "app": "/static/monitor/js/afca/src/frontpage/app",
        "demo": "/static/monitor/js/afca/src/frontpage/demo",
        "dashboard": "/static/monitor/js/afca/src/frontpage/dashboard2",
        "common": "src/common/common"
    }
});
