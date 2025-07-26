import json
import pickle
import time
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from utils.scraping_helpers import get_tableau_url, initialize_webdriver, scroll_through_names

def convert_name(name):
    '''convert name from "last_name, first_name" to 
    "first_name last_name"
    '''
    # Split the name at the comma
    parts = name.split(', ')
    # Rearrange the parts and join them with a space
    converted_name = f"{parts[1]} {parts[0]}"
    return converted_name

def main():
    data = defaultdict(list)
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

    scroll_through_names(driver)

    # grab all names (str) for finding the tags (title="name")
    for element in driver.find_elements(By.CLASS_NAME, "FIText"):
        data[element.text]

    broke_counter, start_index = 0, 0
    # go through all profs, query the data
    for i in range(start_index, data.keys()):
        # while Loop to try fetching data for the same prof 
        # 3 times because selenium/overlapping HTMLObject issues can occur
        while True:
            try:            
                # focus table by pressing all tab
                time.sleep(3)
                table = driver.find_element(By.XPATH, '//a[@title="(All)"]')
                time.sleep(3)
                table.click()
                time.sleep(0.5)

                # get the checkbox for the associated name
                time.sleep(5)
                checkbox = driver.find_element(By.XPATH, f'//a[contains(text(), "{all_names[i]}")]/preceding-sibling::input')
                time.sleep(5)

                # click the checkbox (enable)
                checkbox.click()
                time.sleep(0.5)

                # close dropdown for instructor names
                body = driver.find_element(By.XPATH, '//div[@class="tab-glass clear-glass tab-widget"]')
                time.sleep(3)
                body.click()
                time.sleep(0.5)

                # find the canvas
                canvas = driver.find_element(By.ID, "view7413426041701531777_11695660129199681370")
                time.sleep(5)

                # click on the canvas
                canvas.click()
                time.sleep(0.5)

                # perform keypresses to display the first data point
                ActionChains(driver)\
                        .key_down(Keys.RETURN)\
                        .key_up(Keys.RETURN)\
                        .perform()
                
                # keypresses until displaying the correct data
                incorrect_element = driver.find_element(By.XPATH, '//span[contains(text(), "'+"%"+' of Total Count of RESPONSE_VALUE along RESPONSE_CATEGORY:") and @style="font-family:\'Tableau Book\';font-size:13px;color:#787878;font-weight:normal;font-style:normal;text-decoration:none;"]')
                while incorrect_element:
                    ActionChains(driver)\
                        .key_down(Keys.ARROW_RIGHT)\
                        .key_up(Keys.ARROW_RIGHT)\
                        .perform()
                    try:
                        incorrect_element = driver.find_element(By.XPATH, '//span[contains(text(), "'+"%"+' of Total Count of RESPONSE_VALUE along RESPONSE_CATEGORY:") and @style="font-family:\'Tableau Book\';font-size:13px;color:#787878;font-weight:normal;font-style:normal;text-decoration:none;"]')
                    except:
                        break
                time.sleep(0.5)

                # parse prof data
                num_data_points = 6
                for j in range(num_data_points):
                    datapoint = driver.find_element(By.XPATH, '//span[@style="font-family:\'Tableau Book\';font-size:13px;color:#333333;font-weight:bold;font-style:normal;text-decoration:none;"]').text
                    time.sleep(0.5)
                    data.append(datapoint)
                    if j == num_data_points:
                        break
                
                    # move to next one
                    ActionChains(driver)\
                            .key_down(Keys.ARROW_DOWN)\
                            .key_up(Keys.ARROW_DOWN)\
                            .perform()

                # append the average for this version
                data[all_names[i]].append(str(round(sum([float(e) for e in data[1:]])/num_data_points, 2)))
                
                time.sleep(0.5)
                print(f"{data[all_names[i]]}")

                # re open dropdown for instructor names
                names_dropdown = driver.find_element(By.ID, "tabZoneId12")
                time.sleep(3)

                names_dropdown.click()
                time.sleep(1)

                # click "All" to focus the scrollable section
                table = driver.find_element(By.XPATH, '//a[@title="(All)"]')
                time.sleep(5)
                table.click()
                time.sleep(1)

                # scroll through the names dropdown
                scroll_through_names(driver)

                # uncheck the professor that just got queried
                clicked_checkbox = driver.find_element(By.XPATH, '//input[@checked="checked"]')
                time.sleep(5)
                clicked_checkbox.click()
                break
            except:
                # run broke. known reasons: browser times out / broken index on tableau -> restart selenium
                time.sleep(5)
                print(f"broken at index {i}. Retrying {3-broke_counter} more times...")
                driver.quit()
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

                time.sleep(30) # this could probably be changed to 5-10 seconds
                
                # if the run breaks 3 times in a row then it's likely because of
                # overlapping elements -> skip this one
                broke_counter += 1
                if broke_counter == 3:
                    print("writing to broke.txt ...")
                    with open("broke.txt", 'a') as f_object:
                        f_object.write(f"{i}, {all_names[i]}\n")
                        f_object.close()
                    break

        # skip if the current element cannot be parsed after 3 tries
        if broke_counter == 3:
            broke_counter = 0
            continue
    
    # save the data to json file
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    main()

