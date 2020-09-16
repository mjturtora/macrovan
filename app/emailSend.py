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
emailSubject = "Turf PDF"
sender_address = email_address
sender_pass = email_password

# Set this to False to actually send the emails
testMode = False


def initialize_session():
    if not testMode:
        session = smtplib.SMTP('smtp.gmail.com', 587) 
        session.starttls() 
        session.login(sender_address, sender_pass)
        return session
    else:
        print("Session not started.  Test mode is on.")

def create_email(receiver_addresses, filenames, first_name, last_name, cc_list, list_number):
    message = MIMEMultipart()
    message['From'] = sender_address
    message['Subject'] = emailSubject
    emailBody = "Hello " + first_name + ", \n\nYour PDF is attached.\n\nYour list number is: "+ list_number + "\n\nYou may be able to copy/paste this directly from you phone's email app into MiniVan.\n\nAs a courtesy, please confirm that the file looks right to you with a reply-all to let us know that all is well.\n\nWarm Regards,\nYour GOTV-Pinellas Software Development Team!"
    message['To'] = ",".join(receiver_addresses)
    if(len(cc_list) > 0):
        message['Cc'] = ",".join(cc_list)
    message.attach(MIMEText(emailBody, 'plain'))
    numAttachedFiles = attachpdfs(filenames, message)
    if(numAttachedFiles == len(filenames)):
        return message
    else:
        print("Failed to create email for " + first_name + " " + last_name + "." + "  Email will not be sent.")
        return False

def send_email(receiver_addresses, email, session):
    if not testMode:
        text = email.as_string()
        try:
            session.sendmail(sender_address, receiver_addresses, text)
        except:
            return False
        else:
            return True
    else:
        print("Test mode is on.  Email not sent")


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
            print("Expected: " + expectedFileName + "    :    " + "Found: " + foundFileName)
    return numFiles


#Locate a file in the output folder.  Can toggle ignoring spaces
def find_file(filename, ignore_spaces):
    filename = filename + "*" + ".pdf"
    if ignore_spaces:
        filename = filename.replace(" ", "")
    for file in os.listdir(path):
        if ignore_spaces:
            foundFile = file.replace(" ", "")
        if fnmatch.fnmatch(foundFile, filename):
            return file
    return "NOT FOUND"            

def input_choice():
    print("Enter (Y/N):")
    choice = input()
    if(choice == "Y" or choice == "y"):
        return True
    elif(choice == "N" or choice == "n"):
        return False
    else:
        print("Please enter (Y/N):")
        return input_choice()


def send_files():
    #Add everybody to the CC list
    coordinator_emails = {
        "Carol Cason" : "cpcason23@gmail.com",
        "Denny Robertson" : "Denny88@aol.com",
        "Walt Gigli" : "zeekman320@gmail.com",
        "Tom Kimler" : "tkim55-8@hotmail.com"
    }

    cc_list = ["gboicheff@gmail.com", "janeathom@aol.com", "mjturtora@gmail.com"]
    print("==================================================")
    turfs = get_entries()
    session = initialize_session()
    success = True
    sent_count = 0
    sent_list = []
    for turf in turfs:
        print("-------------------------------------------")
        list_dict = extract_list_nums()
        first_name = turf[0]
        last_name = turf[1]
        turf_name = turf[2]
        building_name = turf[3]
        receiver_address = turf[4]
        coordinator_name = turf[5]
        coordinator_email = coordinator_emails[coordinator_name]
        final_cc_list = cc_list + [coordinator_email]
        #final_cc_list = cc_list
        filename = turf_name + building_name     
        print("Send email to " + first_name + " " + last_name + " at " + receiver_address)
        print("CCing: " + str(final_cc_list))
        print("Expected filename: " + filename)
        foundFile = find_file(filename, True)
        print("Found filename: " + find_file(filename, True))
        if input_choice():
            email = create_email([receiver_address], [filename], first_name, last_name, final_cc_list, list_dict[foundFile])
            if not testMode:
                if email != False:
                    all_to_addresses = [receiver_address] + final_cc_list
                    if send_email(all_to_addresses, email, session) != False:
                        print("Email to " + first_name + " " + last_name + " sent")
                        sent_list += [first_name + " " + last_name + " " + receiver_address + " EMAIL SENT" + "filename: " + foundFile]
                        sent_count+=1
                    else:
                        print("Email to " + first_name + " " + last_name + " not sent")
                        sent_list += [first_name + " " + last_name + " " +  receiver_address + " EMAIL NOT SENT"]
                        success = False
                else:
                    success = False
                    print("Email to " + first_name + " " + last_name + " not sent")
                    sent_list += [first_name + " " + last_name + " " + receiver_address + " EMAIL NOT SENT"]
            else:
                sent_count+=1
                sent_list += [first_name + " " + last_name +  "  " + receiver_address + " EMAIL NOT SENT"]
        else:
            print("Email to " + first_name + " " + last_name + " not sent")
            sent_list += [first_name + " " + last_name + " " + receiver_address + " EMAIL NOT SENT"]
            success = False
    if not testMode:
        session.quit()
    if success:
        print("All " + str(sent_count) + "emails sent!")
    else:
        print("At least one email not sent!")
    print("==================================================")
    for entry in sent_list:
        print(entry)
    

if __name__ == '__main__':
    print(extract_list_info())    
    #send_files()
