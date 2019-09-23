import multiprocessing
import socket
import terminaltables.github_table

import pinglib


def output(host):
    ping_status = pinglib.ping(host)
    if ping_status is False:
        host_info = [host, [False]]
        return host_info
    else:
        try:
            host_info = [host, [ping_status[0], ping_status[1], pinglib.get_hostname(host)]]
            return host_info
        except socket.herror:
            host_info = [host, [ping_status[0], ping_status[1], None]]
            return host_info


def main():
    address_pool = []

    ip_from = input('Input from in x.x.x.x format (Default: 192.168.1.0) ').split('.')
    if ip_from[0] == '':
        ip_from = '192.168.1.0'.split('.')
    ip_to = input('Input to in x.x.x.x format (Default 192.168.1.255) ').split('.')
    if ip_to[0] == '':
        ip_to = '192.168.1.255'.split('.')

    print('Building address pool, please wait...')
    ip_from = list(map(int, ip_from))
    pool = multiprocessing.Pool(100)
    while int(ip_from[3]) <= int(ip_to[3]):
        address_pool.append('{}.{}.{}.{}'.format(ip_from[0], ip_from[1], ip_from[2], ip_from[3]))
        ip_from[3] = int(ip_from[3] + 1)

    result = pool.map(output, address_pool)

    print('Building complete!')

    table_data = [['#', 'IP Address', 'Status', 'Ping time', 'Hostname', "TTL"]]

    for i in range(len(result)):
        if result[i][1][0]:
            info = [i, result[i][0], 'Online', result[i][1][0], result[i][1][2], result[i][1][1]]
            table_data.append(info)
        else:
            pass

    table = terminaltables.GithubFlavoredMarkdownTable(table_data)
    print(table.table)

    def actions_menu():
        uinput = input('Select ID to check: ')
        host_id = result[uinput][0]
        select = int(input('1. Check uptime (Linux only, requires SSH)\r\n'
                           '2. Check running services (Linux only, requires SSH)\r\n'
                           'Select task: '))
        login = input('Input server login: ')
        if select == 1:
            print(pinglib.ssh_uptime(login, host_id))
        elif select == 2:
            print(pinglib.ssh_running_services(login, host_id))
        close = input('Anything else? y/n ')
        if close == 'y':
            print(chr(27) + "[2J")
            print(table.table)
            actions_menu()
        elif close == 'n':
            exit()

    actions_menu()


if __name__ == '__main__':
    main()
