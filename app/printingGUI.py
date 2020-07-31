import tkinter as tk
from utils import *
from printing_steps import *
import time

def printNowButton():
    print('print button clicked')
    # Start from 'List' screen
    # Get list name and then clear the field
    list_name = list_name_entry.get()
    if (list_name == ""):
        no_name_warning_text.pack()
    else:
        if (no_name_warning_text.winfo_ismapped()):
            no_name_warning_text.pack_forget()
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

    #Suppress all print statements
    disable_print()

    window = tk.Tk()
    window.title('GUIvan')


    # Create driver and login
    driver = start_driver()
    get_page(driver)
    driver.implicitly_wait(10)
    # take out login for release
    #login_to_page(driver)


    #Override the exit button of the tk window.
    window.wm_protocol("WM_DELETE_WINDOW", lambda: exit_program(window, driver))

    # Create GUI
    # Create Labels for instructions
    instructions1 = tk.Label(
        text="Please enter a name for this print file (pdf)."
    )
    instructions2 = tk.Label(
        text="When you are ready to print your list click 'Print Now'."
    )
    continue_instructions = tk.Label(
        text="Please make sure everything is correct. After reviewing press 'Continue'."
    )
    no_name_warning_text = tk.Label(
        text="Please enter a name for the print file.",
        fg = "red"
    )
    # exit_instructions = tk.Label(
    #     text="When you finish, click 'Exit'."
    # )

    # Create text Input
    list_name_entry = tk.Entry(
        width=35
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
    no_name_warning_text.pack()
    no_name_warning_text.pack_forget()
    list_name_entry.pack()
    instructions2.pack()
    print_now_button.pack()
    # continue_instructions.pack()
    # continue_button.pack()
    # exit_instructions.pack()
    # exit_button.pack()
    window.after(1500,lambda: check_browser(window, driver))
    window.mainloop()
