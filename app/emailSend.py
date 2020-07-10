import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from secrets import *
import os
import fnmatch
from utils import getAllTurfs

path = "../macrovan/io/Output/"
emailBody = '''Your PDFs are attached'''
emailSubject = "Turf PDFs"
sender_address = emailAddress
sender_pass = emailPassword

#Set this to False to actually send the emails
testMode = False

def sendAllEmails():
    #Iterate through the organizer email address and email them their specific zip file
    numFiles = 0
    if not testMode:
        session = smtplib.SMTP('smtp.gmail.com', 587) 
        session.starttls() 
        session.login(sender_address, sender_pass) 
        #Iterate through each organizer creating their emails and calling the attachPDFs function to attach their files
        for organizer in emailsAndDirPaths:
            organizerTurfCount = len(turf_dict[organizer])        
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

            numAttachedFiles = attachPDFs(organizer, message) 
            numFiles += numAttachedFiles
            
            text = message.as_string()
            if(numAttachedFiles == organizerTurfCount and numAttachedFiles != 0):
                try:
                    session.sendmail(sender_address, receiver_address, text)
                except smtplib.SMTPException:
                    print("Email failed to send to: " + fullName)
                else:
                    print("Email sent to: " + fullName + " : " + str(numAttachedFiles) + " files successfully attached")
            else:
                print("Email failed to send to: " + fullName)               
        session.quit()
    else:
        print("Test Mode")
        print("=========================================")
        print("=====EXPECTED=================FOUND======")
        print("=========================================")
        for organizer in emailsAndDirPaths:
            print(organizer[0] + " " + organizer[1])
            print(emailsAndDirPaths[organizer])
            print("Files that will be sent: ")
            numFiles += attachPDFs(organizer,0)
            print("=========================================")

    #Compare the total count of attached files to the amount of turfs
    expectedFileCount = len(getAllTurfs(turf_dict))
    if numFiles == expectedFileCount:
        print("All " + str(numFiles) + " files successfully attached!")
    else:
        difference = expectedFileCount - numFiles
        print(expectedFileCount)
        print("Failed to attach " + str(difference) + " files.....")


def attachPDFs(organizer, message):
    numFiles = 0
    for file in turf_dict[organizer]:
        fileName = file[0] + " " + file[1] + "*" + ".pdf"
        outFileName= file[0] + " " + file[1] + ".pdf"
        if not testMode:  
            #Search the directory for a file that matches the fileName
            for file in os.listdir(path):
                if fnmatch.fnmatch(file, fileName):
                    pdf = MIMEApplication(open(path + file, 'rb').read())
                    pdf.add_header('Content-Disposition','attachment', filename=outFileName)
                    message.attach(pdf)
                    numFiles+=1
                    break
                    
        #Testing mode
        else:
            foundFile = "FILE NOT FOUND-------------------------------------F"
            for file in os.listdir(path):
                if fnmatch.fnmatch(file, fileName):
                    foundFile = file
                    test = open(path + file, 'rb')
                    test.close()
                    numFiles+=1
                    break
            #Expected on left, found on right            
            print(fileName + " : " + foundFile)
    return numFiles

if __name__ == '__main__':
    sendAllEmails()