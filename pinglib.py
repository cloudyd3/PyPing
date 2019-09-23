import platform
import socket
import subprocess


def port_check(host, port):
    ping_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = ping_socket.connect_ex((host, port))
    ping_socket.close()
    return result == 0


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
        command = ['ping -c 1', host]
        return subprocess.run(command) == 0


def get_hostname(host):
    return socket.gethostbyaddr(host)[0]


def ssh_uptime(login, host):
    ssh = subprocess.Popen(['ssh', '{}@{}'.format(login, host), 'uptime'], stdout=subprocess.PIPE)
    response = ssh.communicate()[0].decode("utf-8")
    return response


def ssh_running_services(login, host):
    ssh = subprocess.Popen(['ssh', '{}@{}'.format(login, host), 'systemctl | grep running && exit'], stdout=subprocess.PIPE)
    response = ssh.communicate()[0].decode("utf-8")
    return response
