
$("#seabtn").click(function(){
    var searchstr = $("#souinput").val()
    if ($.trim(searchstr) == ''){
        $('#inforz').html("输入不能为空")
        $('#infomodal').modal({show:true, backdrop:'static'})    // 显示模态框
        return false  // 不进行后面的（点击链接）操作
        }
    url = "/cmdb/search/?cmdbtype=vp&searchstr="+searchstr
    $("#tiaozhuansearch").attr("href",url)
        })

// 模态框
$('#vpadd').click(function(){
    $('#virtualpropertymodal').modal({show:true, backdrop:'static'}) 

})

// 点击模态框的vpresourcebtn：隐藏vptypemodal，显示vpresourcemodal；ajax请求后台获取select框的所有类型
$('#vpresourcebtn').click(function(){
    $('#vptypemodal').hide()
    $('#vpresourcemodal').show()
    // 改变模态框的“保存按钮”ckvalue，用于提交时 按这个值来区分类别
    $('#vpaddsave').attr('ckvalue','vpresource')
    // 从后台获取vptype数据，生成option
    var actiontype = 'select'
    $.ajax({
             type: "POST",
             url: "/cmdb/vpapi/",
             data: {actiontype:actiontype},
             dataType: "json",
             success: function(data){
              //业务逻辑    
		console.log(data)     
		var allvptypes = data.datas
		var selecthtml = '<option disabled selected> </option>' 
		for (i in allvptypes){
		    selecthtml = selecthtml + '<option>' + allvptypes[i] + '</option>'
		    }
		$('#selectvptype').html(selecthtml)	
             },
	     error: function(){
	     //显示错误信息
	     },
	})
})

// 点击模态框的vptypebtn：隐藏vpresourcemodal，显示vptypemodal
$('#vptypebtn').click(function(){
    $('#vpresourcemodal').hide()
    $('#vptypemodal').show()
    // 改变模态框的“保存按钮”ckvalue，用于提交时 按这个值来区分类别
    $('#vpaddsave').attr('ckvalue','vptype')
})

// 点击 模态框的 添加按钮
$('#vpaddsave').click(function(){
    alert(11)
	var selectenv = $.trim($('#selectenv').val())
	var name = $.trim($('#name').val())
	var host = $.trim($('#host').val())
	var port = $.trim($('#port').val())
	var username = $.trim($('#username').val())
	// var password = $.trim($('#password').val())
	var note = $('#note').val()
    alert(name)

	var inputlist = [name, host, port, username, password]

        if (name == ''){
            $('#name').css({'border-color': 'red', 'background-color': '#FFD2D2'})
        }

        if (host == ''){
            $('#host').css({'border-color': 'red', 'background-color': '#FFD2D2'})
        }

        if (port == ''){
            $('#port').css({'border-color': 'red', 'background-color': '#FFD2D2'})
        }

        if (username == ''){
            $('#username').css({'border-color': 'red', 'background-color': '#FFD2D2'})
        }

        if (password == ''){
            $('#password').css({'border-color': 'red', 'background-color': '#FFD2D2'})
        }

        if (name == '' || host == '' || port == '' || username == '' || password == '' ){
            return false
        }
        $.ajax({
             type: "POST",
             url: "/sql/dbconfig/",
             data: {selectenv:selectenv, name:name, host:host, port:port, username:username, password:password},
             dataType: "json",
             success: function(data){
              //业务逻辑    
                console.log(data)     
		        var status = data.status
                if (status == -1){
                    $('#name').css({'border-color': 'red', 'background-color': '#FFD2D2'})
                    $('#name').attr('value', name + '（提示：该名称已存在）')
                    $('#vpaddsave').attr({"disabled":"disabled"})  // "添加"按钮禁用

                }
                else if (status == 0){
                    $('#virtualpropertymodal').hide()  // 收起"添加"模态框
                    $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起"提示"模态框
                    $('#inforz').html('<span style="font-weight:bold; color:blue; margin-right:10px">'+name+'</span>'+'<span> 添加成功！</span>')
                    $('#infoclose').click(function(){  // 点击关闭按钮，刷新当前页
                        location.reload()
                    })
                }

             },
             error: function(){
             //显示错误信息
             },
        })
})

// 点击模态框的取消按钮 或 cknav （多个元素绑定同一事件），把 needinputsingle 输入框的内容清空，样式清空，启用“添加”按钮
$('#vpaddcancel, .cknav').click(function(){
    $('.needinputsingle, .needinput').attr('value','')
    $('.needinputsingle, .needinput').css({'border-color': '', 'background-color': ''})
    $('#vpaddsave').removeAttr("disabled")
})

// 点击“必填”的input 输入的内容需要在数据库里唯一，启用按钮，清空输入框，清空样式
$('.needinputsingle').click(function(){
    $('#vpaddsave').removeAttr("disabled")  // “添加”按钮启用
    $(this).attr('value','')
    $(this).css({'border-color': '', 'background-color': ''})  // css复原
})

// 点击“必填”的input，清空样式
$('.needinput').click(function(){
    $(this).css({'border-color': '', 'background-color': ''})  // css复原
})

 // 修改类别（数据从后台获取改为从table获取）
 $('.mdyvptype').unbind('click').bind('click', function(){
     // 弹起模态框
	 $('#mvptypemodal').modal('show')
                    var updateid = $(this).attr('ckid')
             	    var vp = 'vptype'
		    // 从table该行数据，给模态框赋值
                    var vpname = $(this).parents("tr").children("td").eq(0).text()
                    var note = $(this).parents("tr").children("td").eq(3).text() 
                    $('#mvptypename').attr("value", vpname)
                    $('#mvptypenote').attr("value", note)
                    // 点击模态框的保存按钮，获取各数据发ajax至后台完成修改
                    $("#mvptypesave").unbind('click').bind('click',function(){
                            var actiontype = 'modify'
                            var vpname = $('#mvptypename').val()
                            var note = $('#mvptypenote').val()
                            $.ajax({
                                type: "POST",
                                url: "/cmdb/vpapi/",
                                data: {name:vpname, note:note, actiontype:actiontype, updateid:updateid, vp:vp},
                                dataType: "json",
                                success: function(data){
                                    if (data.status == 0){
                                        location.reload()
                                        return
                                        }
                                    else if (data.info == 'DataError'){
                                        alert('输入的字符超过长度！')
                                        }
                                },
                                error: function(){
                                        console.log('404..')
                                },
                            })
                            $('#mvptypemodal').modal('hide')
                })
 })

 // 修改资源（数据从后台获取改为从table获取）
 $('.mdyvprs').unbind('click').bind('click', function(){
     // 弹起模态框
	 $('#mvprsmodal').modal('show')
                    var updateid = $(this).attr('ckid')
             	    var vp = 'vpresource'
		    // 从table该行数据，给模态框赋值
                    var name = $(this).parents("tr").children("td").eq(1).text()
                    var exptime = $(this).parents("tr").children("td").eq(2).text() 
                    var note = $(this).parents("tr").children("td").eq(4).text() 
                    $('#mvprsname').attr("value", name)
                    $('#mvprsexptime').attr("value", exptime)
                    $('#mvprsnote').attr("value", note)
                    // 点击模态框的保存按钮，获取各数据发ajax至后台完成修改
                    $("#mvprssave").unbind('click').bind('click',function(){
                            var actiontype = 'modify'
                            var name = $('#mvprsname').val()
			    var exptime = $('#mvprsexptime').val()
                            var note = $('#mvprsnote').val()
                            $.ajax({
                                type: "POST",
                                url: "/cmdb/vpapi/",
                                data: {name:name, note:note, exptime:exptime, actiontype:actiontype, updateid:updateid, vp:vp},
                                dataType: "json",
                                success: function(data){
                                    if (data.status == 0){
                                        location.reload()
                                        return
                                        }
                                    else if (data.info == 'DataError'){
                                        alert('输入的字符超过长度！')
                                        }
                                },
                                error: function(){
                                        console.log('404..')
                                },
                            })
                            $('#mvprsmodal').modal('hide')
                })
 })

// 点击 删除按钮（类deletevp）
 $('.deletevp').unbind('click').bind('click', function(){
        var vp = $(this).attr('ckvalue')
        var actiontype = 'delete'
        var deleteid = $(this).attr('ckid')  
        var url = "/cmdb/vpapi/"    
	var name = $(this).attr('ckname')
	var vnum = $(this).parents('tr').children('td').eq(1).text()  // 获取该类别的资源数（若大于0，则不允许删除）
	console.log(vnum)
	if (vnum > 0){
	    $('#infomodal').modal({show:true, backdrop:'static'})
	    $('#inforz').html('<span>无法删除：</span>'+'<span style="font-weight:bold;color:blue; margin-right:10px; margin-left:10px">'+name+'</span>'+ '<p>原因：资源数大于0</p>')
	    return false
	}
        $('#deleteModal').modal({show:true, backdrop:'static'})
	$('#deleteModalbody').html('<span>确认删除</span>'+'<span style="font-weight:bold;color:blue; margin-right:10px; margin-left:10px">'+name+'</span>'+ '<span>吗？</span>')
        $('#savedeletebtn').unbind('click').bind('click', function(){
                $('#deleteModal').modal('hide')
                $.ajax({
                        type: "POST",
                        url: url,
                        data: {vp:vp, actiontype:actiontype, deleteid:deleteid},
                        dataType: "json",
                        success: function(data){
                            if ( data.status == 0 ){
                                name = data.name
                                $('#deleteModal').modal('hide')
                                $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                $('#inforz').html('<span style="font-weight:bold; color:blue; margin-right:10px">' + name + '</span>' + '<span>删除成功！</span>')
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


