#! /usr/bin/env python3
# send_email.py my_email_list.txt
# An email utility to send messages to a list of recipients

import os
import sys
import time
import datetime
import smtplib
import pkg_resources

# check that keyring is installed
try:
    pkg_resources.require('keyring')
except:
    sys.exit('dependency needed: $ pip3 install keyring')
import keyring


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from shutil import copyfile

def check_list(listFile):
    # check for the recipient list
    if os.path.isfile(listFile):
        pass
    else:
        print("No {} present.".format(listFile))
        sys.exit()                      # exit if no recipients

##################### RECIPIENTS ##########################
# Check if a specific email list is provided as an argument
# if none, then use email_recipients.txt
if len(sys.argv) == 2:
    listFile = sys.argv[1]
    check_list(listFile)
    print("Sending to {}".format(listFile))
else:
    listFile = "email_recipients.txt"
    check_list(listFile)
    print("Sending to {}".format(listFile))

# Check that the subject has been updated, exit if "n"
updated_subject = input("Did you update the subject line? (y/n) ")
if updated_subject.lower() != 'y':
    print("Please update the subject line.")
    exit()

##########################################################
#           edit these every time                        #
##########################################################

##################### DELAY UNTIL ########################
# send later by setting the time to delay until
#                               YYYY, MM, DD, HH, MM, SS
delay_until = datetime.datetime(2019, 8, 26, 13, 40, 0)

##################### SUBJECT ############################
# What is the subject of your email?
mail_subject = '[TESTING] Automated message status'

##################### SMTP SERVER##########################
# insert your smtp server here
mail_server = ''

##################### ATTACHMENT ##########################
# specify a file to attach in the same directory
filename = ''

##################### CREDENTIALS ########################
# store your username and password with the keyring modue
# keyring set system email_username
# keyring set system email_password
username = keyring.get_password('system', 'email_username')
password = keyring.get_password('system', 'email_password')    

##################### LOG ###############################
if os.path.isfile('send_log.txt'):
    logFile = open('send_log.txt', 'a+')
    logFile.write('\n')                 # start log entry on a new line
    logFile.close()
else:
    print("No log file present...")
    sys.exit()                      # exit if no log file

# timestamp the log entries
timestamp = datetime.datetime.now()
timestamp = timestamp.strftime('%Y-%m-%-d_%H:%M:%S')

# message of the email to send
message_file  = "message.txt"

if os.path.isfile(message_file):
    f = open(message_file, "r")
    body = ''.join(f.readlines())
    f.close()
else:
    print('no message file {}'.format(message_file))
    sys.exit()                      # exit if no message file

# pause everything until the delay_until time...
while datetime.datetime.now() < delay_until:
    time.sleep(1)

# opens the list file and send email to each recipient (one per line)
email_list = open(listFile)
for recipient in email_list.readlines():

    msg = MIMEMultipart()
    msg['Subject'] = mail_subject
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

##################### ARCHIVES ############################
filetimestamp = datetime.datetime.now()
filetimestamp = filetimestamp.strftime('%Y%m%d%H%M%S')

message_bkp = filetimestamp + '_' + message_file
copyfile(message_file, message_bkp)
print("Copied " + message_file+ " to " + message_bkp)

recipient_bkp = filetimestamp + '_' + listFile
copyfile(listFile, recipient_bkp)
print("Copied " + listFile + " to " + recipient_bkp)