import multiprocessing

import terminaltables.github_table

import pinglib


def main():
    address_pool = []

    ip_from = input('Input from in x.x.x.x format (Default: 192.168.1.0) ').split(
        '.')
    if ip_from[0] == '':
        ip_from = '192.168.1.0'.split('.')
    # Определение нижнего диапазона подсети
    ip_to = input('Input to in x.x.x.x format (Default 192.168.1.255) ').split(
        '.')
    if ip_to[0] == '':
        ip_to = '192.168.1.255'.split('.')
    # Определение верхнего диапазона подсети

    print('Building address pool, please wait...')
    ip_from = list(map(int, ip_from))
    ip_to = list(map(int, ip_to))
    while int(ip_from[3]) <= int(ip_to[3]):
        address_pool.append('{}.{}.{}.{}'.format(ip_from[0], ip_from[1], ip_from[2], ip_from[3]))
        ip_from[3] = int(ip_from[3] + 1)
    # Построение базы IP аддрессов

    pool = multiprocessing.Pool(100)
    result = pool.map(pinglib.output, address_pool)
    # Скармливание базы IP аддрессов мультипроцессингу

    print('Building complete!')
    print('Please note that OS type detection is based on TTL and may not be accurate. Please use nmap scan for more '
          'accurate results.')

    table_data = [['#', 'IP Address', 'Status', 'Ping time', 'Hostname', "TTL", "OS type"]]
    # определение заголовков таблицы

    for i in range(len(result)):
        if result[i][1][0]:
            if 54 < int(result[i][1][1]) <= 64:
                os_type = '*nix'
            elif 118 < int(result[i][1][1]) <= 128:
                os_type = 'Windows'
            elif 244 < int(result[i][1][1]) <= 254:
                os_type = 'Solaris/AIX'
            else:
                os_type = 'Unknown'
            info = [i, result[i][0], 'Online', result[i][1][0], result[i][1][2], result[i][1][1], os_type]
            table_data.append(info)
        else:
            pass
    # сбор данных таблицы

    table = terminaltables.GithubFlavoredMarkdownTable(table_data)
    print(table.table)

    # выод таблицы

    def actions_menu():
        id_input = int(input('Select ID to check: '))
        host_id = result[id_input][0]
        select = int(input('1. Check uptime (Linux only, requires SSH)\r\n'
                           '2. Check running services (Linux only, systemd only, requires SSH)\r\n'
                           '3. Perform nmap scan for more accurate os detection (experemental)\r\n'
                           'Select task: '))
        if select == 1:
            login = input('Input server login: ')
            print(pinglib.ssh_uptime(login, host_id))
        if select == 2:
            login = input('Input server login: ')
            print(pinglib.ssh_running_services(login, host_id))
        if select == 3:
            print(pinglib.nmap_scan(host_id))

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
