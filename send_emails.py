import random
import string
import smtplib
from email.mime.text import MIMEText

port = 2525 
smtp_server = "smtp.mailtrap.io"
login = "349e49f9ad2b10"
password = "45591dd18cef30"

sender = "from@smtp.mailtrap.io"
receiver = "to@smtp.mailtrap.io"

def randomString(stringLength=10):
	lettersDigits = string.ascii_lowercase + "0123456789"
	return ''.join(random.choice(lettersDigits) for i in range(stringLength))

def makeMessage(subject, content):
	message = MIMEText(content)
	message["Subject"] = subject
	message["From"] = sender
	message["To"] = receiver

	return message

def randomMessage():
	return makeMessage(randomString(), randomString())

def sendMessage(message):
	with smtplib.SMTP(smtp_server, port) as server:
		server.login(login, password)
		server.sendmail(sender, receiver, message.as_string())