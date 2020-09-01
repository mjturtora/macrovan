from utils import *
from printing_steps import *

path = os.getcwd()
print(f"The current working directory is {path}")

if __name__ == '__main__':

    teardown()
    driver = start_driver()
    get_page(driver)
    driver.implicitly_wait(10)
    login_to_page(driver)  # todo: check if really need to or it might hang?
    list_folders(driver)
    select_folder(driver)

    turfs = get_turfs()

    for turf in turfs:
        turf_name = turf[0]
        print_list_name = turf[0] + " " + turf[1]
        select_turf(driver, turf_name)
        handle_alert(driver)
        print_controller(driver, print_list_name)
        driver.implicitly_wait(30)
        return_to_folder(driver)
        driver.implicitly_wait(30)