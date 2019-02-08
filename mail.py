import smtplib
import getpass
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText
 
fromaddr = input("enter your email address : ") 
password = getpass.getpass("enter your password : ")
toaddr = input("enter recievers email address : ")
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr

sub = input("enter message subject : ")

msg['Subject'] = sub
 
body = input("enter the message body : ")
msg.attach(MIMEText(body, 'plain'))
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr,password)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
print("email sent succesfully!") 
