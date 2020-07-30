import tkinter as tk
from utils import *
from printing_steps import *

def printNowButton():
    print('print button clicked')
    # Start from 'List' screen
    # Get list name and then clear the field
    list_name = list_name_entry.get()
    list_name_entry.delete(0, tk.END)
    print_list(driver, list_name)
    continue_instructions.pack()
    continue_button.pack()


def continueButton():
    print('continue button clicked')
    final_selections_submit(driver)
    continue_instructions.pack_forget()
    continue_button.pack_forget()

# def exitButton():
#     print('exit button clicked')

# Main function for testing
if __name__ == '__main__':
    window = tk.Tk()

    # Create driver and login
    teardown()
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
        text="Please make sure everything is correct. After reviewing press 'Continue'."
    )
    # exit_instructions = tk.Label(
    #     text="When you finish, click 'Exit'."
    # )

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
    # exit_button = tk.Button(
    #     text="Exit",
    #     width=15,
    #     height=5,
    #     fg="snow",
    #     bg="steel blue",
    #     command=exitButton
    # )

    # pack everything into GUI
    instructions1.pack()
    list_name_entry.pack()
    instructions2.pack()
    print_now_button.pack()
    # continue_instructions.pack()
    # continue_button.pack()
    # exit_instructions.pack()
    # exit_button.pack()

    window.mainloop()
