function server_stop(instanceid){
    url = '/assets/stop/';
    var info = confirm('确定停止服务器吗');
    if (info) {
        $.getJSON(url,{instanceid:instanceid},function(result){
            alert(result);
        });
    };
}


function server_start(instanceid){
    url = '/assets/start/';
    var info = confirm('确定启动服务器吗')
    if (info) {
        $.getJSON(url,{instanceid: instanceid},function(result){
            alert(result);
        });
    };
}


function server_reboot(instanceid){
    url = '/assets/reboot/';
    var info = confirm('确定重启该服务器吗');
    if (info) {
        $.getJSON(url,{instanceid: instanceid}, function(result){
            alert(result);
        });
    };
}


function change_group(instanceid){
    url = '/assets/server_change_group/';
    //var name = $("#server_group").val();
    var name = $("#server_group" + instanceid).find("option:selected").text()
    var info = confirm('确定修改分组么');
    if (info) {
        $.getJSON(url, {instanceid: instanceid, server_name: name}, function(result){
            alert(result);
        });
    };
}


function item_return(item_id){
    url = '/assets/item_return/';
    var info = confirm("确定归还？");
    if(info) {
        $.getJSON(url, {item_id: item_id}, function(result){
            alert(result);
            location.reload();
        });
    };
}

