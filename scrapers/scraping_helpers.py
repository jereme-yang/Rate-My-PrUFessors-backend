from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
import time

def scroll_through_names(driver, n = 28):
    time.sleep(0.5)
    for _ in range(n):
        ActionChains(driver)\
        .key_down(Keys.END)\
        .key_up(Keys.END)\
        .perform()
        time.sleep(0.5)

def get_tableau_url():
    ''' opens URL where the iframe for gatorevals
    data is available (https://gatorevals.aa.ufl.edu/public-results/)

    returns url for data src
    '''
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_experimental_option("detach", True) 
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless=new") # run without opening a browser - comment this to debug

    # initialize driver
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://gatorevals.aa.ufl.edu/public-results/")
    driver.implicitly_wait(5)
    time.sleep(5)

    tableau_url = driver.find_element(By.TAG_NAME, "iframe").get_attribute("src")
    time.sleep(5)
    driver.quit()
    return tableau_url

def initialize_webdriver(tableau_url):
    ''' Initialize driver based on tableau_url for scraping
    '''
    # initialize chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_experimental_option("detach", True) 
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless=new") # run without opening a browser - comment this to debug

    # initialize driver
    driver = webdriver.Chrome(options=chrome_options)

    # connect driver to website
    driver.get(tableau_url)
    driver.implicitly_wait(5)

    # wait for website to load before continuing
    time.sleep(5) 
    return driver

