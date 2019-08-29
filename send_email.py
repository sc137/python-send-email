#! /usr/bin/env python3
# send_email.py
# sable cantus
# https://cantus.us
# Aug 2019

import os
import sys
import time
import datetime
import smtplib
# store email username and password in the keyring module
# pip3 install keyring
import keyring
# from credentials import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

##########################################################
#
# send later by setting the time to delay until
#                               YYYY, MM, DD, HH, MM, SS
delay_until = datetime.datetime(2019, 8, 26, 13, 40, 0)
#
##########################################################

# specify a file to attach in the same directory
filename = ''

# store your username and password with the keyring modue
# keyring set system email_username
# keyring set system email_password
username = keyring.get_password('system', 'email_username')
password = keyring.get_password('system', 'email_password')

# insert your smtp server here
mail_server = ''                

# list of email addresses to send to
listFile = "email_recipients.txt"

# check for the recipient list
if os.path.isfile(listFile):
    pass
else:
    print("No {} present.".format(listFile))
    sys.exit()                      # exit if no recipients

# put a line in the logfile for each send
if os.path.isfile('send_log.txt'):
    pass
else:
    print("No log file present...")
    sys.exit()                      # exit if no log file

# timestamp the log entries
timestamp = datetime.datetime.now()
timestamp = timestamp.strftime('%Y-%m-%-d %H:%M:%S')

# message of the email to send
message_file  = "message.txt"

if os.path.isfile(message_file):
    f = open(message_file, "r")
    body = ''.join(f.readlines())
    f.close()
else:
    print('no message file {}'.format(message_file))
    sys.exit()                      # exit if no message file

##########################################################
#
# pause everything until the delay_until time...
while datetime.datetime.now() < delay_until:
    time.sleep(1)
#
##########################################################

# opens the list file and send email to each recipient (one per line)
email_list = open(listFile)
for recipient in email_list.readlines():

    msg = MIMEMultipart()
    msg['Subject'] = '[TESTING] Automated message status'
    msg['From'] = ''
    # msg['Reply-To'] = ''
    msg['To'] = recipient

    # attach the body text to the msg
    msg.attach(MIMEText(body, 'plain'))

    # is there a file to attach?
    if len(filename) > 0:
        attachment = open(filename, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)

    server = smtplib.SMTP(mail_server, 587)
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.set_debuglevel(0)                # set to 1 for info, 0 for no info
    server.send_message(msg)
    server.quit()
    
    # add the log entry
    logEntry = timestamp + ' sent message to ' + recipient
    logFile = open('send_log.txt', 'a+')
    logFile.write(logEntry)
    logFile.close()
