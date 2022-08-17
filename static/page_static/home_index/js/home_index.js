var grxx1=document.getElementById("grxx1");
var grxx2=document.getElementById("grxx2");
var grxx3=document.getElementById("grxx3");
var grxx4=document.getElementById("grxx4");
var grxx5=document.getElementById("grxx5");
var grxx6=document.getElementById("grxx6");
var grxx7=document.getElementById("grxx7");
var page_name=document.getElementById("page_name")
$.ajax({
    url: "/home/get_pinfo/",
    type: "get",
    success: function (res) {
        page_name.innerHTML="欢迎 "+res['name'];
        grxx1.innerHTML=res['name'];
        grxx2.innerHTML=res['studentId'];
        grxx3.innerHTML=res['collegeName'];
        grxx4.innerHTML=res['majorName'];
        grxx5.innerHTML=res['className'];
        grxx6.innerHTML=res['politicalStatus'];
        grxx7.innerHTML=res['status'];


    }
});
let myChart1 = echarts.init(document.getElementById('main'));
var date = new Date();
var month = date.getMonth() + 1;//当前月

var year = date.getFullYear();//当前年(4位)
if (month<9){
    month=0;
}
else {
    month=1;
}
var url_grade_1="/home/get_grade?year="+year+"&month="+month+"&zylb="+3;
function getCategoryPolice_yuan(url_grade_1){
$.get(url_grade_1).done(function(data) {
  myChart1.setOption({
      title: {
      text: data["zylb"],
      left: 'left',
      textStyle:{
            fontSize:22
          },
    },

  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: [
    {
      type: 'category',
      data: data.x,
      axisTick: {
        alignWithLabel: true
      },
        axisLabel: {
      rotate: 40
    }
    }
  ],
  yAxis: [
    {
      type: 'value'
    }
  ],
  series: [
    {
        name:"分数",
      type: 'bar',
      barWidth: '60%',
      data: data.nb,
    }
  ],
     tooltip: {
        trigger: 'axis',

        axisPointer: {
            type: 'shadow'
        },

    }
    }

    );

 window.onresize = function(){
 myChart1.resize();
}
})}
getCategoryPolice_yuan(url_grade_1);


var cx_year=document.getElementById("cx_year");
var cx_month=document.getElementById("cx_month");
var zylb=document.getElementById("zylb");
$("#grade_cx").click(function () {
    var url_cx="/home/get_grade?year="+cx_year.value+"&month="+cx_month.value+"&zylb="+zylb.value;
    getCategoryPolice_yuan(url_cx);

})