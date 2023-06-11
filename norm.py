from bs4 import BeautifulSoup
import json
import requests


def get_html_from_url(url, num_lines=60):
    response = requests.get(url)
    lines = response.text.split('\n')
    truncated_lines = lines[:num_lines]
    truncated_html = '\n'.join(truncated_lines)
    return truncated_html


def convert_html_to_json(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    data = {}
    data['Server Version'] = soup.find('dl').find('dt').get_text().split(': ')[1]

    server_mpm_dt = soup.find('dt', string='Server MPM:')
    data['Server MPM'] = server_mpm_dt.find_next('dt').get_text() if server_mpm_dt else None

    server_built_dt = soup.find('dt', string='Server Built:')
    data['Server Built'] = server_built_dt.find_next('dt').get_text().split(': ')[1] if server_built_dt else None

    current_time_dt = soup.find('dt', string='Current Time:')
    current_time = current_time_dt.find_next('dt').get_text().split(': ')[1] if current_time_dt else None

    restart_time_dt = soup.find('dt', string='Restart Time:')
    restart_time = restart_time_dt.find_next('dt').get_text().split(': ')[1] if restart_time_dt else None

    data['Times'] = {'Current Time': current_time, 'Restart Time': restart_time}

    stats_dl = soup.find('dt', string='Server uptime:').find_next('dl') if soup.find('dt', string='Server uptime:') else None
    server_stats = {}
    if stats_dl:
        for dt in stats_dl.find_all('dt'):
            key = dt.get_text().split(': ')[0]
            value = dt.get_text().split(': ')[1]
            server_stats[key] = value
    data['Server Stats'] = server_stats

    table = soup.find('table')
    rows = table.find_all('tr')
    table_data = []
    for row in rows[2:]:
        columns = row.find_all('td')
        slot = columns[0].get_text()
        pid = columns[1].get_text()
        stopping = columns[2].get_text()
        connections_total = columns[3].get_text()
        connections_accepting = columns[4].get_text()
        threads_busy = columns[5].get_text()
        threads_idle = columns[6].get_text()
        async_connections_writing = columns[7].get_text()
        async_connections_keep_alive = columns[8].get_text()
        async_connections_closing = columns[9].get_text()

        row_data = {
            'Slot': slot,
            'PID': pid,
            'Stopping': stopping,
            'Connections': {
                'Total': connections_total,
                'Accepting': connections_accepting
            },
            'Threads': {
                'Busy': threads_busy,
                'Idle': threads_idle
            },
            'Async Connections': {
                'Writing': async_connections_writing,
                'Keep-alive': async_connections_keep_alive,
                'Closing': async_connections_closing
            }
        }
        table_data.append(row_data)

    data['Table Data'] = table_data

    json_data = json.dumps(data, indent=4)
    return json_data


def main():
    url = input("Please provide URL")
    num_lines = input("Please provide number of lines")
    html = get_html_from_url(url, num_lines=60)
    json_data = convert_html_to_json(html)

    output_file = 'output.log'
    with open(output_file, 'w') as file:
        file.write(json_data)

    print(f"JSON output saved to {output_file}")


if __name__ == '__main__':
    main()
