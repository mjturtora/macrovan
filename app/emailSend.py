import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from secrets import *
import os
import fnmatch
from utils import *

path = "../macrovan/io/Output/"
emailBody = '''Your PDFs are attached'''
emailSubject = "Turf PDFs"
sender_address = email_address
sender_pass = email_password

# Set this to False to actually send the emails
testMode = True

# sendAllEmails will send emails to all the organizers in the secrets file
# def sendAllEmails():
#     sendEmails(emailsAndDirPaths.keys())

# # sendEmails to a list of organizers
# def sendEmails(organizers):
#     # Iterate through the organizer email address and email them their specific zip file
#     numFiles = 0
#     expectedFileCount = 0
#     if not testMode:
#         session = smtplib.SMTP('smtp.gmail.com', 587) 
#         session.starttls() 
#         session.login(sender_address, sender_pass) 
#         # Iterate through each organizer creating their emails and calling the attachPDFs function to attach their files
#         for organizer in organizers:
#             organizerTurfCount = len(turf_dict[organizer])
#             expectedFileCount += organizerTurfCount
#             #Create the email        
#             message = MIMEMultipart()
#             message['From'] = emailAddress
#             message['Subject'] = emailSubject
#             lastName = organizer[1]
#             fullName = organizer[0] + " " + organizer[1]
#             emailBody = "Hello " + organizer[0] + " " + lastName + ", \n \n Your PDFs are attached.  Click the download all attachments button to download them in one go." 
#             email = emailsAndDirPaths[organizer]
#             message['To'] = email
#             receiver_address = email
#             message.attach(MIMEText(emailBody, 'plain'))

#             # attachPDFs attaches the PDFs and returns the number of PDFs it attached
#             numAttachedFiles = attachPDFs(organizer, message) 
#             numFiles += numAttachedFiles

#             text = message.as_string()
            
#             # Check that the organizer had all of their files attached.  The email will not be sent if all the files were not attached
#             if(numAttachedFiles == organizerTurfCount and numAttachedFiles != 0):
#                 try:
#                     session.sendmail(sender_address, receiver_address, text)
#                 except smtplib.SMTPException:
#                     print("Email failed to send to: " + fullName)
#                 else:
#                     print("Email sent to: " + fullName + " : " + str(numAttachedFiles) + " files successfully attached")
#             else:
#                 print("Email failed to send to: " + fullName)
#             print()               
#         session.quit()
#         # Compare the total count of attached files to the amount of turfs
#         if numFiles == expectedFileCount:
#             print("All " + str(numFiles) + " files successfully attached!")
#         else:
#             difference = expectedFileCount - numFiles
#             print(expectedFileCount)
#             print("Failed to attach " + str(difference) + " files.....")

#     # In test mode the files will still be searched for and found filenames will be displayed
#     else:
#         print("Test Mode")
#         print("=========================================")
#         print("=====EXPECTED=================FOUND======")
#         print("=========================================")
#         for organizer in organizers:
#             print(organizer[0] + " " + organizer[1])
#             print(emailsAndDirPaths[organizer])
#             print("Files that will be sent: ")
#             numFiles += attachPDFs(organizer,0)
#             print("=========================================")

def initialize_session():
    if not testMode:
        session = smtplib.SMTP('smtp.gmail.com', 587) 
        session.starttls() 
        session.login(sender_address, sender_pass)
        return session
    else:
        print("Session not started.  Test mode is on.")

def create_email(receiver_address, filenames, first_name, last_name):
    message = MIMEMultipart()
    message['From'] = sender_address
    message['Subject'] = emailSubject
    emailBody = "Hello " + first_name + " " + last_name + ", \n \n Your PDF is attached." 
    email = receiver_address
    message['To'] = email
    message.attach(MIMEText(emailBody, 'plain'))
    numAttachedFiles = attachpdfs(filenames, message)
    if(numAttachedFiles == len(filenames)):
        return message
    else:
        print("Failed to create email for " + first_name + " " + last_name + "." + "  Email will not be sent.")
        return False

def add_cc(email, email_addresses):
    email['Cc'] = email_addresses

def send_email(receiver_address, email, session):
    if not testMode:
        text = email.as_string()
        try:
            session.sendmail(sender_address, receiver_address, text)
        except:
            return False
        else:
            return True
    else:
        print("Test mode is on.  Email not sent to " + receiver_address + ".")


def attachpdfs(file_names, email):
    numFiles = 0
    for file_to_attach in file_names:
        expectedFileName = file_to_attach + ".pdf"
        fileName = file_to_attach + "*" + ".pdf"
        fileName = fileName.replace(" ", "")
        outFileName = file_to_attach + ".pdf"
        if not testMode:  
            # Search the directory for a file that matches the fileName
            for file in os.listdir(path):
                foundFile = file.replace(" ", "")
                if fnmatch.fnmatch(foundFile, fileName):
                    pdf = MIMEApplication(open(path + file, 'rb').read())
                    pdf.add_header('Content-Disposition','attachment', filename=outFileName)
                    email.attach(pdf)
                    numFiles+=1
                    print("Attached " + file)
                    break
                    
        # Testing mode
        else:
            foundFile = "FILE NOT FOUND-------------------------------------F"
            for file in os.listdir(path):
                foundFile = file.replace(" ", "")
                foundFileName = "NOT FOUND"
                if fnmatch.fnmatch(foundFile, fileName):
                    foundFileName = file
                    test = open(path + file, 'rb')
                    test.close()
                    numFiles += 1
                    break
            # Expected on left, found on right
            print(expectedFileName + " : " + foundFileName)
    return numFiles


def input_choice():
    choice = input()
    if(choice == "Y" or choice == "y"):
        return True
    elif(choice == "N" or choice == "n"):
        return False
    else:
        print("Please enter (Y/N)")
        return input_choice()

def send_files():
    cc_list = ["gboicheff@gmail.com"]
    print("==================================================")
    turfs = get_entries()
    session = initialize_session()
    success = True
    for turf in turfs:
        print("-------------------------------------------")
        #need to be filled in once the sheet is made
        first_name = turf[0]
        last_name = turf[1]
        turf_name = turf[2]
        building_name = turf[3]
        receiver_address = turf[4]
        filename = turf_name + building_name      
        print("Send email to " + first_name + " " + last_name + " at " + receiver_address)
        print("With filename: " + filename)
        print("Enter (Y/N)")
        if input_choice():
            email = create_email(receiver_address, [filename], first_name, last_name)
            #add_cc(email, cc_list)
            if email != False:
                if send_email(receiver_address, email, session) != False:
                    print("Email to " + first_name + " " + last_name + " sent")
                else:
                    print("Email to " + first_name + " " + last_name + " not sent")
                    success = False
        else:
            print("Email to " + first_name + " " + last_name + " not sent")
            success = False
    session.quit()
    if success:
        print("All emails sent!")
    else:
        print("At least one email not sent!")
    print("==================================================")
    


    

if __name__ == '__main__':    
    send_files()