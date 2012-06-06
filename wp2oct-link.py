import xml.etree.ElementTree as et
import sys
import slugify
from datetime import datetime

xml_wp_ns = '{http://wordpress.org/export/1.1/}' 

def generate_from_file(file_path):
    with open(file_path, 'r') as f:
        xml_str = f.read()
    root = et.fromstring(xml_str )
    channel = root.find('channel')
    site_url = channel.find('link').text
    pmap = {}
    for item in channel.iterfind('item'):
        if item.find(xml_wp_ns + 'status').text.lower() == 'publish':
            create_url(item, site_url, pmap)

    generate_pid_map(pmap)

def create_url(xml_item, site_url, pmap):
    title = xml_item.find('title').text
    title = unicode(title)
    old_link = xml_item.find('link').text
    old_link = old_link.replace(site_url, '')
    post_date_str = xml_item.find(xml_wp_ns + 'post_date').text
    post_date = datetime.strptime(post_date_str, '%Y-%m-%d %H:%M:%S')

    wp_id = xml_item.find(xml_wp_ns + 'post_id').text

    new_link = "/blog/%s/%02d/%02d/%s/" % (post_date.year, post_date.month, post_date.day, 
            slugify.slugify(title))
    
    pmap[wp_id] = new_link
    #print('rewrite ^{}$ {} permanent;'.format('/?p=' + wp_id, new_link))
    print('rewrite ^{}$ {} permanent;'.format(old_link, new_link))

def generate_pid_map(pmap):
    #print('if ($args ~* p=\d+) {')
    for pid, new_link in pmap.iteritems():
        print('if ($args = p=%s) {' % pid)
        print('  return 301 %s; }' % new_link)

    #print('}')

if __name__ == '__main__':
    if not sys.argv > 1:
        print('Usage: python wp2oct-linl.py exported_wordpress.xml')
    generate_from_file(sys.argv[1])
