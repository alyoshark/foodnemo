import os
import sys
import codecs
import datetime as dt
from urlparse import parse_qs

from jinja2 import Template

from parse import get_dishes


TPL_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.join(os.path.dirname(TPL_DIR), 'prototype')


def gen_params(is_closed, mask_msg):
    return {
        'dishes': get_dishes(),
        'is_closed': is_closed,
        'mask_msg': mask_msg,
    }


def gen_files(filename, info):
    with codecs.open(os.path.join(TPL_DIR, filename), 'r', 'utf-8') as f:
        tpl = Template(f.read())
    with codecs.open(os.path.join(STATIC_DIR, filename), 'w', 'utf-8') as f:
        f.write(tpl.render(info=info))


def test():
    info = {
        'dishes': get_dishes(),
        'is_closed': sys.argv[1]=='closed',
        'mask_msg': sys.argv[2].split('|'),
    }
    gen_files('index.html', info)
    gen_files('css/main.css', info)
    gen_files('js/main.js', info)


def main(logline):
    time_str, query_str = logline.split('|', 2)
    timenow = dt.datetime.now()
    timethen = dt.datetime.strptime(time_str.split('+')[0], '%Y-%m-%dT%H:%M:%S')
    if (timenow - timethen).seconds <= 60:
        data = parse_qs(query_str)
        msg = [m for m in data['msg'] if m and len(m) > 0]
        intro = [m for m in data['intro'] if m and len(m) > 0]
        # {'msg': ['We would resume on Feb 15', 'Please join us then :)'], 'is_closed': ['0']}
        if msg and intro:
            info = {
                'dishes': get_dishes(),
                'is_closed': data['is_closed'][0] != '0',
                'mask_msg': msg,
                'intro': intro,
            }
            print info
            gen_files('index.html', info)
            gen_files('css/main.css', info)
            gen_files('js/main.js', info)
        else:
            print "No masking message, skip"
    else:
        print "No request..."


if __name__ == '__main__':
    main(sys.stdin.readline())
