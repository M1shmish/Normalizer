from bs4 import BeautifulSoup
import json
import requests


def get_html_from_url(url, num_lines):
    response = requests.get(url)
    lines = response.text.split('\n')
    truncated_lines = lines[:num_lines]
    truncated_html = '\n'.join(truncated_lines)
    return truncated_html


def html_to_json(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    json_data = {}
    json_data['name'] = soup.title.string.strip() if soup.title else None
    json_data['children'] = parse_html_elements(soup.find_all())

    return json.dumps(json_data, separators=(',', ':'))

def parse_html_elements(elements):
    children = []
    for element in elements:
        if element.name:
            child = {}
            child['name'] = element.name
#            child['attrs'] = element.attrs
            child['text'] = element.get_text().strip()
            child['children'] = parse_html_elements(element.find_all())
            children.append(child)
    return children


def main():
    url = {"URL"}
    num_lines = {Number of lines to get}
    html = get_html_from_url(url, num_lines)
    json_ = html_to_json(html)
    print(json_)

main()
