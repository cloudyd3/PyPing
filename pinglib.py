import platform
import socket
import subprocess


# def port_check(host, port):
#    ping_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    result = ping_socket.connect_ex((host, port))
#    ping_socket.close()
#    return result == 0


def ping(host):
    if platform.system().lower() == 'windows':
        ping_request = subprocess.Popen(['ping', '-n', '1', host], stdout=subprocess.PIPE)
        response = (ping_request.communicate()[0]).decode("utf-8").splitlines()
        if 'ms' in response[-6]:
            ping_time = (response[-1].split(' = ')[-1])
            ttl = (response[-6].split('TTL=')[-1])
            return [ping_time, ttl]
        else:
            return False
    else:
        ping_request = subprocess.Popen(['ping', '-c', '1', host], stdout=subprocess.PIPE)
        response = (ping_request.communicate()[0]).decode("utf-8").splitlines()
        if 'ms' in response[-4]:
            ping_time = (response[-4].split('=')[-1])
            ttl = (response[-4].split('ttl=')[-1])
            return [ping_time, ttl]
        else:
            return False


def output(host):
    ping_status = ping(host)
    if ping_status is False:
        host_info = [host, [False]]
        return host_info
    else:
        try:
            host_info = [host, [ping_status[0], ping_status[1], get_hostname(host)]]
            return host_info
        except socket.herror:
            host_info = [host, [ping_status[0], ping_status[1], None]]
            return host_info



def get_hostname(host):
    return socket.gethostbyaddr(host)[0]


def ssh_uptime(login, host):
    ssh = subprocess.Popen(['ssh', '{}@{}'.format(login, host), 'uptime'], stdout=subprocess.PIPE)
    response = ssh.communicate()[0].decode("utf-8")
    return response


def ssh_running_services(login, host):
    ssh = subprocess.Popen(['ssh', '{}@{}'.format(login, host), 'systemctl | grep running && exit'],
                           stdout=subprocess.PIPE)
    response = ssh.communicate()[0].decode("utf-8")
    return response


def nmap_scan(host):
    try:
        nmap_o_v = subprocess.Popen(['nmap -O -v', host], stdout=subprocess.PIPE)
        response = nmap_o_v.communicate()[0].decode("utf-8")
        return response
    except FileNotFoundError:
        return FileNotFoundError
