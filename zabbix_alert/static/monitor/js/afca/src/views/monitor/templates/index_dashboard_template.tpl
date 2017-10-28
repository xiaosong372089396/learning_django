<div id="main" style="height:300px;"></div>
    <script type="text/javascript">
        require(['echarts', 'jquery'], function (echarts, $){
            var myChart = echarts.init(document.getElementById('main'));
            var option = {
                backgroundColor: '#fff',
                legend: {
                    data: ['正常','故障'],
                    align: 'left',
                    left: 10
                },
                brush: {
                    toolbox: ['clear'],
                    xAxisIndex: 0
                },
                toolbox: {
                    feature: {
                        magicType: {
                            type: ['stack', 'tiled']
                        },
                        dataView: {}
                    }
                },
                tooltip: {},
                xAxis: {
                    data: [<%= group_status_info.group_name %>],
                    axisTick:{show:false},
                    name: '',
                    silent: false,
                    axisLine: {
                        onZero: true,
                        lineStyle: {
                            color: 'rgba(0,0,0,0.4)'
                        }
                    },
                    splitLine: {show: false},
                    splitArea: {show: false},
                    color:"#dd4b39"
                },
                yAxis: {
                    inverse: false,
                    axisTick:{show:false},
                    splitArea: {show: false},
                    axisLine: {
                        lineStyle: {
                            color: 'rgba(0,0,0,0.4)'
                        }
                    }
                },
                grid: {
                    left: 100
                },
                visualMap: {
                    type: 'continuous',
                    dimension: 1,
                    text: ['High', 'Low'],
                    inverse: false,
                    itemHeight: 150,
                    calculable: true,
                    min: 0,
                    max: <%= group_status_info.max_count %>,
                    top: 60,
                    left: 10,
                    inRange: {
                        colorLightness: [0.6, 0.5]
                    },
                    outOfRange: {
                        color: 'red'
                    },
                    controller: {
                        inRange: {
                            color: '#00a65a'
                        }
                    }
                },
                series: [
                    {
                        name: '故障',
                        barWidth:40,
                        type: 'bar',
                        stack: 'one',
                        itemStyle:{
                            normal:{
                                color:"#dd4b39"
                            }
                        },
                        data: [<%= group_status_info.host_issue_count %>]
                    },
                    {
                        name: '正常',
                        barWidth:40,
                        type: 'bar',
                        stack: 'one',
                        itemStyle:{
                            normal:{
                                color:"#00a65a"
                            }
                        },
                        data: [<%= group_status_info.host_normal_count %>]
                    }
                ]
            };
            myChart.setOption(option);
        })

    </script>