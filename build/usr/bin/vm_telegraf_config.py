#coding:utf-8
#从zabbix配置文件中找到 uuid
def get_uuid():
        zabbix_config = '/etc/zabbix/zabbix_agentd.conf'
        with open(zabbix_config, 'r') as f:
                lines = f.readlines()
                for x in lines:
                        if x.startswith('Hostname'):
                                return x.split('=')[1].strip()

def create_telegraf_config(uuid):
        _files_for_linux =  (
                        "[global_tags]\n"
                        "vm_uuid = \"{0}\"\n"
                        "vm_os_type = \"linux\"\n"
                        "[agent]\n"
                        "interval = \"60s\"\n"
                        "round_interval = true\n"
                        "metric_batch_size = 1000\n"
                        "metric_buffer_limit = 10000\n"
                        "collection_jitter = \"5s\"\n"
                        "flush_interval = \"60s\"\n"
                        "flush_jitter = \"10s\"\n"
                        "debug = false\n"
                        "quiet = false\n"
                        "hostname = \"{0}\"\n"
                        "omit_hostname = false\n"
                        "logfile = \"/var/log/wocloud_monitor.log\"\n"
                        "[[outputs.socket_writer]]\n"
                        "address = \"tcp4://169.254.169.254:8094\"\n"
                        "data_format = \"influx\"\n"
                        "[[inputs.cpu]]\n"
                        "percpu = false\n"
                        "totalcpu = true\n"
                        "fielddrop = [\"time_*\"]\n"
                        "name_prefix = \"vm_linux\"\n"
                        "[[inputs.disk]]\n"
                        "ignore_fs = [\"tmpfs\", \"devtmpfs\", \"devfs\"]\n"
                        "name_prefix = \"vm_linux\"\n"
                        "[[inputs.diskio]]\n"
                        "name_prefix = \"vm_linux\"\n"
                        "[[inputs.kernel]]\n"
                        "name_prefix = \"vm_linux\"\n"
                        "[[inputs.mem]]\n"
                        "name_prefix = \"vm_linux\"\n"
                        "[[inputs.processes]]\n"
                        "name_prefix = \"vm_linux\"\n"
                        "[[inputs.swap]]\n"
                        "name_prefix = \"vm_linux\"\n"
                        "[[inputs.system]]\n"
                        "name_prefix = \"vm_linux\"\n"
                        "[[inputs.net]]\n"
                        "name_prefix = \"vm_linux\"\n"
                        "[[inputs.netstat]]\n"
                        "name_prefix = \"vm_linux\"\n".format(uuid,uuid))
        with open('/etc/telegraf/telegraf.conf', 'w') as f:
                f.write(_files_for_linux)

def main():
    uuid = get_uuid()
    create_telegraf_config(uuid)
if __name__ == '__main__':
    main()
