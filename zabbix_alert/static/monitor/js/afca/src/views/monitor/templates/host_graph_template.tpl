<div class="col-md-12">
    <div class="box box-info">
        <div class="box-header with-border">
            <h5><%= name %></h5>
            <div class="box-tools pull-right">
                <input name="switch_status" type="checkbox" checked />
                <button type="button" class="btn btn-box-tool" data-widget="collapse"><i class="fa fa-minus"></i></button>
            </div>
            <div class="col-md-6">
                <div class="input-group">
                    <div class="input-group-addon">
                        <i class="fa fa-clock-o"></i>
                    </div>
                    <input type="text" name="history" class="form-control pull-right" id="history<%= graph_id %>">
                </div>
            </div>
        </div>
        <div class="box-body">
            <div id="<%= graph_id %>" style="height:300px;" class="col-md-12 col-sm-12"></div>
        </div>
    </div>
</div>

<script type="text/javascript">
    require(['echarts', 'jquery',"daterangepicker"], function (echarts, $) {
        var myChart = echarts.init(document.getElementById('<%= graph_id %>'));
        $("[name='switch_status']").bootstrapSwitch();
        $('#history'+"<%= graph_id %>").daterangepicker(
                {timePicker: true, autoUpdateInput:true,timePickerIncrement: 15, timePicker24Hour: true,locale:{format: 'YYYY-MM-DD HH:mm:ss',separator:' / '}}
        );
        var option = {
            tooltip : {
                trigger: 'axis'
            },
            legend: {
                data: [<%= legend %>],
                orient: 'vertical',
                right: 'right',
                top: 'middle'
            },
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            grid: {
                left: '3%',
                right: '30%',
                bottom: '<%= itemPercent %>%',
                containLabel: true,
            },
            xAxis : [
                {
                    type : 'category',
                    axisTick:{show:false},
                    axisLine: {
                        onZero: true,
                        lineStyle: {
                            color: 'rgba(0,0,0,0.4)'
                        }
                    },
                    axisLabel: {rotate:70, interval:5,margin:2},
                    boundaryGap : false,
                    data : [<%= date %>]
                }
            ],
            yAxis : [
                {
                    type : 'value',
                    axisTick:{show:false},
                    axisLine: {
                        lineStyle: {
                            color: 'rgba(0,0,0,0.4)'
                        }
                    }
                }
            ],
            series : [
                <% _.each(data, function (item_data) { %>
            {
                    name:'<%= item_data.item_name %>',
                    type:'line',
                    stack: '总量',
                    label: {
                        normal: {
                            show: false,
                            position: 'top'
                        }
                    },
                    data:[<%= item_data.values %>]
                },
        <% })%>
            ]
        };

        myChart.setOption(option);
    })

</script>