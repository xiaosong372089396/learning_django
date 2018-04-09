
// 删除数组的指定元素
  function removeByValue(arr, val) {
      for(var i=0; i<arr.length; i++) {
          if(arr[i] == val) {
              arr.splice(i, 1);
              break;
          }
      }
  }

// 点击 搜索按钮
$("#seabtn").click(function(){
    var searchstr = $("#souinput").val()
    if ($.trim(searchstr) == ''){
        $('#inforz').html("输入不能为空")
        $('#infomodal').modal({show:true, backdrop:'static'})    // 显示模态框
        return false  // 不进行后面的（点击链接）操作
        }
    url = "/cmdb/search/?cmdbtype=phone&searchstr="+searchstr
    $("#tiaozhuansearch").attr("href",url)
    })

// 弹起 添加 模态框
$('#opadd').click(function(){
    $('#office_phone_modal').modal({show:true, backdrop:'static'}) 
})

// 点击模态框的phonesbtn：隐藏office，显示phone；ajax请求后台获取select框的数据
$('#phonesbtn').click(function(){
    $('#officesmodal').hide()
    $('#phonesmodal').show()
    // 改变模态框的“保存按钮”ckvalue，用于提交时 按这个值来区分类别
    $('#opaddsave').attr('ckvalue','phone')
    // 从后台获取办公区数据，生成option
    var actiontype = 'select'
    $.ajax({
             type: "POST",
             url: "/cmdb/opapi/",
             data: {actiontype:actiontype},
             dataType: "json",
             success: function(data){
              //业务逻辑    
		console.log(data)     
		var alloffices = data.datas
		var selecthtml = '<option disabled selected> </option>' 
		for (i in alloffices){
		    selecthtml = selecthtml + '<option>' + alloffices[i] + '</option>'
		    }
		$('#selectoffice').html(selecthtml)	
             },
	     error: function(){
	     //显示错误信息
	     },
	})
})

// 点击模态框的officesbtn：隐藏phone，显示officemodal
$('#officesbtn').click(function(){
    $('#phonesmodal').hide()
    $('#officesmodal').show()
    // 改变模态框的“保存按钮”ckvalue，用于提交时 按这个值来区分类别
    $('#opaddsave').attr('ckvalue','office')
})

// 点击 模态框的 添加按钮
$('#opaddsave').click(function(){
    var actiontype = 'add'
    var op = $(this).attr('ckvalue')
    if(op == 'office'){  // 添加 'office'
	console.log(1)
	var officename = $.trim($('#officename').val())
	var officearea = $.trim($('#officearea').val())
	var officenote = $.trim($('#officenote').val())
	if (officename == ''){
	    $('#officename').css({'border-color': 'red', 'background-color': '#FFD2D2'})
	}

        if (officearea == ''){
            $('#officearea').css({'border-color': 'red', 'background-color': '#FFD2D2'})
        }

	if(officename == '' || officearea == ''){  // 有必填项为空的，终止程序
	    return false
	}
        $.ajax({
             type: "POST",
             url: "/cmdb/opapi/",
             data: {actiontype:actiontype, op:op, officename:officename, officearea:officearea, officenote:officenote},
             dataType: "json",
             success: function(data){
              //业务逻辑    
                console.log(data)     
		var status = data.status
		if (status == -1){
		    $('#officename').css({'border-color': 'red', 'background-color': '#FFD2D2'})
		    $('#officename').attr('value', officename + '（提示：该名称已存在）')
		    $('#opaddsave').attr({"disabled":"disabled"})  // "添加"按钮禁用
		}
		else if (status == 0){
		    $('#office_phone_modal').hide()  // 收起"添加"模态框
		    $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起"提示"模态框
		    $('#inforz').html('<span style="font-weight:bold; color:blue; margin-right:10px">'+officename+'</span>'+'<span> 添加成功！</span>')
                    $('#infoclose').click(function(){  // 点击关闭按钮，刷新当前页
                        location.reload()
                    })
		}
             },
             error: function(){
             //显示错误信息
             },
        })
    }
    else if (op == 'phone'){  // 添加 'phone'
	var selectoffice = $('#selectoffice').val()
	var uname = $.trim($('#uname').val())
	var department = $.trim($('#department').val())
	var site = $.trim($('#site').val())
	var liantongnum = $.trim($('#liantongnum').val())
	var dianxinnum = $.trim($('#dianxinnum').val())
	var sncode = $.trim($('#sncode').val())
	var mac = $.trim($('#mac').val())
	var ptype = $.trim($('#ptype').val())
	var phonestatus = $('#status').val()
	var phonenote = $.trim($('#phonenote').val())
	var inputlist = [selectoffice, uname, department, site, liantongnum, dianxinnum, sncode, mac, ptype, phonestatus]
	if (selectoffice == ''){
		$('#selectoffice').css({'border-color': 'red', 'background-color': '#FFD2D2'})
	}

        if (uname == ''){
                $('#uname').css({'border-color': 'red', 'background-color': '#FFD2D2'})
        }

        if (department == ''){
                $('#department').css({'border-color': 'red', 'background-color': '#FFD2D2'})
        }

        if (site == ''){
                $('#site').css({'border-color': 'red', 'background-color': '#FFD2D2'})
        }

        if (liantongnum == ''){
                $('#liantongnum').css({'border-color': 'red', 'background-color': '#FFD2D2'})
        }

        if (dianxinnum == ''){
                $('#dianxinnum').css({'border-color': 'red', 'background-color': '#FFD2D2'})
        }
        if (sncode == ''){
                $('#sncode').css({'border-color': 'red', 'background-color': '#FFD2D2'})
        }

        if (mac == ''){
                $('#mac').css({'border-color': 'red', 'background-color': '#FFD2D2'})
        }

        if (ptype == ''){
                $('#ptype').css({'border-color': 'red', 'background-color': '#FFD2D2'})
        }

        if (phonestatus == ''){
                $('#status').css({'border-color': 'red', 'background-color': '#FFD2D2'})
        }
	// 要求必填的项
        if (selectoffice == '' || uname == '' || department == '' || site == '' || sncode == '' || mac == '' || ptype == '' || phonestatus == ''){
            return false
        }
	// 电信，联通号至少有一个
	if (liantongnum == '' && dianxinnum == ''){
	    return false
	}
        $.ajax({
             type: "POST",
             url: "/cmdb/opapi/",
             data: {actiontype:actiontype, op:op, selectoffice:selectoffice, uname:uname, department:department, site:site, liantongnum:liantongnum, dianxinnum:dianxinnum, sncode:sncode, mac:mac, ptype:ptype, phonestatus:phonestatus, phonenote:phonenote},
             dataType: "json",
             success: function(data){
              //业务逻辑    
                console.log(data)     
		var status = data.status
                if (status == -1){
		    ckaddtype = '更新'
                }
                else if (status == 0){
		    ckaddtype = '添加'
                }
                $('#office_phone_modal').hide()  // 收起"添加"模态框
                $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起"提示"模态框
                $('#inforz').html('<span style="font-weight:bold; color:blue; margin-right:10px">' + mac + '</span>'+'<span>' + ckaddtype + '成功！</span>')
                $('#infoclose').click(function(){  // 点击关闭按钮，刷新当前页
                location.reload()
                })
             },
             error: function(){
             //显示错误信息
             },
        })
    }
})

// 点击模态框的取消按钮 或 cknav （多个元素绑定同一事件），把 needinputsingle 输入框的内容清空，样式清空，启用“添加”按钮
$('#opaddcancel, .cknav').click(function(){
    $('.needinputsingle, .needinput').attr('value','')
    $('.needinputsingle, .needinput').css({'border-color': '', 'background-color': ''})
    $('#opaddsave').removeAttr("disabled")
})

// 点击“必填”的input 输入的内容需要在数据库里唯一，启用按钮，清空输入框，清空样式
$('.needinputsingle').click(function(){
    $('#opaddsave').removeAttr("disabled")  // “添加”按钮启用
    $(this).attr('value','')
    $(this).css({'border-color': '', 'background-color': ''})  // css复原
})

// 点击“必填”的input，清空样式
$('.needinput').click(function(){
    $(this).css({'border-color': '', 'background-color': ''})  // css复原
})

 // 修改办公区（数据从后台获取改为从table获取）
 $('.mdyoffice').unbind('click').bind('click', function(){
     // 弹起模态框
	 $('#mofficemodal').modal('show')
                    var updateid = $(this).attr('ckid')
             	    var op = 'office'
		    // 从table的该行取数据，给模态框赋值
                    var officename = $(this).parents("tr").children("td").eq(0).text()
                    var officearea = $(this).parents("tr").children("td").eq(3).text() 
                    var officenote = $(this).parents("tr").children("td").eq(4).text() 
                    $('#mofficename').attr("value", officename)
                    $('#mofficearea').attr("value", officearea)
                    $('#mofficenote').attr("value", officenote)
		    $('#mdyofficetitle').text(officename)  // 渲染 "修改office"模态框标题
                    // 点击模态框的保存按钮，获取各数据发ajax至后台完成修改
                    $("#mofficesave").unbind('click').bind('click',function(){
                            var actiontype = 'modify'
                            var officename = $.trim($('#mofficename').val())
			    var officearea = $.trim($('#mofficearea').val())
                            var officenote = $.trim($('#mofficenote').val())
                            $.ajax({
                                type: "POST",
                                url: "/cmdb/opapi/",
                                data: {officename:officename, officearea:officearea, officenote:officenote, actiontype:actiontype, updateid:updateid, op:op},
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
                            $('#mofficemodal').modal('hide')
                })
 })

 // 修改电话（数据从后台获取改为从table获取）
 $('.mdyphone').unbind('click').bind('click', function(){
     // 弹起模态框
	 $('#mphonemodal').modal('show')
                    var updateid = $(this).attr('ckid')
             	    var op = 'phone'
		    // 从table该行数据，给模态框赋值
                    var uname = $(this).parents("tr").children("td").eq(1).text()
                    var department = $(this).parents("tr").children("td").eq(2).text()
                    var site = $(this).parents("tr").children("td").eq(3).text()
                    var dianxinnum = $(this).parents("tr").children("td").eq(4).text()
                    var liantongnum = $(this).parents("tr").children("td").eq(5).text()
                    var sncode = $(this).parents("tr").children("td").eq(6).text()
                    var mac = $(this).parents("tr").children("td").eq(7).text()
                    var ptype = $(this).parents("tr").children("td").eq(8).text()
                    var phonestatus = $.trim($(this).parents("tr").children("td").eq(9).text())
                    var phonenote = $(this).parents("tr").children("td").eq(10).text()
		    $('#mdyphonetitle').text(mac)  // 渲染"修改phone"模态框标题
		    // 按当前的状态 排列select顺序
		    console.log(phonestatus)
		    if (phonestatus == '在线'){
			$("#onstatus").attr("checked","checked");
		    }
		    else{
			$("#offstatus").attr("checked","checked");
		    }
                    $('#muname').attr("value", uname)
                    $('#mdepartment').attr("value", department)
                    $('#msite').attr("value", site)
                    $('#mdianxinnum').attr("value", dianxinnum)
                    $('#mliantongnum').attr("value", liantongnum)
                    $('#msncode').attr("value", sncode)
                    $('#mmac').attr("value", mac)
                    $('#mptype').attr("value", ptype)
                    $('#mstatus').attr("value", phonestatus)
                    $('#mphonenote').attr("value", phonenote)
                    // 点击模态框的保存按钮，获取各输入框的数据，ajax至后台完成修改
                    $("#mphonesave").unbind('click').bind('click',function(){
                            var actiontype = 'modify'
                            var uname = $.trim($('#muname').val())
                            var department = $.trim($('#mdepartment').val())
                            var site = $.trim($('#msite').val())
                            var dianxinnum = $.trim($('#mdianxinnum').val())
                            var liantongnum = $.trim($('#mliantongnum').val())
                            var sncode = $.trim($('#msncode').val())
                            var mac = $.trim($('#mmac').val())
                            var ptype = $.trim($('#mptype').val())
                            //var phonestatus = $.trim($('#mstatus').val())
                            var phonenote = $.trim($('#mphonenote').val())
			    var phonestatus = $('input[name="form-field-radio"]').filter(':checked').val()
				console.log(phonestatus)
                            $.ajax({
                                type: "POST",
                                url: "/cmdb/opapi/",
                                data: {uname:uname, department:department, site:site, dianxinnum:dianxinnum, liantongnum:liantongnum, sncode:sncode, mac:mac, ptype:ptype, phonestatus:phonestatus, phonenote:phonenote, actiontype:actiontype, updateid:updateid, op:op},
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
                            $('#mphonemodal').modal('hide')
                })
 })

// 点击 删除按钮
 $('.deleteop').unbind('click').bind('click', function(){
        var op = $(this).attr('ckvalue')  // 获取删除元素的类型（后端根据此类型去操作）
        var actiontype = 'delete'
        var deleteid = $(this).attr('ckid')  
        var url = "/cmdb/opapi/"    
	if (op == 'office'){
            var dianxins = $(this).parents('tr').children('td').eq(1).text()  // 获取电信电话数
            var liantongs = $(this).parents('tr').children('td').eq(2).text()  // 获取联通电话数
	    var name = $(this).parents('tr').children('td').eq(0).text()  // 获取同tr第0个td的值
            if (dianxins > 0 || liantongs > 0){  // 若办公区的电信/联通电话数 大于0，则不删除
                $('#infomodal').modal({show:true, backdrop:'static'})
                $('#inforz').html('<span>无法删除：</span>'+'<span style="font-weight:bold;color:blue; margin-right:10px; margin-left:10px">'+name+'</span>'+ '<p>原因：电信/联通电话数 大于0</p>')
                return false
            }
	    warhtml = '<span>确认删除</span>'+'<span style="font-weight:bold;color:blue; margin-right:10px; margin-left:10px">' + name + '</span>'+ '<span>吗？</span>'
	    rzhtml = '<span style="font-weight:bold; color:blue; margin-right:10px">' + name + '</span>' + '<span>删除成功！</span>'
	}
	else if(op == 'phone'){
	    sncode = $(this).attr('ckname')
	    warhtml = '<span>确认删除</span>'+'<span style="font-weight:bold;color:blue; margin-right:10px; margin-left:10px">' +sncode+ '</span>'+ '<span>吗？</span>'
	    rzhtml = '<span style="font-weight:bold; color:blue; margin-right:10px">' + sncode + '</span>' + '<span>删除成功！</span>'
	}
        $('#deleteModal').modal({show:true, backdrop:'static'})
	$('#deleteModalbody').html(warhtml)
        $('#savedeletebtn').unbind('click').bind('click', function(){
                $('#deleteModal').modal('hide')
                $.ajax({
                        type: "POST",
                        url: url,
                        data: {op:op, actiontype:actiontype, deleteid:deleteid},
                        dataType: "json",
                        success: function(data){
                            if ( data.status == 0 ){
                                $('#deleteModal').modal('hide')
                                $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                $('#inforz').html(rzhtml)
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


