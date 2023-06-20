**send_email.py**

Send a plaintext email message with an optional attachment to a list of
email recipients.

* send_email.py			
	* edit this and run
* email_recipients.txt	
	* your list of recipients
* message.txt
	* write your message in here in plaintext
* send_log.txt
	* keep a log of each sent message

List your email addresses one per line on email_recipients.txt:

    email1@example.com
	email2@example.com
	email3@example.com

You will also need to install keyring using pip and put your credentials there.

    $ pip3 install keyring
	$ keyring set system email_username
	Password for 'email_username' in 'system': 
	$ keyring set system email_password
	Password for 'email_password' in 'system': 

These credentials will be called for the smtp authentication over tls.

**Delay Until**

You can delay the sending of your email by entering the date and time in
the code. Python will sleep until the time you specify.

	# send later by setting the time to delay until
	#                               YYYY, MM, DD, HH, MM, SS
	delay_until = datetime.datetime(2019, 8, 26, 13, 40, 0)

**Attaching a file**

Put your file in the same directory and specify the filename in the script.

	# specify a file to attach in the same directory
	filename = 'your_handout.pdf'

When you are all setup, run the script:

    $ python3 send_email.py

This is handy if you have regular template emails you send out to groups.

**Testing and Alternate Recipient Lists**

You can specify an email list as a command line argument:

    $ send_email.py test_list.txt

This will send to the test_list.txt instead of email_recipients.txt. This is useful to send yourself a test run to check the message prior to sending to the entire list.