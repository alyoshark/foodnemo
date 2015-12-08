import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

import config

def mail_sender():
    conns = {}

    def init_conn():
        conns['smtp'] = smtplib.SMTP('smtp.gmail.com', 587)
        conns['smtp'].ehlo()
        conns['smtp'].starttls()
        conns['smtp'].ehlo()
        conns['smtp'].login(config.GMAIL_CRED['username'], config.GMAIL_CRED['password'])

    # @retry(wait_exponential_multiplier=1000, wait_exponential_max=1000000)
    def sendmail(recv, title, msg):
        mail = MIMEMultipart()
        mail['From'] = config.GMAIL_CRED['sender']
        mail['To'] = recv
        mail['Subject'] = title
        mail.attach(MIMEText(msg, 'plain'))
        try:
            conns['smtp'].sendmail(config.GMAIL_CRED['sender'], recv, mail.as_string())
        except:
            raise
            init_conn()
            conns['smtp'].sendmail(config.GMAIL_CRED['sender'], recv, mail.as_string())

    init_conn()
    return sendmail
