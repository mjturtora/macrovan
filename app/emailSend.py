import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from secrets import *
import os

#This file is setup to read data from turfData containing an organizers email address and the zipped directory
#that their PDFS are stored in and email that to them

path = "../macrovan/io/Output/"
emailBody = '''Your PDFs are attached'''
emailSubject = "Turf PDFs"


def sendEmails():
    sender_address = emailAddress
    sender_pass = emailPassword

    #Iterate through the organizer email address and email them their specific zip file
    for organizer in emailsAndDirPaths:
        message = MIMEMultipart()
        message['From'] = emailAddress
        message['Subject'] = emailSubject
        lastName = organizer[1]
        emailBody = "Hello " + organizer[0] + " " + lastName + ", \n \n Your PDFs are attached.  Click the download all attachments button to download them in one go." 
        email = emailsAndDirPaths[organizer]
        message['To'] = email
        receiver_address = email
        message.attach(MIMEText(emailBody, 'plain'))

        attachPDFs(lastName, message) 

        #Send the email
        session = smtplib.SMTP('smtp.gmail.com', 587) 
        session.starttls() 
        session.login(sender_address, sender_pass) 
        text = message.as_string()
        try:
            session.sendmail(sender_address, receiver_address, text)
        except smtplib.SMTPException:
            print("Email failed to send to: " + organizer[0] + " " + organizer[1])

    session.quit()

#Attaches a given organizers pdfs to an email
def attachPDFs(lastName, message):
    for filename in os.listdir(path + lastName):
     fileLocation = path + lastName + "/" + filename
     pdf = MIMEApplication(open(fileLocation, 'rb').read())
     pdf.add_header('Content-Disposition','attachment', filename=filename)
     message.attach(pdf)