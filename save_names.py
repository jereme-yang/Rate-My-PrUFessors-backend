import pickle
import time
from typing import List
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from utils.scraping_helpers import get_tableau_url, initialize_webdriver, scroll_through_names

def save_names(names: List[str], filename: str) -> None:
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(names, outp, pickle.HIGHEST_PROTOCOL)

# get the URL to the tableau page from the iframe found on https://gatorevals.aa.ufl.edu/public-results/
tableau_url = get_tableau_url()
driver = initialize_webdriver(tableau_url)

# open dropdown for instructor name
names_dropdown = driver.find_element(By.ID, "tabZoneId12")
names_dropdown.click()

# uncheck the all button
time.sleep(1)
all_checkbox = driver.find_element(By.NAME, "FI_sqlproxy.1j0k1xa05f9b0k18gqber1rlouv3,none:INSTRUCTOR_NAME:nk7413426041701531777_11695660129199681370_(All)")
all_checkbox.click()

# scroll through entire list
scroll_through_names(driver)

# grab all names (str) for finding the tags (title="name")
all_name_elements = driver.find_elements(By.CLASS_NAME, "FIText")
all_names = [element.text for element in all_name_elements][2:]
del all_name_elements

# save the list of names
save_object(all_names, 'all_names.pkl')
print("all names saved")