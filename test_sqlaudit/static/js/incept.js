
$('.sqlcontent').click(function(){
  var sqlcontent = $(this).attr('ckvalue')
  $('#infomodal').modal({show:true, backdrop:'static'})
  sqllist = sqlcontent.split(';')
  sqlhtml = ''
  for (i in sqllist){
      if(sqllist[i] == ''){break}  // 不要最后那个多余的分号
      sqlhtml += '<div>' + sqllist[i] + ';' + '</div>'
  }
  $('#inforz').html(sqlhtml)
  $('#infotitle').html('SQL详情')
})

$('.opsqldetail').click(function(){
  var suggestion = $(this).attr('ckvalue')
  $('#infomodal').modal({show:true, backdrop:'static'})
  $('.modal-dialog').css({'width':'80%', 'height':'60%'})
  $('#inforz').html('<pre>' + suggestion + '</pre>')
  $('#infotitle').html('优化建议')
})

$('.sqldetail').click(function () {
    var sql = $(this).attr('ckvalue')
    $('#sqlmodal').modal({show:true, backdrop:'static'})
    $('#sqlrz').html('<pre>' + sql + '</pre>')
    $('#sqltitle').html('SQL语句')

})


$('.sqlfailbtn').click(function(){
  var failcontent = $(this).attr('ckvalue')
    data = failcontent.split('),')
    failhtml = ''
    for (i in data){
      row = data[i]
      if (row.search(/Execute failed/i) != -1 ){  // 匹配到错误的sql
          failhtml += '<div style="color:indianred">' + row + '),</div>'
      } else {
          failhtml += '<div>' + row + '),</div>'
      }
    }
    // 替换结尾多余的),
    var regExp = /\)\,\<\/div\>$/
    failhtml = failhtml.replace( regExp, "</div>" )
    console.log(failhtml)
    $('#sqlmodal').modal({show:true, backdrop:'static'})
    $('#sqlrz').html(failhtml)
    $('#sqltitle').html('失败详情')
})

$('.sqlnote').click(function(){
  var notecontent = $(this).attr('ckvalue')
  $('#infomodal').modal({show:true, backdrop:'static'})
  $('#inforz').html(notecontent)
  $('#infotitle').html('备注')
})

$(".sqlaction").click(function(){
  var $this =$(this)
  var sqlid = $this.attr('ckid')
  var actiontype = $this.attr('actiontype')
  $('.sqlaction').attr({"disabled":"disabled"})  // 所有按钮禁用
  if (actiontype=='execute'){
	$('#actioncontent').html('执行此SQL到数据库？')
	}
  else if (actiontype=='reject'){
	$('#actioncontent').html('放弃此SQL？')
	}
  else if (actiontype=='pause'){
	$('#actioncontent').html('暂停此SQL？')
	}
  else if (actiontype=='cancelpause'){
	$('#actioncontent').html('取消暂停此SQL？')
	}
  else if (actiontype=='rollback'){
	$('#actioncontent').html('确定回滚本SQL？')
	}
  $('#action').modal({show:true, backdrop:'static'})
  $('#actioncancel').click(function(){
	$('#action').modal('hide') 
	$('.sqlaction').removeAttr("disabled")  // 所有按钮启用 
  })
  $("#actionsave").unbind('click').bind('click',function(){
    $('#action').modal('hide')  
    $this.parent().parent().children().children('#imgloading').show()
    $.ajax({
        type: "post",
        url: "/sqlmng/inception_result/" + sqlid + "/" + actiontype,
        data: {},
        dataType: "json",
        success: function(result){
            console.log(result)
            $this.parent().parent().children().children('#imgloading').hide()
            status = result.status
            if (actiontype == 'execute'){
                if (status == 0){
                    var Warninghtml = '<p> </p>'
                    if(result.Warning != "") {
                        Warninghtml = '<p>Warning：' + result.Warning + '</p>'
                    }
                    htmlcontent = '<p>' + 'SQL执行结果：' + '成功' + '</p>' + '<p>' + '受影响的行：' + result.affected_rows + '</p>' + '<p>' + '时间：' + result.execute_time + '</p>' + Warninghtml
                }
                else if (status == -2){
                    htmlcontent = '<p>' + 'SQL状态已被改变' + '</p>'
                }
                else if (status == -1){
                    htmlcontent = '<p>' + '执行失败：' + result.msg + '</p>'
                }
                else {
                    htmlcontent = result.msg
                }
            }
            else if (actiontype == 'rollback'){
                if (status == 0){
                    htmlcontent = '<p> SQL回滚结果：' + '成功' + ' </p>' + '<p> 影响的行数：' + result.rollnum + ' </p>'
                }
                else{
                    htmlcontent = '<p> SQL回滚失败 </p>'
                }
            }
            else if (actiontype == 'pause'){
                if (status == 0){
                    htmlcontent = '<p> SQL已暂停 </p>'
                }
            }
            else if (actiontype == 'cancelpause'){
                if (status == 0){
                    htmlcontent = '<p> SQL已取消暂停 </p>'
                }
            }
            else if (actiontype == 'reject'){
                if (status == 0){
                    htmlcontent = '<p> SQL已放弃 </p>'
                }
            }

		$('#infomodal').modal({show:true, backdrop:'static'})
            $('#inforz').html(htmlcontent)

		$('#infoclose').click(function(){
		    location.reload()
		})
        },
        error: function(){
        },
	})
  })
})

// 删除优化的sql
 $('.sqldelete').unbind('click').bind('click', function(){
     var id = $(this).attr('ckid')
     var url = "/sqlmng/optimize_result/" + id
     $('#action').modal({show:true, backdrop:'static'})
     $('#actioncontent').html('<span>确认删除该记录吗？</span>')
     $('#actionsave').unbind('click').bind('click', function(){
         $.ajax({
             type: "delete",
             url: url,
             data: {},
             dataType: "json",
             success: function(data){
                 if ( data.status == 0 ){
                     name = data.name
                     $('#action').modal('hide')
                     $('#infomodaldialog').css('text-align', 'center')
                     $('#infomodaldialog').css('width','30%')
                     $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                     $('#inforz').html('<span>删除成功！</span>')
                     $('#infoclose').click(function(){
                         location.reload()
                     })
                 }
                 },
             error: function(){
                 console.log('404..')
             },
         })

     })
 })

