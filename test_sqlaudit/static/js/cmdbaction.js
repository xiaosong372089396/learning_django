
  //进行全选
   $(".quanxuan").click(function(){
   $("input[type=checkbox]").each(function(){
    if ($(this).attr("checked"))
    {
     $(this).attr("checked",false);
    }else{
     $(this).attr("checked",true);
    }
   });
   });

 // 批量修改(模态框内容)
 var idcmap = {'地理位置':'idcaddr', '联系人':'idccontacts', '联系方式':'idcphone', '备注':'idcnote'}
 var rackmap = {'机柜大小':'racksize', '备注':'racknote'}
 var netdevicemap = {'设备型号':'ndname', '责任人':'owner', '状态':'runstatus', '备注':'ndnote'}
 var hostmap = {'设备型号':'brandtype', '机型':'usize', 'CPU核心数':'cpunum', '内存':'memory', 'RAID级别':'raid', '磁盘':'disk', '操作系统':'osversion', '代码环境':'codeenv', '状态':'runstatus', '责任人':'owner', '采购日期':'buydate', '业务类型':'busstyle', '备注':'hostnote'}
 var vmmap = {'系统':'osversion', '业务':'busstyle', '责任人':'owner', '状态':'runstatus', '备注':'note'}
 // 给定字典和value，根据value求key
 function mapindex(maplist, mapvalue){
     for(i in maplist){
	if (mapvalue == i){
		return maplist[i]
	}
    }
}

// 修改
 $(document).ready(function(){
  $(".btnupdate").unbind('click').bind('click',function(){
   if ($("input:checkbox:checked").length == 0)  // 未选择
   {
	$('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
        $('#inforz').html('请先选择数据！')
   }
   else{
        var result = new Array();
        $("input[type=checkbox]").each(function () {  // 已选择
        if ($(this).is(":checked")) {
                cmdbtype = $(this).attr("cmdbtype")
                result.push($(this).attr("ckvalue"));
            }
        });
                if(result.length > 1){  // result长度大于1（多选的情形，即批量修改）
                        $('#updatebatchModal').modal({show:true, backdrop:'static'})   // 弹起批量修改的模态框
                        $('#updatebatchselect').empty()
			// 根据不同的类型，生成模态框元素
                        if (cmdbtype == 'idc'){
                                var maps = idcmap
                            }
                        else if (cmdbtype == 'rack'){
                                var maps = rackmap
                                }
			else if (cmdbtype == 'netdevice'){
				var maps = netdevicemap
				}
                        else if (cmdbtype == 'host'){
                                var maps = hostmap
                                }
                        else if (cmdbtype == 'vm'){
                                var maps = vmmap
                                }
                        for(i in maps) {
                            var modalhtml = '<option>' + i + '</option>'  // 生成修改界面的元素
                            $('#updatebatchselect').append(modalhtml)  
			    selectdata = $("#updatebatchselect").val()  // 取select值
			    sltindex = mapindex(maps, selectdata)  // 获取该值的key
			    $('#updatebatchinput').attr('ckitem', sltindex)  // 设置#updatebatchinput的属性为sltindex
                        }
			
			// 特殊之处：ckdata 的key和value都是变化的，key是select的val对应的key（对应关系在各个select的字典）
			$("#updatebatchselect").change(function(){  // select变化时，把option对应的key加到输入框的属性
			    selectdata = $("#updatebatchselect").val()
			    sltindex = mapindex(maps, selectdata)  
			    $('#updatebatchinput').attr('ckitem', sltindex)  // select变化时，给输入框变化属性值，目的是获取ckdata的key
			})

			$('#saveupdatebtn').click(function(){
                            var ckdata = {}
                            sltval = $('#updatebatchselect').val()
	  		    content = $('#updatebatchinput').val()
			    ckdata['cmdbtype'] = cmdbtype
                            ckdata['ids'] = JSON.stringify(result)
			    ckitem = $('#updatebatchinput').attr('ckitem')
			    ckdata[ckitem] = content  // ckdaata以输入框的属性ckitem为key，以content为值
			if($.trim(content) == ''){
				$('#updatebatchModal').modal('hide')  // 隐藏修改的模态框
				$('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                $('#inforz').html('输入不能为空！')
				return false  // 就此终止
			}

			    console.log(ckdata)
			
		    	    $.ajax({
             			type: "POST",
             			url: "/cmdb/batchupdate/",
             			data: ckdata,
             			dataType: "json",
             			success: function(data){
  					console.log(data)
					if(data == 'ok'){
					    $('#updatebatchModal').modal('hide')  // 隐藏修改的模态框
					    $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
					    $('#inforz').html('修改成功！')
					    $('#infoclose').click(function(){
						location.reload()				
						})
					}
             			    },
	     			error: function(){
	     		        },
			    })
		        })
                    }

		else if (result.length == 1){  // 单个修改
			    var url = '/cmdb/update/'
			    var updateid = result[0]
			// start idc
                        if (cmdbtype == 'idc'){
			    $('#upidcModal').modal({show:true, backdrop:'static'})   // 弹起修改idc的模态框                         
			    $.ajax({
			        type: "GET",
			        url: url,
			        data: {id:updateid, ajaxtype:'ajaxwebidc'},
             			dataType: "json",
             			success: function(data){
                        	  console.log(data)
                    		  $('#idctitle').html(data.idcname)
		                  $('#up_idcname').attr("value", data.idcname)
                    		  $('#up_idcaddr').attr("value", data.idcaddr)
                    		  $('#up_idccontacts').attr("value", data.idccontacts)
				  $('#up_idcphone').attr("value", data.idcphone)
                    		  $('#up_idcnote').attr("value", data.idcnote)
                    		  $("#upidcBtn").unbind('click').bind('click',function(){   // 点击保存按钮
				      var idcname = $('#up_idcname').val()
                            	      var idcaddr = $('#up_idcaddr').val()
                            	      var idccontacts = $('#up_idccontacts').val()
				      var idcphone = $('#up_idcphone').val()
                            	      var idcnote = $('#up_idcnote').val()
                            	      $.ajax({
                                          type: "GET",
                                          url: url,
                                          data: {id:updateid, ajaxtype:'upidc', idcname:idcname, idcaddr:idcaddr, idccontacts:idccontacts, idcphone:idcphone, idcnote:idcnote},
                                          dataType: "json",
                                          success: function(data){
                                              if (data.info == 'ok'){
                                            	$('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                            	$('#inforz').html('修改成功！')
                                            	$('#infoclose').click(function(){
                                                	location.reload()
                                                })
                                              }
                                              else if (data.info == 'DataError'){
                                            	$('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                            	$('#inforz').html('输入的内容超过长度！')
                                              }
                                 	    },
                                          error: function(){
                                      	      console.log('404..')
                                  	      },
                            	          })
                            	          $('#upidcModal').modal('hide')
                		      })
             			    },
             			    error: function(){
                    			console.log('404..')
                		        },
        			    })
                                }
			// end idc

			// start rack
			if (cmdbtype == 'rack'){
			    $('#uprackModal').modal({show:true, backdrop:'static'})   // 弹起修改rack的模态框 
                            $.ajax({
                                type: "GET",
                                url: url,
                                data: {id:updateid, ajaxtype:'ajaxwebrack'},
                                dataType: "json",
                                success: function(data){
                                  console.log(data)
                                  $('#racktitle').html(data.rackname)
                                  $('#up_rackname').attr("value", data.rackname)
                                  $('#up_rackaddr').attr("value", data.rackaddr)
                                  $('#up_racksize').attr("value", data.racksize)
                                  $('#up_racknote').attr("value", data.racknote)
                                  $("#uprackBtn").unbind('click').bind('click',function(){   // 点击保存按钮
                                      var rackname = $('#up_rackname').val()
                                      var rackaddr = $('#up_rackaddr').val()
                                      var racksize = $('#up_racksize').val()
                                      var racknote = $('#up_racknote').val()
                                      $.ajax({
                                          type: "GET",
                                          url: url,
                                          data: {id:updateid, ajaxtype:'uprack', rackname:rackname, rackaddr:rackaddr, racksize:racksize, racknote:racknote},
                                          dataType: "json",
                                          success: function(data){
                                              if (data.info == 'ok'){
                                                $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                                $('#inforz').html('修改成功！')
                                                $('#infoclose').click(function(){
                                                        location.reload()
                                                })
                                              }
                                              else if (data.info == 'DataError'){
                                                $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                                $('#inforz').html('输入的内容超过长度！')
                                              }
                                            },
                                          error: function(){
                                              console.log('404..')
                                            },
                                          })
                                          $('#uprackModal').modal('hide')
                                      })
                                    },
                                    error: function(){
                                        console.log('404..')
                                      },
                                    })
			        }
			// end rack

			// start nd
                        if (cmdbtype == 'netdevice'){
                            $('#upndModal').modal({show:true, backdrop:'static'})   // 弹起修改rack的模态框 
                            $.ajax({
                                type: "GET",
                                url: url,
                                data: {id:updateid, ajaxtype:'ajaxwebnetdevice'},
                                dataType: "json",
                                success: function(data){
                                  console.log(data)
                                  $('#ndtitle').html(data.ndname)
                                  $('#up_ndbrandtype').attr("value", data.brandtype)
                                  $('#up_ndsncode').attr("value", data.sncode)
                                  $('#up_ndowner').attr("value", data.owner)
                                  $('#up_ndnote').attr("value", data.ndnote)
                		  $("#up_ndrunstatus").append('<option>'+data.runstatus+'</option>')
                		  var cmdbstatus = ['在线', '离线']
                		  removeByValue(cmdbstatus, data.runstatus)
                		  for(i=0; i<cmdbstatus.length; i++){
                    			opt = '<option>' + cmdbstatus[i] + '</option>'
                    			$("#up_ndrunstatus").append(opt)
                    		      }

                                  $("#upndBtn").unbind('click').bind('click',function(){   // 点击保存按钮
                                      var brandtype = $('#up_ndbrandtype').val()
                                      var sncode = $('#up_ndsncode').val()
                                      var owner = $('#up_ndowner').val()
                                      var runstatus = $('#up_ndrunstatus').val()
				      var ndnote = $('#up_ndnote').val()
                                      $.ajax({
                                          type: "GET",
                                          url: url,
                                          data: {id:updateid, ajaxtype:'upnetdevice', brandtype:brandtype, sncode:sncode, owner:owner, runstatus:runstatus, ndnote:ndnote},
                                          dataType: "json",
                                          success: function(data){
                                              if (data.info == 'ok'){
                                                $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                                $('#inforz').html('修改成功！')
                                                $('#infoclose').click(function(){
                                                        location.reload()
                                                })
                                              }
                                              else if (data.info == 'DataError'){
                                                $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                                $('#inforz').html('输入的内容超过长度！')
                                              }
                                            },
                                          error: function(){
                                              console.log('404..')
                                            },
                                          })
                                          $('#upndModal').modal('hide')
                                      })
                                    },
                                    error: function(){
                                            console.log('404..')
                                        },
                                    })
                                }
			// end nd

			// start host
			if (cmdbtype == 'host'){
				location.href = '/cmdb/updatehost/?id=' + updateid
                            }
			// end host

			// start vm
			if (cmdbtype == 'vm'){
                            $('#upvmModal').modal({show:true, backdrop:'static'})  // 弹起修改vm的模态框 
                            $.ajax({
                                type: "GET",
                                url: url,
                                data: {id:updateid, ajaxtype:'ajaxwebvm'},
                                dataType: "json",
                                success: function(data){
                                  console.log(data)
                                  $('#vmtitle').html(data.ip)
                                  $('#up_vmosversion').attr("value", data.osversion)
                                  $('#up_vmbusstyle').attr("value", data.busstyle)
                                  $('#up_vmowner').attr("value", data.owner)
                                  $('#up_vmstatus').attr("value", data.runstatus)
				  $('#up_vmnote').attr("value", data.note)
                		  $("#up_vmstatus").append('<option>'+data.runstatus+'</option>')
                		  var cmdbstatus = ['在线', '离线']
                		  removeByValue(cmdbstatus, data.runstatus)
                		  for(i=0; i<cmdbstatus.length; i++){
                    			opt = '<option>' + cmdbstatus[i] + '</option>'
                    			$("#up_vmstatus").append(opt)
                    		      }

                                  $("#upvmBtn").unbind('click').bind('click',function(){   // 点击保存按钮
				      var osversion = $('#up_vmosversion').val()
                                      var busstyle = $('#up_vmbusstyle').val()
                                      var owner = $('#up_vmowner').val()
                                      var runstatus = $('#up_vmstatus').val()
                                      var note = $('#up_vmnote').val()
                                      $.ajax({
                                          type: "GET",
                                          url: url,
                                          data: {id:updateid, ajaxtype:'upvm', osversion:osversion, busstyle:busstyle, owner:owner, runstatus:runstatus, note:note},
                                          dataType: "json",
                                          success: function(data){
                                              if (data.info == 'ok'){
                                            	$('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                            	$('#inforz').html('修改成功！')
                                            	$('#infoclose').click(function(){
                                                	location.reload()
                                                })
                                              }
                                              else if (data.info == 'DataError'){
                                                $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                                $('#inforz').html('输入的内容超过长度！')
                                              }
                                            },
                                          error: function(){
                                              console.log('404..')
                                            },
                                          })
                                          $('#upvmModal').modal('hide')
                                      })
                                    },
                                    error: function(){
                                            console.log('404..')
                                        },
                                    })
                                }
			// end vm
			}
                    }
        	})

      });

  // 机柜的网络设备  修改/删除
  $('.racknetdevice').click(function(){
    var id = $(this).attr('ckid')
    var type = $(this).attr('actiontype')
    if(type == 'update'){
	var url = '/cmdb/update/'
	var type = 'ajaxwebnetdevice'
	// 弹模态框
	// ajax 请求数据
	// ajax 发送数据
        $('#upndModal').modal({show:true, backdrop:'static'})   // 弹起修改idc的模态框                         
            $.ajax({
        	type: "GET",
                url: url,
                data: {id:id, ajaxtype:'ajaxwebnetdevice'},
                dataType: "json",
                success: function(data){
                console.log(data)
                $('#ndtitle').html(data.ndname)
                $('#up_ndbrandtype').attr("value", data.brandtype)
                $('#up_ndsncode').attr("value", data.sncode)
                $('#up_ndowner').attr("value", data.owner)
                $('#up_ndnote').attr('value', data.ndnote)
                $("#up_ndrunstatus").append('<option>'+data.runstatus+'</option>')
                var cmdbstatus = ['在线', '离线']
                removeByValue(cmdbstatus, data.runstatus)
                for(i=0; i<cmdbstatus.length; i++){
                	opt = '<option>' + cmdbstatus[i] + '</option>'
                        $("#up_ndrunstatus").append(opt)
                }

                $("#upndBtn").unbind('click').bind('click',function(){   // 点击保存按钮
                    var brandtype = $('#up_ndbrandtype').val()
                    var sncode = $('#up_ndsncode').val()
                    var owner = $('#up_ndowner').val()
                    var runstatus = $('#up_ndrunstatus').val()
                    var ndnote = $('#up_ndnote').val()
                        $.ajax({
                            type: "GET",
                            url: url,
                            data: {id:id, ajaxtype:'upnetdevice',brandtype:brandtype, sncode:sncode, owner:owner, runstatus:runstatus, ndnote:ndnote},
                            dataType: "json",
                            success: function(data){
                                if (data.info == 'ok'){
                                	$('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                        $('#inforz').html('修改成功！')
                                        $('#infoclose').click(function(){
                                        	location.reload()
                                            })
                                }
                                else if (data.info == 'DataError'){
                                        $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                        $('#inforz').html('输入的内容超过长度！')
                                }
                            },
                            error: function(){
                                console.log('404..')
                            },
                        })
                        $('#upndModal').modal('hide')
                    })
                   },
                   error: function(){
                       console.log('404..')
                       },
                   })
		}
	else if (type == 'delete'){
		var cmdbtype = 'netdevice'
		var url = '/cmdb/update/'
	        $('#deleteModal').modal({show:true, backdrop:'static'})
        	$("#savedeletebtn").unbind('click').bind('click',function(){
                $.ajax({
                        type: "GET",
                        url: "/cmdb/delete/",
                        data: {idlist:id, cmdbtype:cmdbtype},
                        dataType: "json",
                        success: function(data){
                                console.log(data.info)                       
                            if ( data.info == "existports" ){
                                ndname = data.ndname
                                $('#deleteModal').modal('hide')
                                $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                $('#inforz').html(ndname + ' 有端口在使用中，不允许删除！')
                                $('#infoclose').click(function(){
                                	location.reload()
                                    })
                                }
                            else if ( data.info == 'ok' ){
                                dltnum = data.dltnum
                                $('#deleteModal').modal('hide')
                                $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                $('#inforz').html('成功删除'+ '<span style="color:green;margin-left:10px;margin-right:10px">' + dltnum + '</span>' + '条数据')
                                $('#infoclose').click(function(){
                                    location.reload()
                                    })
                                }
                                else if ( data.info == 'one' ){
                                    name = data.name
                                    $('#deleteModal').modal('hide')
                                    $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                    $('#inforz').html('成功删除'+ '<span style="color:green; margin-left:10px; margin-right:10px">' + name + '</span>') 
                                    $('#infoclose').click(function(){
                                        location.reload()
                                    })
                                }
                        }
                    })
        	})
    	    }
  	})

 $(document).ready(function(){
  // 对是否选择进行判断
  $(".btndelete").click(function(){
   if ($("input:checkbox:checked").length == 0)
   {
	// 显示warModal框
	$('#infomodal').modal({show:true, backdrop:'static'}) 
        $('#inforz').html('请先选择数据！')
   }
   else{
        // 把已选择数据保存到result
        var result = new Array();
        $("input[type=checkbox]").each(function () {
        if ($(this).is(":checked")) {
                cmdbtype = $(this).attr("cmdbtype")
                result.push($(this).attr("ckvalue"));
            }
        });
		if(result.length > 1 && (cmdbtype == 'idc' || cmdbtype == 'rack' || cmdbtype == 'netdevice' )){
			if (cmdbtype == 'idc'){
				cmdbtype = '机房'
                        $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                        $('#inforz').html(cmdbtype + ' 不支持批量删除！')
			}
			else if (cmdbtype == 'rack'){
				cmdbtype = '机柜'
				}		
			else if (cmdbtype == 'netdevice'){
				cmdbtype = '网络设备'			
				}
			$('#deleteModal').modal('hide')
                        $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                        $('#inforz').html(cmdbtype + ' 不支持批量删除！')
			return false

		}
        // 点击'#btndelete'显示deleteModal框
        $('#deleteModal').modal({show:true, backdrop:'static'})
        // 点击"#savedeletebtn"，向后台接口发起删除请求，隐藏deleteModal框
	$("#savedeletebtn").unbind('click').bind('click',function(){
		var idlist = result.join(' ')    // 数组转化成字符串
    		$.ajax({
             		type: "GET",
             		url: "/cmdb/delete/",
             		data: {idlist:idlist, cmdbtype:cmdbtype},
             		dataType: "json",
             		success: function(data){
				console.log(data.info)
                   		if( data.info == "idcdeletefail" ){
					idcname = data.idcname
					$('#deleteModal').modal('hide')
                                        $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                        $('#inforz').html(idcname + ' 有机柜在使用中，不允许删除！')
                                        $('#infoclose').click(function(){
                                        	location.reload()
                                        })
				} 
				else if ( data.info == "rackdeletefail" ){
					rackname = data.rackname
                                        $('#deleteModal').modal('hide')
                                        $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                        $('#inforz').html(rackname + ' 有服务器在使用中，不允许删除！')
                                        $('#infoclose').click(function(){
                                                location.reload()
                                        })
				}
				else if ( data.info == "hostdeletefail" ){
					hostip = data.hostip
                                        $('#deleteModal').modal('hide')
                                        $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                        $('#inforz').html(hostip + ' 有虚拟机在使用中，不允许删除！')
                                        $('#infoclose').click(function(){
                                                location.reload()
                                        })
				}
				else if ( data.info == "existports" ){
					ndname = data.ndname
                                        $('#deleteModal').modal('hide')
                                        $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                        $('#inforz').html(ndname + ' 有端口在使用中，不允许删除！')
                                        $('#infoclose').click(function(){
                                                location.reload()
                                        })
				}
				else if ( data.info == 'ok' ){
                                        dltnum = data.dltnum
                                        $('#deleteModal').modal('hide')
                                        $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                        $('#inforz').html('成功删除'+ '<span style="color:green;margin-left:10px;margin-right:10px">' + dltnum + '</span>' + '条数据')
                                        $('#infoclose').click(function(){
                                                location.reload()
                                        })
				}
				else if ( data.info == 'one' ){
					name = data.name
                                        $('#deleteModal').modal('hide')
                                        $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                        $('#inforz').html('成功删除'+ '<span style="color:green; margin-left:10px; margin-right:10px">' + name + '</span>') 
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
   }
   
  });
   });

  $("#btnrefresh").click(
	function(){
    	    if ($("input:checkbox:checked").length == 0)
   		{    
                        $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                        $('#inforz').html('未选择数据！')
			return false
                 	}

	var result = new Array();
	var cmdbtype
        $("input[type=checkbox]").each(function () {
        if ($(this).is(":checked")) {
                result.push($(this).attr("ckvalue"));
		cmdbtype = $(this).attr("cmdbtype")
            }
        });

       $.ajax({
           type: "GET",
           url: "/cmdb/refresh/",
           data: {cmdbtype:cmdbtype, refreshtype:'batch', cmdbid:result.join("-")},
           dataType: "json",
           success: function(data){
		if(data['cmdbinfo']=='cmdbtypeerror'){
			var cmdbtype = data['cmdbtype']
                        $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                        $('#inforz').html(cmdbtype + ' 不支持自动更新！')
		}
		else{
			$("#cmdbautohref").show()
		}

           },
           error:function(){
		alert('server error...')
              },
      })
}
)

// 鼠标点击时，显示机柜的交换机
$("#rackndbtn").click(
    function()
        {
            var ckaction = $(this).attr("ckvalue")
            if(ckaction == 'ckshow')
                {
                        $("#racknd").show("slow")
                        $(this).attr("ckvalue","ckhide")
                        $(this).attr("value","收起上方交换机")
                    }
            else{
                        $("#racknd").hide("slow")
                        $(this).attr("ckvalue","ckshow")
                        $(this).attr("value","显示上方交换机")
                    }
    }
    )

// 点击按钮后，修改a标签的href值，即实现类似form的功能
$("#seabtn").click(function(){
    var searchstr = $("#souinput").val()
    url = "/cmdb/search/?searchstr="+searchstr
    $("#tiaozhuansearch").attr("href",url)
	})

// 修改主机

	function removeByValue(arr, val) {  // 在数组arr里删除元素val
	  for(var i=0; i<arr.length; i++) {
	    if(arr[i] == val) {
	      arr.splice(i, 1);
	      break;
	    }
	  }
	}

	function sw(swname, data){  // 交换机select填充数据
		// "#" + swname : 把变量传进引号
                $("#" + swname).append('<option>'+data[swname]+'</option>')
                var idcnetdevices = $('#hostupdate').attr('ckidcnetdevices').split(",")  // 取存在元素的字符串，再转换成数组
                removeByValue(idcnetdevices, data[swname])
                for(i=0; i<idcnetdevices.length; i++){
                    opt = '<option>' + idcnetdevices[i] + '</option>'
                    $("#" + swname).append(opt)
                    }
		}

	function getList(){
	    var cmdbtype = 'host'
	    var ajaxtype = 'ajaxwebhost'
	    var id = $("#hostupdate").attr('ckid')
	    var url = '/cmdb/update/'
	    $.ajax({
                type: "GET",
                url: url,
                data: {cmdbtype:cmdbtype, ajaxtype:ajaxtype, id:id},
                dataType: "json",
                success: function(data){
		console.log(data.rackhsites)
		$('#hostupdate').attr('ckidcnetdevices', data.idcnetdevices.join(","))  // 在元素里存变量 data.idcnetdevices 以供后续读取，直接读它是递减的
                $("#hsite").append('<option>'+data.hsite+'</option>')
                var rackhsites = data.rackhsites
                removeByValue(rackhsites, data.hsite)
                for(i=0; i<rackhsites.length; i++){
		    // 暂时不做 服务器 网络设备的位置区分
		    // if (rackhsites[i] <= 10){
                    	    opt = '<option>' + rackhsites[i] + '</option>'
                    	    $("#hsite").append(opt)
			// }
                    }

		$("#usize").append('<option>'+data.usize+'</option>')
		var Usizes = ['1U', '2U', '4U', '6U及以上']
		removeByValue(Usizes, data.usize)
		for(i=0; i<Usizes.length; i++){
		    opt = '<option>' + Usizes[i] + '</option>'
		    $("#usize").append(opt)
		    }

                $("#devicetype").append('<option>'+data.devicetype+'</option>')
                var Dtypes = ['物理服务器','宿主机']
                removeByValue(Dtypes, data.devicetype)
                for(i=0; i<Dtypes.length; i++){
                    opt = '<option>' + Dtypes[i] + '</option>'
                    $("#devicetype").append(opt)
                    }

		$("#raid").append('<option>'+data.raid+'</option>')
		var raids = ['RAID 0', 'RAID 1', 'RAID 5', 'RAID 10']
		removeByValue(raids, data.raid)
		for(i=0; i<raids.length; i++){
		    opt = '<option>' + raids[i] + '</option>'
		    $("#raid").append(opt)
		    }

		$("#codeenv").append('<option>'+data.codeenv+'</option>')
		var envs = ['线上', '测试']
		removeByValue(envs, data.codeenv)
		for(i=0; i<envs.length; i++){
		    opt = '<option>' + envs[i] + '</option>'
		    $("#codeenv").append(opt)
		    }

		$("#runstatus").append('<option>'+data.runstatus+'</option>')
		var hoststatus = ['在线', '离线']
		removeByValue(hoststatus, data.runstatus)
		for(i=0; i<hoststatus.length; i++){
		    opt = '<option>' + hoststatus[i] + '</option>'
		    $("#runstatus").append(opt)
		    }
		// 如果ip有数据，就给它填充相应的交换机数据
		if ($('#ip1').val() != ''){
			sw('sw1', data)
		}

		if ($('#ip2').val() != ''){
			sw('sw2', data)
		}

		if ($('#mngip').val() != ''){
			sw('mngsw', data)
		}

             }

	})
    }

// 机柜图

  $(".rackgif").click(
    function(){
	var rackid=$(this).attr("ckvalue")
	$.ajax({
        type: "GET",
        url: "/cmdb/racktable/",
        data: {id:rackid},
        dataType: "json",
        success: function(retdata){
			console.log(retdata)
		    var racktablehtml = '<tr><td style="height:27px"></td></tr>' //待拼装的table部分代码(最上面一行，空行)
		    var sitecodelist = []  //把该机柜服务器的sitecode放在一个列表里，待与行号比较
		    data = retdata['rackhosts']
			console.log(data.length)
		    var dis1u = "height:25px;"
		    rname = retdata['rackname']
		    for (var i = 0; i < data.length; i++){
			sitecode = data[i]['sitecode']
			sitecodelist.push(sitecode)  //列表添加元素
			}
		    for (var raw = 18; raw >= 1; raw--)  //按行号从上到下去比较（使得服务器的位置从下到上倒序排列)
			{
			   inres = $.inArray(raw,sitecodelist)  // 如果行号在sitecodelist里 返回对象的索引（好的是 sitecode在sitecodelist里的索引，与它在data里的一致），否则返回-1
			   if(inres == -1)
				{
				racktd = '<td></td>'
			}
			   else{
                                var hostid = data[inres]['id']
                                var ndname = data[inres]['ndname']
				var devstyle = data[inres]['devstyle']
				var type = data[inres]['type']
				var devstatus = data[inres]['status']
				if(type == '物理服务器' || type == '宿主机')
				{
					var ip = data[inres]['insideip']
					var osversion = data[inres]['osversion']
					var usize = data[inres]['usize']
					if(usize == '2U') {
						if(devstatus == '在线') {
							var imgpath = "/static/imgs/images/cmdb/2u_normal.gif"
						}
						else if(devstatus == '离线') { 
							var imgpath = "/static/imgs/images/cmdb/2u_down.gif"
						}
						var imgstyle = "width:140px;"
						var imgdistance = "height:35px;"
						}
					else if(usize == '1U') {
						if(devstatus == '在线') {
                                                        var imgpath = "/static/imgs/images/cmdb/1u_normal.gif"
                                                }
                                                else if(devstatus == '离线') {  
                                                        var imgpath = "/static/imgs/images/cmdb/1u_down.png"
                                                }
						var imgstyle = "width:135px;"
                                              	var imgdistance = dis1u
                                                }

                                	else if (usize == '4U'){
						if(devstatus == '在线') {
                                        		var imgpath = "/static/imgs/images/cmdb/ser4u_normal.gif"
						}
                                                if(devstatus == '离线') {
                                                        var imgpath = "/static/imgs/images/cmdb/ser4u_down.gif"
                                                }
                                        	var imgstyle = "width:140px;"
                                        	var imgdistance = "height:50px;"
                                	}
					var imgdetail = '/cmdb/hostdetail/?cmdbtype=server&hostid=' + hostid
					var hosttitle = "IP地址：" + ip + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + "型号：" + devstyle + "&nbsp&nbsp&nbsp&nbsp&nbsp" + "操作系统：" + osversion
						}
				else if(type == '网络设备')
				{
					var sn = data[inres]['sn']
					var devstyle = data[inres]['devstyle']
					if (devstyle == 'N77-C7706'){
					    if(devstatus == '在线') {
						var imgpath = "/static/imgs/images/cmdb/n7k_normal.gif"
						}
					    else if(devstatus == '离线') {
						var imgpath = "/static/imgs/images/cmdb/n7k_down.gif"
						}	
					}
					else{
                                            if(devstatus == '在线') {
                                                var imgpath = "/static/imgs/images/cmdb/switch_normal.gif"
                                                }
                                            else if(devstatus == '离线') {
                                                var imgpath = "/static/imgs/images/cmdb/switch_down.png"
                                                }
					}
					var imgdetail = '/cmdb/query/?type=host_switch&sw=' + ndname
					var imgstyle = "width:135px;"
                                	var imgdistance = dis1u
					var hosttitle = "型号：" + devstyle + " " + "SN号：" + sn
					}

				var racktd = '<td style="'+imgdistance+'"><a href="'+imgdetail+'" target="_blank"><img src="'+imgpath+'" style="'+imgstyle+'"  alt="'+ip+'" data-toggle="tooltip" data-placement="left" title="'+hosttitle+'"></img></a></td>'
				}
		    var hosthtml = '<tr>' + racktd + '</tr>'
		    var racktablehtml = racktablehtml + hosthtml
		}	
		    var racktablehtml = racktablehtml + '<tr><td style="height:24px"></td></tr>'  // 加最下面一行（空行）
		    $('#rackname').html(rname)
        	    $('#rackhtml').html(racktablehtml) 
		    $(function () { $("[data-toggle='tooltip']").tooltip(); });
             },
        error:function(){
        	$('#rackhtml').html('404...')
                },
        })
	
	$('#racktable').modal({show:true, backdrop:'static'})
	$('#racktableclosebtn').click(function(){
		$('#racktable').modal('hide')
	})

	})



// table 点击行的时候 把checkbox选中
  $(".cklist tr").each(function(){    
            $(this).children().click(function(e){    
                $(e.target).parent("tr.ckitem").each(function(){  
                    if($(this).find(":checkbox").is(":checked")){  
                        $(this).find(":checkbox").attr("checked",false);  
                    }else{  
                        $(this).find(":checkbox").attr("checked",true);  
                    }  
                });  
        });    
  }); 

// table的 checkbox 样式
  function changeState(el) {
    if (el.readOnly) el.checked=el.readOnly=false;
    else if (!el.checked) el.readOnly=el.indeterminate=true;
  }

// form和update可复用的，填容量后 点击添加按钮 增加内存或磁盘
$("#memadd").click(
function()
{
var mem = $.trim($("#memsize").val())  // 获取输入框内容（去掉两边的字符串）
if(mem == ''){
    return
}
inputval = mem + 'GB' //获取输入框的输入
ckval = $("#memory").val()   //获取上一次的结果ckval
ckval = ckval + " " + inputval  //把结果ckval 和 输入的值累加
$("#memory").val(ckval)  //修改
}
)

$("#diskadd").click(
function()
{
var disk = $.trim($("#disksize").val())
if(disk == ''){
    return
}
inputval = disk + $("#diskgt").val() //获取输入框的输入
ckval = $("#disk").val()   //获取上一次的结果ckval
ckval = ckval + " " + inputval  //把结果ckval 和 输入的值累加
$("#disk").val(ckval)  //修改
}
)

