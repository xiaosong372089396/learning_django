
function bingtu(bingtudata) {
        var chart;
        chart = new Highcharts.Chart({
        chart: {
            renderTo: "container2",        //在哪个区域呈现，对应HTML中的一个元素ID
            plotBackgroundColor: null,    //绘图区的背景颜色
            plotBorderWidth: null,        //绘图区边框宽度
            plotShadow: false            //绘图区是否显示阴影            
                        },
                        
            title: {
                text: "服务器&网络设备"
                        },
            tooltip: {
                formatter: function() {
                return '<b>'+ this.point.name +'</b>: '+ Highcharts.numberFormat(this.percentage, 1) +'% ('+Highcharts.numberFormat(this.y, 0, ',') +' 个)';
                                }  
                        },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: "pointer",
                    dataLabels: {
                        enabled: true,
                        color: "#000000",
                        connectorColor: "#000000",
                        formatter: function() {
                            return "<b>"+ this.point.name +"</b>: "+Highcharts.numberFormat(this.percentage,2) +" %";
                                    }
                                }
                            }
                        },
            series: [{
                type: "pie",
                name: "份额",
                data: bingtudata,
                                }]
                    });
                }

function tiaoxingtu(tiaoxdata){    
   var chart = {
      type: 'bar'
   };
   var title = {
      text: '机房&设备'   
   };
   var subtitle = {
      text: '来源: u2'  
   };
   var xAxis = {
      categories: tiaoxdata['idclist'],
      title: {
         text: null
      }
   };
   var yAxis = {
      min: 0,
      title: {
         text: '单位 (个)',
         align: 'high'
      },
      labels: {
         overflow: 'justify'
      }
   };
   var tooltip = {
      valueSuffix: '个'
   };
   var plotOptions = {
      bar: {
         dataLabels: {
            enabled: true
         }
      }
   };
   var legend = {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'top',
      x: -40,
      y: 100,
      floating: true,
      borderWidth: 1,
      backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
      shadow: true
   };
   var credits = {
      enabled: false
   };
   
   var series= [{
         name: '物理服务器',
        color: '#483D8B',
            data: tiaoxdata['phys']
        }, {
            name: '网络设备',
        color: '#32CD32',
            data: tiaoxdata['nds']
        },
   ];     
      
   var json = {};   
   json.chart = chart; 
   json.title = title;   
   json.subtitle = subtitle; 
   json.tooltip = tooltip;
   json.xAxis = xAxis;
   json.yAxis = yAxis;  
   json.series = series;
   json.plotOptions = plotOptions;
   json.legend = legend;
   json.credits = credits;
   $('#container1').highcharts(json);

}


