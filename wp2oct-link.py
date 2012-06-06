import xml.etree.ElementTree as et
import sys
from datetime import datetime

xml_wp_ns = '{http://wordpress.org/export/1.1/}' 

def generate_from_file(file_path):
    with open(file_path, 'r') as f:
        xml_str = f.read()
    root = et.fromstring(xml_str )
    channel = root.find('channel')
    for item in channel.iterfind('item'):
        print create_url(item)

def create_url(xml_item):
    title = xml_item.find('title').text
    old_link = xml_item.find('link').text
    post_date_str = xml_item.find(xml_wp_ns + 'post_date').text
    post_date = datetime.strptime(post_date_str, '%Y-%m-%d %H:%M:%S')

    new_link = "/%s/%s/%s/%s" % (post_date.year, post_date.month, post_date.day, 
            get_ocotoed_title(title))

    return '%s -> %s ' % (old_link, new_link)

def get_ocotoed_title(title):
    return title.replace(' ', '-').replace('"', '').replace('#', '') \
                .replace(':', '').replace('.','').replace('\'', '') \
                .replace(',', '').replace('"', '')

if __name__ == '__main__':
    if not sys.argv > 1:
        print('Usage: python wp2oct-linl.py exported_wordpress.xml')
    generate_from_file(sys.argv[1])
