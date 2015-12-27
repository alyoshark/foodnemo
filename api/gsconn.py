import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from retrying import retry

import config
import sendmail


def order_writer():
    conns = {}
    notify = sendmail.mail_sender()

    def init_conn():
        conns['credentials'] = SignedJwtAssertionCredentials(
            config.JSON_KEY['client_email'],
            config.JSON_KEY['private_key'],
            config.GOAUTHSCOPE,
        )
        conns['reader'] = gspread.authorize(conns['credentials'])
        conns['book'] = conns['reader'].open_by_key(config.TEST_BOOKID)
        try:
            conns['sheet'] = conns['book'].worksheet(config.SHEET)
        except gspread.exceptions.WorksheetNotFound:
            conns['sheet'] = conns['book'].add_worksheet(title=config.SHEET, rows='500', cols='8')

    # @retry(wait_exponential_multiplier=1000, wait_exponential_max=1000000)
    def dump_order(order_list):
        try:
            ids = conns['sheet'].col_values(1)
            if ids:
                maxid, err_offset = 0, 0
                for i in ids:
                    try:
                        maxid = max(maxid, int(i))
                    except:
                        # On error, we skip the ID by one just to be safe
                        err_offset += 1
                maxid += err_offset
            else:
                maxid = 0
            for idx, order in enumerate(order_list):
                order_id = idx + maxid + 1
                write_order(order_id, order)
            notify(config.GMAIL_CRED['sender'], 'Order Summary', order2email(order_list))
        except:
            init_conn()

    def write_order(order_id, order):
        conns['sheet'].update_cell(order_id, 1, order_id)
        for col, val in zip(xrange(2, 9), order):
            conns['sheet'].update_cell(order_id, col, val)

    def order2email(order_list):
        msg = 'Hi,\nBelow are the orders from last aggregation mail:\n\n'
        msg += '\n'.join('\t'.join(str(i) for i in order) for order in order_list)
        return msg

    init_conn()
    return dump_order


if __name__ == '__main__':
    pass
