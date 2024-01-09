from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re
import pandas as pd

def WebScrape(restaurant_name, comments_num, progress_bar):
    chrome_options = Options()
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_argument('--headless') # Run in the background without displaying a visible browser window

    driver = webdriver.Chrome("桌面\chromedriver.exe", options=chrome_options)

    search_url = "https://www.google.com/maps/@39.1111036,-105.0715591,5.37z?hl=en"
    driver.get(search_url)
    time.sleep(2)

    # Search by restaurant name
    Search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchboxinput")))
    Search_box.clear()
    Search_box.send_keys(restaurant_name)
    Search_box.send_keys(Keys.ENTER)
    time.sleep(2)

    # Get restaurant's location (Latitude, longtitude)
    url = driver.current_url
    pattern = r"@([-+]?\d+\.?\d*),([-+]?\d+\.?\d*)"
    match = re.search(pattern, url)
    lat = float(match.group(1)) 
    lon = float(match.group(2))
    df = pd.DataFrame({
        'lat': [lat],
        'lon': [lon],
        'color': '#ED2B2A',
        'size': 7
    })

    # Get restaurant address and phone number
    address_and_phone_number = []
    address = ''
    phone = ''

    address_and_phone = driver.find_elements(By.CSS_SELECTOR, ".Io6YTe.fontBodyMedium")
    for i in address_and_phone:
        address_and_phone_number.append(i.text)
    
    print(address_and_phone_number)

    address_regex = r'\d+\s+[\w\s]+,\s+\w+,\s+\w+\s+\d+,\s+\w+'
    phone_regex = r'\+\d+\s+\d+-\d+-\d+'
    
    for item in address_and_phone_number:
        if re.match(address_regex, item):
            address = item
        elif re.match(phone_regex, item):
            phone = item

    address = address_and_phone_number[0]
    print(address)
    print(phone)

    # Click more reviews section
    More_reviews= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@jsaction ='pane.reviewChart.moreReviews']")))
    More_reviews.click()
    time.sleep(1.5)

    text = []
    new_text =[]

    if (int(comments_num/10)) < 50:    
        for i in range(int(comments_num/10)): 
            scroll_body= WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]')))
            
            driver.execute_script('arguments[0].scrollBy(0,7100);', scroll_body)
            time.sleep(0.5)
            progress = int(((i + 1) / (comments_num / 10)) * 100)  
            progress_bar.progress(progress)  
    else:
        for i in range(50):
            scroll_body= WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]')))
            
            driver.execute_script('arguments[0].scrollBy(0,7100);', scroll_body)
            time.sleep(0.5)
            progress = int(((i + 1) / 50) * 100) 
            progress_bar.progress(progress)


    text = driver.find_elements(By.CLASS_NAME, "wiI7pd")

    # Remove duplicate reviews from the text list and store the unique reviews in the new_text list.
    for t in text:
        if t.text not in new_text:
            new_text.append(t.text)

    new_text_df = pd.DataFrame(new_text, columns=['comment'])

    driver.close()
    
    return new_text_df, df, address, phone