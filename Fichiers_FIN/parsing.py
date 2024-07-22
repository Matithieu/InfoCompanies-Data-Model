import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time
import random
import multiprocessing
from multiprocessing import Manager
import pandas as pd
import numpy as np


def sleep_time():
    time.sleep(random.randint(1, 1))


def configure_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_experimental_option(
        "excludeSwitches", ["enable-logging", "enable-automation"]
    )
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--window-size=1600, 1080")
    options.add_argument("--headless")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def scrape_company_info(driver, company_name, adresse):
    driver.get(f"https://www.google.com/search?q={company_name} {adresse}")
    # Increase or get blocked after 1-2 min
    # Try to see without the headless mode to see what's happening
    # Maybe a captcha
    time.sleep(2)

    try:
        cookie_button = driver.find_elements(By.XPATH, '//*[@id="L2AGLb"]')
        if cookie_button:
            cookie_button[0].click()
    except NoSuchElementException:
        pass

    company_info = {
        "phone_number": extract_phone_number(driver),
        "website": extract_website(driver),
        "instagram": extract_instagram(driver),
        "facebook": extract_facebook(driver),
        "twitter": extract_twitter(driver),
        "linkedin": extract_linkedin(driver),
        "youtube": extract_youtube(driver),
        "email": extract_email(driver),
        "scraping_date": time.strftime("%Y-%m-%d"),
        "reviews": extract_reviews(driver),
        "schedule": extract_schedule(driver, company_name),
    }

    # Replace 'nan' with empty string
    for key, value in company_info.items():
        if pd.isna(value) or value == "nan":
            company_info[key] = ""

    return company_info


def extract_phone_number(driver):
    phone = ""
    try:
        phone_element = driver.find_element(
            By.XPATH, "//span[contains(@aria-label, 'Appeler le')]"
        )
        phone = phone_element.text
    except NoSuchElementException:
        phone = ""
    return phone


def extract_website(driver):
    website = ""
    try:
        website_element = driver.find_element(By.XPATH, '//a[contains(.,"Site Web")]')
        website = website_element.get_attribute("href")
    except NoSuchElementException:
        website = ""
    return website


def extract_schedule(driver, company_name):
    dayOfTheWeek = [
        "lundi",
        "mardi",
        "mercredi",
        "jeudi",
        "vendredi",
        "samedi",
        "dimanche",
    ]
    schedule = {}

    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        for table in tables:
            day_column = table.find_elements(By.XPATH, ".//tbody/tr/td[1]")
            if day_column:
                for day_elem in day_column:
                    day = day_elem.get_attribute("textContent").strip().lower()
                    if day in dayOfTheWeek:
                        hours_td_list = table.find_elements(
                            By.XPATH,
                            ".//tbody/tr[td[1][text()='{}']]/td[2]".format(day),
                        )
                        if hours_td_list:
                            for hours_td in hours_td_list:
                                hours_text = hours_td.get_attribute(
                                    "textContent"
                                ).strip()
                            schedule[day] = hours_text
                        else:
                            schedule[day] = ""
    except NoSuchElementException as e:
        print(f"Could not extract schedule for {company_name}: {e}")
        schedule = {}

    return schedule


def extract_instagram(driver):
    instagram = ""
    try:
        instagram_element = driver.find_element(
            By.XPATH, "//a[contains(@href, 'https://www.instagram.com/')]"
        )
        instagram = instagram_element.get_attribute("href")
    except NoSuchElementException:
        instagram = ""
    return instagram


def extract_facebook(driver):
    facebook = ""
    try:
        facebook_element = driver.find_element(
            By.XPATH, "//a[contains(@href, 'https://www.facebook.com/')]"
        )
        facebook = facebook_element.get_attribute("href")
    except NoSuchElementException:
        facebook = ""
    return facebook


def extract_twitter(driver):
    twitter = ""
    try:
        twitter_element = driver.find_element(
            By.XPATH, "//a[contains(@href, 'https://twitter.com/')]"
        )
        twitter = twitter_element.get_attribute("href")
    except NoSuchElementException:
        twitter = ""
    return twitter


def extract_linkedin(driver):
    linkedin = ""
    try:
        linkedin_element = driver.find_element(
            By.XPATH, "//a[contains(@href, 'https://www.linkedin.com/')]"
        )
        linkedin = linkedin_element.get_attribute("href")
    except NoSuchElementException:
        linkedin = ""
    return linkedin


def extract_youtube(driver):
    youtube = ""
    try:
        youtube_element = driver.find_element(
            By.XPATH, "//a[contains(@href, 'https://www.youtube.com/')]"
        )
        youtube = youtube_element.get_attribute("href")
    except NoSuchElementException:
        youtube = ""
    return youtube


def extract_email(driver):
    email = ""
    try:
        email = driver.find_element(By.LINK_TEXT, "Email")
    except NoSuchElementException:
        email = ""
    return email


def extract_reviews(driver):
    reviews = {}
    try:
        stars_elements = driver.find_elements(
            By.XPATH, "//span[contains(@aria-label, 'Note')]"
        )
        number_of_reviews_elements = driver.find_elements(
            By.XPATH, "//a[contains(text(), 'avis')]"
        )

        if stars_elements:
            reviews["stars"] = stars_elements[0].get_attribute("aria-label").split()[2]
        else:
            reviews["stars"] = ""

        if number_of_reviews_elements:
            reviews["number_of_reviews"] = number_of_reviews_elements[0].text.split()[0]
        else:
            reviews["number_of_reviews"] = ""

    except NoSuchElementException:
        reviews = {"stars": "", "number_of_reviews": ""}

    return reviews


def process_chunk(chunk, output_file, lock):
    driver = configure_selenium()
    try:
        for _, row in chunk.iterrows():
            search_name = row["company_name"]
            adresse = row["city"]

            try:
                company_info = scrape_company_info(driver, search_name, adresse)
                row.update(company_info)

                # Replace 'nan' with empty string in the row
                row = row.replace("nan", "", regex=True)
                row = row.fillna("")

                with lock:
                    with open(output_file, mode="a", encoding="utf-8", newline="") as f:
                        writer = csv.DictWriter(f, fieldnames=row.index, delimiter=";")
                        writer.writerow(row.to_dict())

                print(f"Data updated for {search_name}")
            except Exception as e:
                print(f"Error while scraping {search_name}: {e}")
    finally:
        driver.quit()


def main():
    input_file = "./final.csv"
    output_file = "./fichier_combine_updated.csv"
    chunk_size = 1000  # Adjust based on your needs and available memory

    # Create output file with header if it doesn't exist
    if not os.path.exists(output_file):
        df = pd.read_csv(input_file, nrows=0, delimiter=";")
        df.to_csv(output_file, index=False, sep=";")

    # Read already processed companies
    processed_companies = set()
    try:
        df_processed = pd.read_csv(output_file, usecols=["company_name"], delimiter=";")
        processed_companies = set(df_processed["company_name"])
    except Exception as e:
        print(f"Error reading processed companies: {e}")

    # Use a Manager to create a shareable Lock
    with Manager() as manager:
        lock = manager.Lock()

        # Process file in chunks
        with pd.read_csv(input_file, chunksize=chunk_size, delimiter=";") as reader:
            for chunk in reader:
                # Filter out already processed companies
                chunk = chunk[~chunk["company_name"].isin(processed_companies)]

                if not chunk.empty:
                    # Create a process pool
                    with multiprocessing.Pool() as pool:
                        # Split the chunk into sub-chunks for each process
                        num_processes = multiprocessing.cpu_count()
                        sub_chunks = np.array_split(chunk, num_processes)

                        # Start parallel processing
                        pool.starmap(
                            process_chunk,
                            [
                                (sub_chunk, output_file, lock)
                                for sub_chunk in sub_chunks
                            ],
                        )


if __name__ == "__main__":
    multiprocessing.freeze_support()  # Necessary for Windows
    main()
