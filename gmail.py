import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
from sql import select

def send_gmail(judul,description,credentials,db):
	users = select(q=f"select name,email from {db}")

	gmail_user = credentials[0]
	gmail_password = credentials[1]

	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.ehlo()
	server.login(gmail_user, gmail_password)

	subject = f'Event DOSCOM - {judul.title()}'

	for x in users:
		msg = MIMEMultipart()
		msg['From'] = gmail_user
		msg['Subject'] = subject
		names = x[0]
		body = f'''Hai {names},

{description}

@Doscom_bot
'''
		msg.attach(MIMEText(body, 'plain'))
		msg['To'] = x[1]

		# binary_pdf = open(f"pdf/{names}.pdf", 'rb')
		# payload = MIMEBase('application', 'octate-stream', Name=f"{names}.pdf")
		# payload.set_payload((binary_pdf).read())
		# encoders.encode_base64(payload)
		# payload.add_header('Content-Decomposition', 'attachment', filename=f"{names}.pdf")
		# msg.attach(payload)

		server.sendmail(gmail_user, x[1], msg.as_string())

	server.close()

if __name__ == '__main__':
	send_gmail()