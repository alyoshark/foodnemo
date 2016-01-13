import csv
import json
import datetime as dt


def parse_order(line):
    timestamp, data = line.split('|', 1)
    data = json.loads(data.decode('string_escape'))
    dishes = ', '.join(
        '%s: (%d - %.1f)' % (i['name'], i['count'], i['price'])
        for i in data['dishes']
    )
    contact = data['contact']
    phone = int(contact['phone'])
    slot = int(contact['slot'])
    zipcode = int(contact['zipcode'])
    name = contact['name']
    location = contact['location']
    remark = contact['remark']
    return (timestamp, phone, slot, zipcode, name, location, remark, dishes)


def populate_data(f):
    order_list = []
    while True:
        l = f.readline()
        if not l or len(l) == 0:
            break
        else:
            try:
                order = parse_order(l)
                order_list.append(order)
            except:
                print l
                print l.decode('string_escape')
                continue
    return order_list


def main(file_log):
    with open(file_log) as f:
        order_list = populate_data(f)
    with open('/opt/proj/foodnemo/private/today.csv', 'w') as f:
        cw = csv.writer(f)
        for i in order_list:
            cw.writerow(i)


if __name__ == '__main__':
    main('/opt/proj/foodnemo/raw/test-order.json')
