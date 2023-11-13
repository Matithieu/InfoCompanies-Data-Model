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
        "Phone": extract_phone_number(driver),
        "Website": extract_website(driver),
        "Schedule": extract_schedule(driver),
        "Instagram": extract_instagram(driver),
        "Facebook": extract_facebook(driver),
        "Twitter": extract_twitter(driver),
        "LinkedIn": extract_linkedin(driver),
        "Youtube": extract_youtube(driver),
        "Email": extract_email(driver),
        "DateOfScraping": time.strftime("%Y-%m-%d"),
        "Reviews": extract_reviews(driver),
    }
    
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
        list_review_button = driver.find_element(
            By.XPATH, "//span[contains(text(), 'avis Google')]"
        )
        list_review_button.click()

        time.sleep(3)

        rows = driver.find_elements(By.CLASS_NAME, "gws-localreviews__google-review")
        for row in rows:
            try:
                author = row.find_element(
                    By.XPATH,
                    ".//img[contains(@src, 'https://lh3.googleusercontent.com/')]",
                )
                author = author.get_attribute("alt")
                stars = row.find_element(
                    By.XPATH, ".//*[contains(@aria-label, 'Note')]"
                )
                stars = stars.get_attribute("aria-label")
                note = stars.split()[2]  # Assuming the format "Note: 4.5 out of 5"

                review_text = ""
                try:
                    extended_review_button = row.find_elements(
                        By.XPATH, ".//a[@class='review-more-link']"
                    )
                    if extended_review_button:
                        extended_review_button[0].click()

                    time.sleep(1)  # Wait for the review to expand
                    review_text = row.find_element(
                        By.XPATH, ".//span[@data-expandable-section]"
                    ).text
                except NoSuchElementException:
                    # Handle the case where the 'Plus' button is not present
                    review_text = row.find_element(
                        By.XPATH, ".//span[@data-expandable-section]"
                    )
                    review_text = (
                        review_text.text if review_text else "Review text not available"
                    )

                reviews.append({"author": author, "text": review_text, "stars": note})
            except NoSuchElementException:
                print("Problem finding review elements")
                continue

    except NoSuchElementException:
        reviews = "No reviews found"

    return reviews

filename = './fichier_combine.csv'
updated_filename = './fichier_combine_updated.csv'

# Vérifiez si le fichier mis à jour existe et doit inclure les entêtes
file_exists = os.path.isfile(updated_filename)
number_of_iteraites = 0     
updated_companies_info = {}

# Vérifiez si le fichier mis à jour existe et doit inclure les entêtes
file_exists = os.path.isfile(updated_filename)
if file_exists:
    with open(updated_filename, mode='r', encoding='utf-8') as updated_file:
        reader = csv.DictReader(updated_file, delimiter=';')
        for row in reader:
            # Utilisez la Dénomination de l'entreprise comme clé pour le dictionnaire
            updated_companies_info[row['Dénomination']] = row

driver = configure_selenium()

try:
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        # Enregistrer les entêtes existants et ajouter les nouveaux
        existing_fieldnames = reader.fieldnames.copy()
        new_fieldnames = ["Phone", "Website", "Reviews", "Schedule", "Instagram", "Facebook", "Twitter", "LinkedIn", "Youtube", "Email", "DateOfScraping"]
        for field in new_fieldnames:
            if field not in existing_fieldnames:
                existing_fieldnames.append(field)

        # Ouvrez le fichier CSV pour la mise à jour en mode écriture
        with open(updated_filename, mode='a+', encoding='utf-8', newline='') as updated_file:
            updated_file.seek(0)  # Allez au début du fichier pour vérifier les en-têtes
            first_line = updated_file.readline()
            if not first_line:  # Si le fichier est vide, écrivez les en-têtes
                writer = csv.DictWriter(updated_file, fieldnames=existing_fieldnames, delimiter=';')
                writer.writeheader()
            else:  # Sinon, créez simplement le writer sans écrire les en-têtes
                writer = csv.DictWriter(updated_file, fieldnames=existing_fieldnames, delimiter=';')

            # Retournez à la fin du fichier pour commencer à écrire
            updated_file.seek(0, os.SEEK_END)

            for line in reader:
                search_name = line['Dénomination']
                adresse = line['Adresse']
                
                # Vérifiez si les informations sont déjà présentes dans le dictionnaire
                company_info = updated_companies_info.get(search_name)
                if company_info and all(company_info.get(field, '').strip() for field in new_fieldnames):
                    print(f"Les informations pour {search_name} existent déjà. Passage à l'élément suivant.")
                    continue  # Passez à la ligne suivante sans rescraping
                
                # Si les informations sont manquantes, lancez le script de scraping
                try:
                    company_info = scrape_company_info(driver, search_name, adresse)
                    line.update(company_info)
                    writer.writerow(line)  # Écrire la ligne mise à jour immédiatement dans le fichier CSV
                    print(f"Informations mises à jour pour {search_name}")
                    number_of_iteraites += 1
                except KeyboardInterrupt:
                    # Si l'utilisateur interrompt le programme, sortez de la boucle
                    print(" Interruption par l'utilisateur. Fin de la mise à jour.")
                    print(f"Nombre d'itérations: {number_of_iteraites}")

                    break
                except Exception as e:
                    print(f"Erreur lors de la récupération des informations pour {search_name}: {e}")
except KeyboardInterrupt:
    print("Interruption par l'utilisateur avant la lecture du CSV.")
    print(f"Nombre d'itérations: {number_of_iteraites}")
except Exception as e:
    print(f"Erreur globale: {e}")
finally:
    driver.quit()