# imports
from selenium import webdriver
import csv
import parameters
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
# defining new variable passing two parameters
writer = csv.writer(open(parameters.file_name, 'w'))

# writerow() method to the write to the file object
header = ['Name', 'Job Title', 'Company / College', 'Location', 'URL']
writer.writerow(header)

# specifies the path to the chromedriver.exe
# Define Chrome service with custom executable path
cService = webdriver.ChromeService(executable_path='C:/Driver/chromedriver.exe')

# Define Chrome options
chrome_options = webdriver.ChromeOptions()

# Add the --disable-infobars argument
chrome_options.add_argument("--disable-infobars")
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--use-subprocess")
# Initialize the Chrome WebDriver with the service and options
driver = webdriver.Chrome(service=cService, options=chrome_options)

#driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com')

# locate email form by_class_name
username = driver.find_element("id","session_key")

# send_keys() to simulate key strokes
username.send_keys(parameters.linkedin_username)

# sleep for 0.5 seconds

# locate password form by_class_name
password = driver.find_element("name","session_password")

# send_keys() to simulate key strokes
password.send_keys(parameters.linkedin_password)
# locate submit button by_xpath
sign_in_button = driver.find_element(By.XPATH,'//*[@type="submit"]')

# .click() to mimic button click
sign_in_button.click()


# Replace 'your_excel_file.xlsx' with the path to your Excel file.
file_path = 'uploads\data.csv'

# Load the Excel file into a DataFrame.
df = pd.read_csv(file_path)
wait = WebDriverWait(driver, 1)
def is_captcha_present():
    try:
        captcha_element = wait.until(EC.presence_of_element_located((By.ID, 'recaptcha')))
        return True
    except Exception:
        return False

# Assuming the first column in the Excel file is labeled 'Name'.
for name in df['Name']:
    print(name)
    driver.get('https:www.google.com')
    search_query = driver.find_element("id","APjFqb") 
    search_query.send_keys(parameters.search_query+name)

    search_query.send_keys(Keys.RETURN)
    while is_captcha_present():
        time.sleep(2)
    time.sleep(2)
    link_elements = driver.find_elements(By.XPATH,'//a[@jsname="UWckNb"]')

    linkedin_urls = []

    for link in link_elements:
        href = link.get_attribute("href")
        first_name, last_name = name.split()
        if first_name.lower() in href and last_name.lower() in href:
            if 'post' in href:
                continue
            else:
                linkedin_urls.append(href)
    time.sleep(0.5)
   
    # For loop to iterate over each URL in the list
    for linkedin_url in linkedin_urls:

        # get the profile URL 
        driver.get(linkedin_url)

        # add a 5 second pause loading each URL
        time.sleep(2)

        # assigning the source code for the webpage to variable sel
        sel = Selector(text=driver.page_source) 
        
        # xpath to extract the text from the class containing the name
        name = sel.xpath('//*[starts-with(@class,"text-heading-xlarge inline t-24 v-align-middle break-words")]/text()').extract_first()
        if name:
            name = name.strip()

        linkedin_url = driver.current_url
        # Assuming `sel` contains the Selector object for the HTML

        company = sel.xpath('//div[contains(@style, "-webkit-line-clamp:2;")]/text()').get()
        if company:
            company = company.strip()

        job_title = sel.xpath('//div[@class="text-body-medium break-words"]/text()').get()
        if job_title:
            job_title = job_title.strip()

        location = sel.xpath('//span[@class="text-body-small inline t-black--light break-words"]/text()').get()
        if location:
            location = location.strip()


        # printing the output to the terminal
        print('\n')
        print(name)
        print(company)
        print(job_title)
        print(location)
        print(linkedin_url)
        print('\n')
        
        # writing the corresponding values to the header
        writer.writerow([name,job_title,company,location,linkedin_url])
driver.quit()
