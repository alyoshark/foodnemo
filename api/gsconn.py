import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from retrying import retry

import config


def order_writer():
    conns = {}

    def init_conn():
        conns['credentials'] = SignedJwtAssertionCredentials(
            JSON_KEY['client_email'],
            JSON_KEY['private_key'],
            config.GOAUTHSCOPE,
        )
        conns['reader'] = gspread.authorize(conns['credentials'])
        conns['book'] = conns['reader'].open_by_key(config.TEST_BOOKID)
        conns['sheet'] = conns['book'].worksheet(config.SHEET)

    # @retry(wait_exponential_multiplier=1000, wait_exponential_max=1000000)
    def dump_order(order_list):
        try:
            ids = conns['sheet'].col_values(1)
            if ids:
                maxid = max(ids)
            else:
                ids = 0
            for idx, order in enumerate(order_list):
                order_id = idx + maxid + 1
                write_order(order_id, order)
        except:
            init_conn()
            raise

    def write_order(order_id, order):
        conns['sheet'].update_cell(order_id, 1, order_id)
        for col, val in zip(xrange(2, 5), order):
            conns['sheet'].update_cell(order_id, col, val)

    init_conn()
    return dump_order


if __name__ == '__main__':
    pass
