<div class="box box-info">
    <div class="box-header with-border">
        <h3 class="box-title"><%= name %>(<%= unit %>)</h3>
        <div class="box-tools pull-right">
            <button type="button" class="btn btn-box-tool" data-widget="collapse"><i class="fa fa-minus"></i>
            </button>
            <button type="button" class="btn btn-box-tool" data-widget="remove"><i class="fa fa-times"></i></button>
        </div>
    </div>
    <div class="box-body">
        <div class="col-md-12">
            <div id="<%= html_id %>" style="height:300px;"></div>
        </div>
    </div>

</div>

<script type="text/javascript">
    require(['echarts', 'jquery'], function (echarts, $){
        var myChart = echarts.init(document.getElementById('<%= html_id %>'));
        var option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            backgroundColor: '#fff',
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'value',
                axisTick:{show:false},
                axisLine: {
                        lineStyle: {
                            color: 'rgba(0,0,0,0.4)'
                        }
                    },
                boundaryGap: [0, 0.01]
            },
            yAxis: {
                type: 'category',
                axisTick:{show:false},
                axisLine: {
                        lineStyle: {
                            color: 'rgba(0,0,0,0.4)'
                        }
                    },
                data: [<%= chart_category %>]
            },
            series: [
                {
                    name: " 当前值",
                    type: 'bar',
                    itemStyle:{
                            normal:{
                                color:"#dd4b39"
                            }
                        },
                    data: [<%= value %>]
                }
            ]
        };

        myChart.setOption(option);
    })

</script>