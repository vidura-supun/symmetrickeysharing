import smtplib
import getpass
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
fromaddr = raw_input("enter your email address : ") 
password = getpass.getpass("enter your password : ")
toaddr = raw_input("enter recievers email address : ")
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr

sub = raw_input("enter message subject : ")

msg['Subject'] = sub
 
body = raw_input("enter the message body : ")
#body = "hi from the cli"
msg.attach(MIMEText(body, 'plain'))
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr,password)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
print("email sent succesfully!") 
