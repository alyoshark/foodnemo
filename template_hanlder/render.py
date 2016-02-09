import os
import sys
import codecs

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


def main():
    info = {
        'dishes': get_dishes(),
        'is_closed': sys.argv[1]=='closed',
        'mask_msg': sys.argv[2].split('|'),
    }
    gen_files('index.html', info)
    gen_files('css/main.css', info)
    gen_files('js/main.js', info)


if __name__ == '__main__':
    main()
