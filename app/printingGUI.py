import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import ctypes  # for windows message pop-up
import tkinter as tk
from PrintingSteps import *
from secrets import *

def start_driver():
    """Initialize Chrome WebDriver with option to save user data to local
     folder to handle cookies"""
    # todo: check for valid (up-to-date) webdriver
    # driver.get('chrome://settings/')
    # driver.set_window_size(1210, 720)

    # https://stackoverflow.com/questions/15058462/how-to-save-and-load-cookies-using-python-selenium-webdriver

    chrome_options = Options()

    # todo: following lines added 7/8 trying to make repo pretty. Gave up. Maybe later.
    # Or maybe someone else can tell what I was trying to do and make it work. :)
    # chrome_options.add_argument(r"--user-data-dir='..\io\chrome-data'")
    # #chrome_options.add_argument("--enable-caret-browsing")
    # driver = webdriver.Chrome(r'..\io\drivers\chromedriver 83', options=chrome_options)
    # # adding argument opens with address bar highlighted and I can't figure out why!
    # #driver = webdriver.Chrome('./chromedriver 83')

    chrome_options.add_argument("--user-data-dir=chrome-data")
    driver = webdriver.Chrome('./chromedriver 83', options=chrome_options)

    return driver

def get_page(driver):
    # Get webpage
    driver.get('https://www.votebuilder.com/Default.aspx')
    # print_title(driver)
    return


def login_to_page(driver):
    # login and initialize:
    # Click ActionID Button to open login

    wait_no_longer_than = 30
    element = WebDriverWait(driver, wait_no_longer_than).until(
                EC.presence_of_element_located((By.XPATH, '//a[@href="/OpenIdConnectLoginInitiator.ashx?ProviderID=4"]')))
    #print(f'ELEMENT = {element}')

    driver.find_element_by_xpath("//a[@href='/OpenIdConnectLoginInitiator.ashx?ProviderID=4']").click()
    print('After ActionID Button')
    # print_title(driver)

    wait_no_longer_than = 30
    element = WebDriverWait(driver, wait_no_longer_than).until(
                EC.presence_of_element_located((By.ID, 'username')))
    #print(f'ELEMENT = {element}')

    username = driver.find_element_by_id("username")
    username.send_keys(user_name)
    password = driver.find_element_by_id("password")
    password.send_keys(pass_word)
    driver.find_element_by_class_name("btn-blue").click()
    return

def printNowButton():
    print('print button clicked')
    # Start from 'List' screen
    # Get list name and then clear the field
    list_name = list_name_entry.get()
    list_name_entry.delete(0, tk.END)
    print_list(driver, list_name)

def continueButton():
    print('continue button clicked')
    driver.implicitly_wait(30)
    return_to_folder(driver)

def exitButton():
    print('exit button clicked')

# Main function for testing
if __name__ == '__main__':
    window = tk.Tk()

    # Create driver and login
    driver = start_driver()
    get_page(driver)
    driver.implicitly_wait(10)
    login_to_page(driver)

    # Create GUI
    # Create Labels for instructions
    instructions1 = tk.Label(
        text="Please enter the name for your list below."
    )
    instructions2 = tk.Label(
        text="After you have opened your List click 'Print Now' to begin the printing process."
    )
    continue_instructions = tk.Label(
        text="If you need to print another list, click 'Continue'."
    )
    exit_instructions = tk.Label(
        text="When you finish, click 'Exit'."
    )

    # Create text Input
    list_name_entry = tk.Entry(
        width=25
    )

    # Create Buttons
    print_now_button = tk.Button(
        text="Print Now",
        width=15,
        height=5,
        fg="snow",
        bg="steel blue",
        command=printNowButton
    )
    continue_button = tk.Button(
        text="Continue",
        width=15,
        height=5,
        fg="snow",
        bg="steel blue",
        command=continueButton
    )
    exit_button = tk.Button(
        text="Exit",
        width=15,
        height=5,
        fg="snow",
        bg="steel blue",
        command=exitButton
    )

    # pack everything into GUI
    instructions1.pack()
    list_name_entry.pack()
    instructions2.pack()
    print_now_button.pack()
    continue_instructions.pack()
    continue_button.pack()
    exit_instructions.pack()
    exit_button.pack()

    window.mainloop()