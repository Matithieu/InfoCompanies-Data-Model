import csv
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import random

# Helper functions for browser setup and random sleep times
def sleep_time():
    time.sleep(random.randint(2, 2))

def configure_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--window-size=1600, 1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_company_info(driver, company_name, adresse):
    driver.get(f"https://www.google.com/search?q={company_name} {adresse}")
    time.sleep(1)

    try:
        # Accept the cookies if the button is present
        cookie_button = driver.find_elements(By.XPATH, '//*[@id="L2AGLb"]')
        if cookie_button:
            cookie_button[0].click()
    except NoSuchElementException:
        pass

    sleep_time()

    company_info = {
        "company_name": company_name,
        "phone": extract_phone_number(driver),
        "address": extract_address(driver),
        "website": extract_website(driver),
        "schedule": extract_schedule(driver),
        "instagram": extract_instagram(driver),
        "facebook": extract_facebook(driver),
        "twitter": extract_twitter(driver),
        "linkedin": extract_linkedin(driver),
        "youtube": extract_youtube(driver),
        "email": extract_email(driver),
        "reviews": extract_reviews(driver),
    }

    driver.quit()

    print(company_info)

    return company_info

def extract_phone_number(driver):
    # Extract the phone number
    phone = ""
    try:
        phone_element = driver.find_element(By.XPATH, "//span[contains(@aria-label, 'Appeler le')]")
        phone = phone_element.text
    except NoSuchElementException:
        phone = "No phone number found"

    return phone

def extract_address(driver):
    # Extract the address without relying on class names
    address = ""
    try:
        # This XPATH finds the anchor element containing the text 'Adresse'
        # Then gets the following sibling that contains the address text
        address_element = driver.find_element(By.XPATH, "//a[contains(text(), 'Adresse')]/following::span[2]")
        address = address_element.text
    except NoSuchElementException:
        address = "No address found"

    return address

def extract_website(driver):
    # Extract the website URL
    website = ""
    try:
        # This XPath looks for an 'a' element with a 'div' child that contains the text 'Site Web'
        website_element = driver.find_element(By.XPATH, "//a[./div[text()='Site Web']]")
        website = website_element.get_attribute('href')
    except NoSuchElementException:
        website = "No website URL found"

    return website

def extract_schedule(driver):
    # Extract the schedule from the table
    time.sleep(3)
    schedule = {}
    try:
        extend_schedule_list = driver.find_element(By.XPATH, "//a[contains(text(), 'Horaires')]/following::div/div")
        extend_schedule_list.click()
        
        rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
        
        for row in rows:
            # The first <td> contains the day of the week
            day_td = row.find_element(By.XPATH, "./td[1]")
            day = day_td.text.strip()

            # The second <td> contains the hours and any additional information
            hours_td = row.find_element(By.XPATH, "./td[2]")
            hours_text = hours_td.text.strip()

            schedule[day] = hours_text
    except NoSuchElementException:
        schedule = "No schedule found"

    return schedule

def extract_instagram(driver):
    # Extract the Instagram URL
    instagram = ""
    try:
        instagram_element = driver.find_element(By.XPATH, "//a[contains(@href, 'https://www.instagram.com/')]")
        instagram = instagram_element.get_attribute('href')
    except NoSuchElementException:
        instagram = "No Instagram URL found"
    return instagram

def extract_facebook(driver):
    # Extract the Facebook URL
    facebook = ""
    try:
        # Since the href attribute contains the full Facebook URL, we can directly get it
        facebook_element = driver.find_element(By.XPATH, "//a[contains(@href, 'https://www.facebook.com/')]")
        facebook = facebook_element.get_attribute('href')
    except NoSuchElementException:
        facebook = "No Facebook URL found"
    return facebook

def extract_twitter(driver):
    # Extract the Twitter URL
    twitter = ""
    try:
        twitter_element = driver.find_element(By.XPATH, "//a[contains(@href, 'https://twitter.com/')]")
        twitter = twitter_element.get_attribute('href')
    except NoSuchElementException:
        twitter = "No Twitter URL found"
    return twitter

def extract_linkedin(driver):
    # Extract the LinkedIn URL
    linkedin = ""
    try:
        linkedin_element = driver.find_element(By.XPATH, "//a[contains(@href, 'https://www.linkedin.com/')]")
        linkedin = linkedin_element.get_attribute('href')
    except NoSuchElementException:
        linkedin = "No LinkedIn URL found"
    return linkedin

def extract_youtube(driver):
    # Extract the YouTube URL
    youtube = ""
    try:
        youtube_element = driver.find_element(By.XPATH, "//a[contains(@href, 'https://www.youtube.com/')]")
        youtube = youtube_element.get_attribute('href')
    except NoSuchElementException:
        youtube = "No YouTube URL found"
    return youtube

def extract_email(driver):
    # Extract the email through the url starting by mailto:
    email = ""
    try:
        email = driver.find_element(By.LINK_TEXT, "Email")
    except NoSuchElementException:
        email = "No email found"

    return email


def extract_reviews(driver):
    try:
        reviews = []
        list_review_button = driver.find_element(By.XPATH, "//span[contains(text(), 'avis Google')]")
        list_review_button.click()
        
        time.sleep(3)
        
        rows = driver.find_elements(By.CLASS_NAME, "gws-localreviews__google-review")
        
        for row in rows:            
            author = row.find_element(By.XPATH, ".//img[contains(@src, 'https://lh3.googleusercontent.com/')]")
            author = author.get_attribute('alt')
            stars = row.find_element(By.XPATH, ".//*[contains(@aria-label, 'Note')]")
            # Extract the rating from the aria-label attribute
            stars = stars.get_attribute('aria-label')
            note = stars.split()[2]  # Cela suppose que la chaîne est de la forme "Note : 4,5 sur 5"
            
            try:
                extend_review_button = row.find_element(By.XPATH, ".//a[contains(text(), 'Plus')]")
                extend_review_button.click()
            except:
                pass

            review_text = row.find_element(By.XPATH, ".//span[@class='review-snippet']").text
            
            reviews.append({"author": author, "text": review_text, "stars": note})
    except NoSuchElementException:
        reviews = "No reviews found"
        
    return reviews
        
scrape_company_info(configure_selenium(), "Mistral boite de nuit", "aix")