import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from secrets import *
import os


path = "../macrovan/io/Output/"
emailBody = '''Your PDFs are attached'''
emailSubject = "Turf PDFs"
sender_address = emailAddress
sender_pass = emailPassword

#Set this to False to actually send the emails
testMode = False

def sendAllEmails():
    #Iterate through the organizer email address and email them their specific zip file
    if not testMode:
        session = smtplib.SMTP('smtp.gmail.com', 587) 
        session.starttls() 
        session.login(sender_address, sender_pass) 
        
        #Iterate through each organizer creating their emails and calling the attachPDFs function to attach their files
        for organizer in emailsAndDirPaths:        
            message = MIMEMultipart()
            message['From'] = emailAddress
            message['Subject'] = emailSubject
            lastName = organizer[1]
            fullName = organizer[0] + " " + organizer[1]
            emailBody = "Hello " + organizer[0] + " " + lastName + ", \n \n Your PDFs are attached.  Click the download all attachments button to download them in one go." 
            email = emailsAndDirPaths[organizer]
            message['To'] = email
            receiver_address = email
            message.attach(MIMEText(emailBody, 'plain'))

            attachPDFs(organizer, message) 
            
            text = message.as_string()
            try:
                session.sendmail(sender_address, receiver_address, text)
            except smtplib.SMTPException:
                print("Email failed to send to: " + fullName)
            else:
                print("Email sent to: " + fullName)               
        session.quit()
    else:
        print("Test Mode")
        print("=========================================")
        for organizer in emailsAndDirPaths:
            print(organizer[0] + " " + organizer[1])
            print(emailsAndDirPaths[organizer])
            print("Files that will be sent: ")
            attachPDFs(organizer,0)
            print("=========================================")

#Cycles through the PDFs in output and attaches each organizers files to their email
def attachPDFs(organizer, message):
    for file in turf_dict[organizer]:
        fileName = file[0] + ".pdf"
        filePath = path + fileName
        if not testMode:  
            pdf = MIMEApplication(open(filePath, 'rb').read())
            pdf.add_header('Content-Disposition','attachment', filename=fileName)
            message.attach(pdf) 
        else:
            try:
                test = open(filePath, 'rb')
                test.close()
            except FileNotFoundError:
                print(filePath + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FILE NOT FOUND")
            else:
                print(filePath)

if __name__ == '__main__':
    sendAllEmails()