import json
import logging
import datetime as dt

DATESTR = dt.date.today().strftime('%Y%m%d')

LOGFILE = DATESTR + '.log'
LOGLEVEL = logging.ERROR

GOAUTHFILE = 'fn-dev-015c422fd6c5.json'
JSON_KEY = json.load(open(GOAUTHFILE))

GOAUTHSCOPE = ['https://spreadsheets.google.com/feeds']
BOOKID = '1zVmgdtAHi0oCD3F0RBFrAyypdgu1Qol8lX_g5wqxT9k'
TEST_BOOKID = '1CKdrx8nmFLs0pU52l7b_rHOBytQK4Z5Npz78RHtEuAM'
SHEET = DATESTR
