if (-not (Test-Path -path "C:\zabbix_agent\conf\zabbix_agentd.win.conf")) {
    "zabbix 配置文件不存在，无法读取虚机uuid 按任意键退出"; Read-Host | Out-Null ; Exit
}
$zabbix_conf = "$(Get-Content C:\zabbix_agent\conf\zabbix_agentd.win.conf)"
$reg = "\b[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}\b"
$h = $zabbix_conf -match $reg
$zabbix_uuid = $matches[0]

$telegraf_conf = Get-Content .\telegraf\telegraf.conf 
$t = $telegrafConf -match $reg
$uuid_to_replace = $matches[0]

$new_content = $telegraf_conf -replace "$uuid_to_replace", "$zabbix_uuid"
# telegraf.exe 只能解析编码为ASCII格式的配置文件
$new_content | Out-File .\telegraf\telegraf.conf -Encoding ASCII

Copy-Item -recurse telegraf "C:\Program Files\telegraf"

"停止telegraf 并删除telegraf 服务";
C:\Program Files\telegraf\telegraf.exe --service stop
C:\Program Files\telegraf\telegraf.exe --service uninstall
"安装telegraf服务，并启动telegraf";
C:\Program Files\telegraf\telegraf.exe --service install
C:\Program Files\telegraf\telegraf.exe --service start

"telegraf 配置已更新，并设置为windows服务，按任意键退出"; Read-Host | Out-Null ; Exit