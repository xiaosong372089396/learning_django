/**
 * Created by zengchunyun on 16/8/12.
 */

define(function (require, exports, module) {
    var Backbone = require('backbone');

    var MonitorCollection = Backbone.Collection.extend({
        initialize: function (options) {
            //默认分页数据从第一页开始
            this.page = 1;
            //默认可以获取到数据
            this.canFetch = true;
            //默认重置状态为true
            this.reseted = true;
            this.monitor_type = options.type;
            this.model = options.model;
            this.parseData = options.parseData;
        },

        parse: function (response) {
            if(response.status == true){
                //判断是否还有数据可以取回
                this.canFetch = response.has_next;
                if(this.canFetch){
                    this.addPage();
                }
                if(response.info && response.info != "") {
                    swal({   title: response.info, type: response.category,   timer: 1500,   showConfirmButton: false });
                }

            }else {
                swal({   title: response.info, type: response.category,   timer: 1500,   showConfirmButton: false });
            }
            $("#loading").fadeOut("slow");
            if(typeof response.data != "undefined"){
                return response.data
            }else {
                return response;
            }
        },
        resetCollection: function () {
            this.page = 1;
            this.canFetch = true;
            this.reseted = true;
        },
        addPage: function () {
            this.page += 1;
        },
        fetchData: function (reset, form_data, self,method) {
             if(reset){
                this.resetCollection();
            }else {
                 this.reseted = false;
            }
            var requestData = {page: this.page, type: this.monitor_type};
            for(var key in form_data){
                requestData[key] = form_data[key];
            }
            if(this.canFetch || reset || !this.reseted){
                if(self){
                    var args = "";
                    var func = function () {};
                    //当第三个参数为方法时，将func替换为该函数，将第四个参数当成参数传给该方法
                    //当第三个参数为对象时，那么判断第四个对象是不是属于该对象的方法，是就将该参数赋值给func，同时将该对象当成参数执行时传给func
                    if(typeof self == "function"){
                        func = self;
                        args = method;
                    }else if(typeof self == "object"){
                        for(var attr in self){
                            if(self[attr] == method){
                                func = typeof self[attr] == "function" ? self[attr]: func;
                                args = self;
                                break;
                            }
                        }
                    }
                    this.fetch({
                        data: requestData,
                        reset: true,
                        success: function (collection, response, options) {
                            func(args, collection, response, options);
                        },
                        error:function (xhr, textStatus, errorThrown) {
                            $("#loading").fadeOut("slow");
                            swal({   title: "内部请求错误！", type: 'error',   timer: 5500,   showConfirmButton: true });
                        },
                        beforeSend:function (callbackContext, jqXHR) {
                            $("#loading").show();
                            console.log('callbackContext', callbackContext);
                            console.log('jqXHR', jqXHR);
                        }
                    });
                }else {
                    this.fetch({
                        data: requestData,
                        reset: true,
                        success: function (collection, response, options) {

                        },
                        error: function (xhr, textStatus, errorThrown) {
                            $("#loading").fadeOut("slow");
                            swal({   title: "内部请求错误！", type: 'error',   timer: 5500,   showConfirmButton: true });
                        },
                        beforeSend:function (callbackContext, jqXHR) {
                            $("#loading").show();
                            console.log('callbackContext', callbackContext);
                            console.log('jqXHR', jqXHR)
                        }
                    });
                }
            }else {
                $("#loading").fadeOut("slow");
            }
        }
    });

    return MonitorCollection;

});