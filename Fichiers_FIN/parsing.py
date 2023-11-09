import csv
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# Helper functions for browser setup and random sleep times
def sleep_time():
    time.sleep(random.randint(2, 4))

def configure_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_company_info(driver, company_name, adresse):
    time.sleep(1)
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

    # Click on Maps link if it exists
    #try:
    #    driver.find_element(By.LINK_TEXT, "Maps").click()
    #    sleep_time()
    #except NoSuchElementException:
    #    pass

    # Get reviews, if present
    reviews = []
    try:
        button_plus = driver.find_elements(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]/div[2]/div[2]')
        if button_plus:
            button_plus[0].click()
        sleep_time()

        # Expand all the reviews if the button is present
        review_expand_buttons = driver.find_elements(By.CLASS_NAME, "w8nwRe")
        for button in review_expand_buttons:
            button.click()
        sleep_time()

        reviews = extract_reviews(driver)

    except NoSuchElementException:
        reviews = "No reviews found"

    company_info = {
        "Adresse": adresse,
        "Téléphone": phone,
        "Site web": website,
        "Reviews": reviews
    }


    return company_info

def extract_reviews(driver):
    # Extract the reviews details
    authors_elements = driver.find_elements(By.CLASS_NAME, "d4r55")
    text_elements = driver.find_elements(By.CLASS_NAME, "wiI7pd")
    stars_elements = driver.find_elements(By.CLASS_NAME, "kvMYJc")

    reviews = []
    for i in range(len(authors_elements)):
        author = authors_elements[i].text if i < len(authors_elements) else "No author"
        text = text_elements[i].text if i < len(text_elements) else "No comment"
        stars_label = stars_elements[i].get_attribute("aria-label") if i < len(stars_elements) else "No rating"
        stars = stars_label.split()[0] if stars_label else "No rating"
        reviews.append({"author": author, "text": text, "stars": stars})

    return reviews

def extract_phone_number(driver):
    # Extract the phone number
    phone = ""
    try:
        phone = driver.find_element(By.CLASS_NAME.startswith("Appeler le")).text
    except NoSuchElementException:
        phone = "No phone number found"

    return phone

def extract_address(driver):
    # Extract the address
    address = ""
    try:
        address = driver.find_element(By.LINK_TEXT, "Adresse")
        address = address.find_element(By.XPATH, "./following-sibling::span").text
    except NoSuchElementException:
        address = "No address found"

    return address

def extract_website(driver):
    # Extract the website
    website = ""
    try:
        website = driver.find_element(By.LINK_TEXT, "Site web")
        website = website.find_element(By.CLASS_NAME, "ab_button").text
    except NoSuchElementException:
        website = "No website found"

    return website

def extract_schedule(driver):
    # Extract the schedule
    schedule = ""
    try:
        schedule = driver.find_element(By.CSS_SELECTOR, "tr").text
    except NoSuchElementException:
        schedule = "No schedule found"

    return schedule

def extract_instagram(driver):
    # Extract the instagram through the url starting by https://www.instagram.com/
    instagram = ""
    try:
        instagram = driver.find_element(By.LINK_TEXT, "Instagram")
        instagram = instagram.find_element(By.CLASS_NAME, "ab_button").text
    except NoSuchElementException:
        instagram = "No instagram found"

    return instagram

def extract_facebook(driver):
    # Extract the facebook through the url starting by https://www.facebook.com/
    facebook = ""
    try:
        facebook = driver.find_element(By.LINK_TEXT, "Facebook")
        facebook = facebook.find_element(By.CLASS_NAME, "ab_button").text
    except NoSuchElementException:
        facebook = "No facebook found"

    return facebook 

def extract_twitter(driver):
    # Extract the twitter through the url starting by https://twitter.com/
    twitter = ""
    try:
        twitter = driver.find_element(By.LINK_TEXT, "Twitter")
        twitter = twitter.find_element(By.CLASS_NAME, "ab_button").text
    except NoSuchElementException:
        twitter = "No twitter found"

    return twitter

def extract_linkedin(driver):
    # Extract the linkedin through the url starting by https://www.linkedin.com/
    linkedin = ""
    try:
        linkedin = driver.find_element(By.LINK_TEXT, "LinkedIn")
        linkedin = linkedin.find_element(By.CLASS_NAME, "ab_button").text
    except NoSuchElementException:
        linkedin = "No linkedin found"

    return linkedin

def extract_youtube(driver):
    # Extract the youtube through the url starting by https://www.youtube.com/
    youtube = ""
    try:
        youtube = driver.find_element(By.LINK_TEXT, "YouTube")
        youtube = youtube.find_element(By.CLASS_NAME, "ab_button").text
    except NoSuchElementException:
        youtube = "No youtube found"

    return youtube

def extract_email(driver):
    # Extract the email through the url starting by mailto:
    email = ""
    try:
        email = driver.find_element(By.LINK_TEXT, "Email")
    except NoSuchElementException:
        email = "No email found"

    return email


# Read the CSV, search for each company, and update the information
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
        new_fieldnames = ["Téléphone", "Site web", "Reviews"]
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