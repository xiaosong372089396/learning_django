<td><input type="checkbox"></td>
<td><%= host_name %></td>
<td><a href="http://<%= monitor_server %>/applications.php?groupid=0&hostid=<%= host_id %>" target="_blank">应用集</a><%= applications_count %></td>
<td><a href="http://<%= monitor_server %>/items.php?filter_set=1&hostid=<%= host_id %>" target="_blank">监控项</a><%= items_count %></td>
<td><a href="http://<%= monitor_server %>/triggers.php?groupid=0&hostid=<%= host_id %>" target="_blank">触发器</a><%= triggers_count %></td>
<td><a href="http://<%= monitor_server %>/graphs.php?groupid=0&hostid=<%= host_id %>" target="_blank">图形</a><%= graphs_count %></td>
<td><a href="http://<%= monitor_server %>/host_discovery.php?&hostid=<%= host_id %>" target="_blank">自动发现</a><%= discovery_count %></td>
<td><%= interface %></td>
