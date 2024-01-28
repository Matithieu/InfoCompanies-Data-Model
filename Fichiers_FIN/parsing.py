import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import NoSuchElementException

import time
import random


# Helper functions for browser setup and random sleep times
def sleep_time():
    time.sleep(random.randint(1, 2))


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
        "Phone": extract_phone_number(driver),
        "Website": extract_website(driver),
        "Instagram": extract_instagram(driver),
        "Facebook": extract_facebook(driver),
        "Twitter": extract_twitter(driver),
        "LinkedIn": extract_linkedin(driver),
        "Youtube": extract_youtube(driver),
        "Email": extract_email(driver),
        "DateOfScrapping": time.strftime("%Y-%m-%d"),
        "Reviews": extract_reviews(driver),
        "Schedule": extract_schedule(driver, company_name),
    }

    return company_info


def extract_phone_number(driver):
    # Extract the phone number
    phone = ""
    try:
        phone_element = driver.find_element(
            By.XPATH, "//span[contains(@aria-label, 'Appeler le')]"
        )
        phone = phone_element.text
    except NoSuchElementException:
        phone = ""

    return phone


def extract_address(driver):
    # Extract the address without relying on class names
    address = ""
    try:
        # This XPATH finds the anchor element containing the text 'Adresse'
        # Then gets the following sibling that contains the address text
        address_element = driver.find_element(
            By.XPATH, "//a[contains(text(), 'Adresse')]/following::span[2]"
        )
        address = address_element.text
    except NoSuchElementException:
        address = ""

    return address


def extract_website(driver):
    # Extract the website URL
    website = ""
    try:
        # This XPath looks for an 'a' element with a 'div' child that contains the text 'Site Web'
        website_element = driver.find_element(By.XPATH, '//a[contains(.,"Site Web")]')
        website = website_element.get_attribute("href")
    except NoSuchElementException:
        website = ""

    return website


from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def extract_schedule(driver, company_name):
    # Extract the schedule from the table
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
        # Find all tables in the page
        tables = driver.find_elements(By.TAG_NAME, "table")

        # Iterate over each table
        for table in tables:
            # Check if the table contains the days of the week in the first column
            day_column = table.find_elements(By.XPATH, ".//tbody/tr/td[1]")

            # Check if the day_column has elements
            if day_column:
                # Iterate over the days in the first column
                for day_elem in day_column:
                    day = day_elem.get_attribute("textContent").strip().lower()

                    # Check if the day is in the list of daysOfTheWeek
                    if day in dayOfTheWeek:
                        # Find the corresponding hours in the second column
                        hours_td_list = table.find_elements(
                            By.XPATH,
                            ".//tbody/tr[td[1][text()='{}']]/td[2]".format(day),
                        )

                        # Check if elements exist in the list before accessing them
                        if hours_td_list:
                            # Iterate over the list of hours_td elements to get the text content for each one
                            for hours_td in hours_td_list:
                                hours_text = hours_td.get_attribute(
                                    "textContent"
                                ).strip()

                            schedule[day] = hours_text
                        else:
                            schedule[day] = ""

    except NoSuchElementException as e:
        print(f"Could not extract schedule for {company_name}: {e}")
        schedule = ""

    return schedule


def extract_instagram(driver):
    # Extract the Instagram URL
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
    # Extract the Facebook URL
    facebook = ""
    try:
        # Since the href attribute contains the full Facebook URL, we can directly get it
        facebook_element = driver.find_element(
            By.XPATH, "//a[contains(@href, 'https://www.facebook.com/')]"
        )
        facebook = facebook_element.get_attribute("href")
    except NoSuchElementException:
        facebook = ""
    return facebook


def extract_twitter(driver):
    # Extract the Twitter URL
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
    # Extract the LinkedIn URL
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
    # Extract the YouTube URL
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
    # Extract the email through the url starting by mailto:
    email = ""
    try:
        email = driver.find_element(By.LINK_TEXT, "Email")
    except NoSuchElementException:
        email = ""

    return email


def extract_reviews(driver):
    # Extract the stars and the number of reviews
    reviews = {}
    try:
        # Updated XPath expressions
        stars_elements = driver.find_elements(
            By.XPATH, "//span[contains(@aria-label, 'Note')]"
        )
        number_of_reviews_elements = driver.find_elements(
            By.XPATH, "//a[contains(text(), 'avis')]"
        )

        # Check if elements exist in the lists before accessing them
        if stars_elements:
            reviews["stars"] = stars_elements[0].get_attribute("aria-label").split()[2]
        else:
            reviews["stars"] = ""

        if number_of_reviews_elements:
            reviews["number_of_reviews"] = number_of_reviews_elements[0].text.split()[0]
        else:
            reviews["number_of_reviews"] = ""

    except NoSuchElementException:
        reviews = {}

    return reviews


# def extract_reviews(driver):
#     try:
#         reviews = []
#         list_review_button = driver.find_element(
#             By.XPATH, "//span[contains(text(), 'avis')]"
#         )
#         list_review_button.click()

#         time.sleep(3)

#         rows = driver.find_elements(By.CLASS_NAME, "gws-localreviews__google-review")
#         for row in rows:
#             try:
#                 author = row.find_element(
#                     By.XPATH,
#                     ".//img[contains(@src, 'https://lh3.googleusercontent.com/')]",
#                 )
#                 author = author.get_attribute("alt")
#                 stars = row.find_element(
#                     By.XPATH, ".//*[contains(@aria-label, 'Note')]"
#                 )
#                 stars = stars.get_attribute("aria-label")
#                 note = stars.split()[2]  # Assuming the format "Note: 4.5 out of 5"

#                 review_text = ""
#                 try:
#                     extended_review_button = row.find_elements(
#                         By.XPATH, ".//a[@class='review-more-link']"
#                     )
#                     if extended_review_button:
#                         extended_review_button[0].click()

#                     time.sleep(1)  # Wait for the review to expand
#                     review_text = row.find_element(
#                         By.XPATH, ".//span[@data-expandable-section]"
#                     ).text
#                 except NoSuchElementException:
#                     # Handle the case where the 'Plus' button is not present
#                     review_text = row.find_element(
#                         By.XPATH, ".//span[@data-expandable-section]"
#                     )
#                     review_text = (
#                         review_text.text if review_text else "Review text not available"
#                     )

#                 reviews.append({"author": author, "text": review_text, "stars": note})
#             except NoSuchElementException:
#                 print("Problem finding review elements")
#                 continue

#     except NoSuchElementException:
#         reviews = ""

#     return reviews


filename = "./fichier_combine.csv"
updated_filename = "./fichier_combine_updated.csv"

file_exists = os.path.isfile(updated_filename)
number_of_iteraites = 0
updated_companies_info = {}

# Verify if the updated file exists and needs to include the headers
file_exists = os.path.isfile(updated_filename)
if file_exists:
    with open(updated_filename, mode="r", encoding="utf-8") as updated_file:
        reader = csv.DictReader(updated_file, delimiter=";")
        for row in reader:
            # Use the company name as key for the dictionary
            updated_companies_info[row["Dénomination"]] = row

driver = configure_selenium()

try:
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        # Save the existing headers and add the new ones
        existing_fieldnames = reader.fieldnames.copy()
        new_fieldnames = [
            "Phone",
            "Website",
            "Reviews",
            "Schedule",
            "Instagram",
            "Facebook",
            "Twitter",
            "LinkedIn",
            "Youtube",
            "Email",
            "DateOfScrapping",
        ]
        for field in new_fieldnames:
            if field not in existing_fieldnames:
                existing_fieldnames.append(field)

        # Open the CSV file for updating in write mode
        with open(
            updated_filename, mode="a+", encoding="utf-8", newline=""
        ) as updated_file:
            updated_file.seek(
                0
            )  # Go to the beginning of the file to check if it's empty
            first_line = updated_file.readline()
            if not first_line:  # If the file is empty, write the headers
                writer = csv.DictWriter(
                    updated_file, fieldnames=existing_fieldnames, delimiter=";"
                )
                writer.writeheader()
            else:  # Else, append to the existing file
                writer = csv.DictWriter(
                    updated_file, fieldnames=existing_fieldnames, delimiter=";"
                )

            # Return to the end of the file to start writing
            updated_file.seek(0, os.SEEK_END)

            for line in reader:
                search_name = line["Dénomination"]
                adresse = line["Ville"]

                # Verify if the information is already present in the dictionary
                company_info = updated_companies_info.get(search_name)
                if (
                    company_info
                    and "Dénomination" in company_info
                    and company_info["Dénomination"].strip()
                ):
                    continue  # If the company is already present, skip it

                # If the information is missing, launch the scraping script
                try:
                    company_info = scrape_company_info(driver, search_name, adresse)
                    line.update(company_info)
                    writer.writerow(
                        line
                    )  # Write in the file the updated information for the company
                    print(f"Data updated for {search_name}")
                    number_of_iteraites += 1
                except KeyboardInterrupt:
                    # If the user interrupts the program, exit the loop
                    print("Stoppped by the user. End of update.")
                    print(f"Number of iterations : {number_of_iteraites}")

                    break
                except Exception as e:
                    print(f"Error while scraping {search_name} : {e}")
except KeyboardInterrupt:
    print("Interrupted by the user. End of update.")
    print(f"Number of iterations: {number_of_iteraites}")
except Exception as e:
    print(f"Global error: {e}")
finally:
    driver.quit()
