# -*- coding: utf-8 -*-

from logging import getLogger
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import yaml

from dir_path import MAILER_CONFIG_PATH_NAME

logger = getLogger(__name__)


def load_gmail_config():
    with open(MAILER_CONFIG_PATH_NAME)as f:
        mailer_config_dict = yaml.safe_load(f)

    return mailer_config_dict


def send_message_from_gmail(title, msg):

    charset = "utf-8"

    config_dict = load_gmail_config()

    account = config_dict['account']
    password = config_dict['password']
    to_address = config_dict['to_address'].split(';')

    # メール本文
    mail_obj = MIMEText(msg, "plain", charset)
    # メールタイトル
    mail_obj["subject"] = Header(title.encode(charset), charset)

    # Gmailでのメール送信は「smtplib.SMTP_SSL」を用いてポート番号465を使用すること。
    smtp_obj = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    # ehlo()でSMTPサーバーに挨拶しておきましょう。挨拶しておかないとログインできません！
    smtp_obj.ehlo()
    # ログイン
    smtp_obj.login(account, password)
    # メール送信
    smtp_obj.sendmail(account, to_address, mail_obj.as_string())
    # ログアウト
    smtp_obj.quit()


if __name__ == '__main__':
    send_message_from_gmail('テストじゃ', 'こりゃー')
    pass
