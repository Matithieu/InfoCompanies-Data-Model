import csv
import os
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import multiprocessing
from multiprocessing import Manager
import pandas as pd
import numpy as np
import re


def sleep_time():
    time.sleep(random.randint(1, 2))


def configure_selenium():
    # https://googlechromelabs.github.io/chrome-for-testing/
    path = "./Parsing/chromedriver-mac-arm64/chromedriver"
    driver = uc.Chrome(
        headless=False,
        use_subprocess=True,
    )
    return driver


def is_captcha_page(driver):
    try:
        # Check if CAPTCHA iframe is present
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//iframe[@title="reCAPTCHA"]'))
        )
        print("CAPTCHA detected.")
        return True
    except TimeoutException:
        return False


def scrape_company_info(driver, company_name, adresse):
    driver.get(f"https://www.google.com/search?q={company_name} {adresse}")
    time.sleep(2)

    if is_captcha_page(driver):
        time.sleep(20)  # Wait 20 seconds as instructed and stop execution
        driver.quit()
        raise Exception("CAPTCHA encountered, stopping the script.")

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
        # Try extracting phone number from span with aria-label
        phone_element = driver.find_element(
            By.XPATH, "//span[contains(@aria-label, 'Appeler le')]"
        )
        phone = phone_element.text
    except NoSuchElementException:
        try:
            # If not found, try extracting from div containing 'Téléphone :'
            phone_div = driver.find_element(
                By.XPATH, "//div[contains(text(), 'Téléphone')]"
            )
            phone = phone_div.text.split(":")[-1].strip()
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
    day_of_the_week = [
        "lundi",
        "mardi",
        "mercredi",
        "jeudi",
        "vendredi",
        "samedi",
        "dimanche",
    ]
    schedule = {}

    # Regular expression to match valid time ranges, e.g., "09:00–12:00" or "Fermé"
    valid_hours_pattern = re.compile(r"^(\d{2}:\d{2}–\d{2}:\d{2}|Fermé)$")

    try:
        tables = driver.find_elements(By.TAG_NAME, "table")
        for table in tables:
            day_elements = table.find_elements(By.XPATH, ".//tbody/tr/td[1]")
            if day_elements:
                for day_elem in day_elements:
                    day = day_elem.get_attribute("textContent").strip().lower()
                    if day in day_of_the_week:
                        hours_elements = table.find_elements(
                            By.XPATH, f".//tbody/tr[td[1][text()='{day}']]/td[2]"
                        )
                        if hours_elements:
                            hours_text = (
                                hours_elements[0].get_attribute("textContent").strip()
                            )
                            # Validate the extracted hours text using the pattern
                            if valid_hours_pattern.match(hours_text):
                                schedule[day] = hours_text
                            else:
                                schedule[day] = ""
                        else:
                            schedule[day] = ""
    except NoSuchElementException as e:
        print(f"Could not extract schedule for {company_name}: {e}")
        schedule = {}
    except IndexError as e:
        print(f"IndexError while extracting schedule for {company_name}: {e}")
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

        # Regular expression to extract only digits, commas, and dots for stars
        valid_star_pattern = re.compile(r"^\d+[.,]?\d*$")
        # Regular expression to extract only digits for the number of reviews
        valid_number_pattern = re.compile(r"^\d+$")

        if stars_elements and len(stars_elements) > 0:
            # Safely split the aria-label and ensure there are enough parts
            aria_label = stars_elements[0].get_attribute("aria-label")
            parts = aria_label.split()
            if len(parts) >= 3:  # Ensure there are at least 3 parts in the split list
                stars_value = parts[2]  # The 3rd element should be the star rating
                # Validate if the extracted value matches the star pattern
                if valid_star_pattern.match(stars_value):
                    reviews["stars"] = stars_value.replace(
                        ",", "."
                    )  # Normalize to a dot for consistency
                else:
                    reviews["stars"] = ""
            else:
                reviews["stars"] = ""
        else:
            reviews["stars"] = ""

        if number_of_reviews_elements and len(number_of_reviews_elements) > 0:
            # Extract the number of reviews safely
            number_of_reviews_text = number_of_reviews_elements[0].text.split()
            if len(number_of_reviews_text) > 0:
                reviews_value = number_of_reviews_text[0]
                # Validate if the extracted value is numeric
                if valid_number_pattern.match(reviews_value):
                    reviews["number_of_reviews"] = reviews_value
                else:
                    reviews["number_of_reviews"] = ""
            else:
                reviews["number_of_reviews"] = ""
        else:
            reviews["number_of_reviews"] = ""

    except NoSuchElementException:
        reviews = {"stars": "", "number_of_reviews": ""}

    except IndexError as e:
        print(f"IndexError while extracting reviews: {e}")
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
                break  # Exit if CAPTCHA is encountered
    finally:
        driver.quit()


def main():
    input_file = "./ETL/data/output/final.csv"
    output_file = "./fichier_combine_updated.csv"
    chunk_size = 500

    # Create the output file if it doesn't exist
    if not os.path.exists(output_file):
        df = pd.read_csv(input_file, nrows=0, delimiter=";")
        df.to_csv(output_file, index=False, sep=";")

    # Track processed SIREN numbers
    processed_companies = set()
    try:
        df_processed = pd.read_csv(
            output_file,
            usecols=["siren_number"],
            delimiter=";",
            dtype={"siren_number": str},  # Ensure SIREN is read as string
        )
        processed_companies = set(df_processed["siren_number"])
    except Exception as e:
        print(f"Error reading processed SIRENs: {e}")

    # Use multiprocessing with a Manager for thread-safe lock
    with Manager() as manager:
        lock = manager.Lock()

        try:
            # Read the input file in chunks
            with pd.read_csv(
                input_file,
                chunksize=chunk_size,
                delimiter=";",
                dtype={"siren_number": str},  # Ensure SIREN is read as string
            ) as reader:
                for chunk in reader:
                    # Filter out rows with SIRENs already processed
                    chunk = chunk[~chunk["siren_number"].isin(processed_companies)]

                    if not chunk.empty:
                        # Split the chunk into sub-chunkzs for parallel processing
                        num_processes = max(
                            1, multiprocessing.cpu_count() - 1
                        )  # Reserve one core
                        # num_processes = 1  # Debugging with 1 process
                        sub_chunks = np.array_split(chunk, num_processes)

                        # Create a multiprocessing pool
                        with multiprocessing.Pool(processes=num_processes) as pool:
                            try:
                                # Process sub-chunks in parallel
                                pool.starmap(
                                    process_chunk,
                                    [
                                        (sub_chunk, output_file, lock)
                                        for sub_chunk in sub_chunks
                                    ],
                                )
                            except KeyboardInterrupt:
                                print(
                                    "\033[91mInterruption detected! Cleanly shutting down processes...\033[0m"
                                )
                                pool.terminate()  # Immediately stop the workers
                                pool.join()  # Wait for the processes to finish
                                print("\033[91mAll processes have been stopped.\033[0m")
                                return  # Cleanly exit the main function

        except KeyboardInterrupt:
            print("\033[91mManual interruption detected. Stopping the program.\033[0m")


if __name__ == "__main__":
    multiprocessing.freeze_support()  # Necessary for Windows
    main()


# Debugging purposes
# if __name__ == "__main__":
#     driver = configure_selenium()
#     company_info = scrape_company_info(
#         driver, "Computerline", "1411 Rte de la Côté d'Azur"
#     )
#     print(company_info)
