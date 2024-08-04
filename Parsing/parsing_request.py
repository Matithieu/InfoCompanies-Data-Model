import csv
import datetime
import os
import requests
from bs4 import BeautifulSoup
import time
import random


# Helper function for random sleep times
def sleep_time():
    time.sleep(random.randint(1, 2))


def fetch_html(company_name, adresse):
    url = f"https://www.google.com/search?q={company_name} {adresse}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0"
    }
    now = datetime.datetime.now()
    cookies = {
        "CONSENT": "PENDING+987",
        "SOCS": "CAESHAgBEhJnd3NfMjAyMzA4MTAtMF9SQzIaAmRlIAEaBgiAo_CmBg",
    }
    response = requests.get(url, headers=headers, cookies=cookies)
    return response.text


def scrape_company_info(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    company_info = {
        "phone_number": extract_phone_number(soup),
        "website": extract_website(soup),
        "instagram": extract_instagram(soup),
        "facebook": extract_facebook(soup),
        "twitter": extract_twitter(soup),
        "linkedin": extract_linkedin(soup),
        "youtube": extract_youtube(soup),
        "email": extract_email(soup),
        "scraping_date": time.strftime("%Y-%m-%d"),
        "reviews": extract_reviews(soup),
        "schedule": extract_schedule(soup),
    }

    return company_info


def extract_phone_number(soup):
    phone = ""
    # Try to find the phone number with aria-label containing 'Appeler le'
    phone_element = soup.find(
        "span", attrs={"aria-label": lambda x: x and "Appeler le" in x}
    )

    if phone_element:
        phone = phone_element.get_text().strip()
    else:
        # Alternative method to find phone number if aria-label method fails
        potential_phones = soup.find_all("span")
        for span in potential_phones:
            if span.get_text().strip().replace(" ", "").isdigit():
                phone = span.get_text().strip()
                break

    return phone


def extract_address(soup):
    address = ""
    address_element = soup.find("a", text="Adresse")
    if address_element and address_element.find_next("span"):
        address = address_element.find_next("span").get_text()
    return address


def extract_website(soup):
    website = ""
    website_element = soup.find("a", string="Site Web")
    if website_element:
        website = website_element.get("href")
    return website


def extract_schedule(soup):
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
    tables = soup.find_all("table")

    for table in tables:
        day_column = table.find_all(
            "td", string=lambda x: x and x.strip().lower() in dayOfTheWeek
        )
        for day_elem in day_column:
            day = day_elem.get_text().strip().lower()
            hours_td = day_elem.find_next_sibling("td")
            if hours_td:
                schedule[day] = hours_td.get_text().strip()
            else:
                schedule[day] = ""
    return schedule


def extract_instagram(soup):
    instagram = ""
    instagram_element = soup.find(
        "a", href=lambda x: x and "https://www.instagram.com/" in x
    )
    if instagram_element:
        instagram = instagram_element.get("href")
    return instagram


def extract_facebook(soup):
    facebook = ""
    facebook_element = soup.find(
        "a", href=lambda x: x and "https://www.facebook.com/" in x
    )
    if facebook_element:
        facebook = facebook_element.get("href")
    return facebook


def extract_twitter(soup):
    twitter = ""
    twitter_element = soup.find("a", href=lambda x: x and "https://twitter.com/" in x)
    if twitter_element:
        twitter = twitter_element.get("href")
    return twitter


def extract_linkedin(soup):
    linkedin = ""
    linkedin_element = soup.find(
        "a", href=lambda x: x and "https://www.linkedin.com/" in x
    )
    if linkedin_element:
        linkedin = linkedin_element.get("href")
    return linkedin


def extract_youtube(soup):
    youtube = ""
    youtube_element = soup.find(
        "a", href=lambda x: x and "https://www.youtube.com/" in x
    )
    if youtube_element:
        youtube = youtube_element.get("href")
    return youtube


def extract_email(soup):
    email = ""
    email_element = soup.find("a", href=lambda x: x and "mailto:" in x)
    if email_element:
        email = email_element.get("href").replace("mailto:", "")
    return email


def extract_reviews(soup):
    reviews = {}
    stars_element = soup.find("span", attrs={"aria-label": lambda x: x and "Note" in x})
    reviews_element = soup.find("a", string=lambda x: x and "avis" in x)

    if stars_element:
        reviews["stars"] = stars_element.get("aria-label").split()[2]
    else:
        reviews["stars"] = ""

    if reviews_element:
        reviews["number_of_reviews"] = reviews_element.get_text().split()[0]
    else:
        reviews["number_of_reviews"] = ""

    return reviews


filename = "./renamedColumns.csv"
updated_filename = "./fichier_combine_updated.csv"

file_exists = os.path.isfile(updated_filename)
number_of_iterations = 0
updated_companies_info = {}

if file_exists:
    with open(updated_filename, mode="r", encoding="utf-8") as updated_file:
        reader = csv.DictReader(updated_file, delimiter=";")
        for row in reader:
            updated_companies_info[row["company_name"]] = row

try:
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        existing_fieldnames = reader.fieldnames.copy()
        new_fieldnames = [
            "phone_number",
            "website",
            "reviews",
            "schedule",
            "instagram",
            "facebook",
            "twitter",
            "linkedin",
            "youtube",
            "email",
            "scraping_date",
        ]
        for field in new_fieldnames:
            if field not in existing_fieldnames:
                existing_fieldnames.append(field)

        with open(
            updated_filename, mode="a+", encoding="utf-8", newline=""
        ) as updated_file:
            updated_file.seek(0)
            first_line = updated_file.readline()
            if not first_line:
                writer = csv.DictWriter(
                    updated_file, fieldnames=existing_fieldnames, delimiter=";"
                )
                writer.writeheader()
            else:
                writer = csv.DictWriter(
                    updated_file, fieldnames=existing_fieldnames, delimiter=";"
                )

            updated_file.seek(0, os.SEEK_END)

            for line in reader:
                search_name = line["company_name"]
                adresse = line["city"]

                company_info = updated_companies_info.get(search_name)
                if (
                    company_info
                    and "company_name" in company_info
                    and company_info["company_name"].strip()
                ):
                    continue

                try:
                    html_content = fetch_html(search_name, adresse)
                    company_info = scrape_company_info(html_content)
                    line.update(company_info)
                    writer.writerow(line)
                    print(f"Data updated for {search_name}")
                    number_of_iterations += 1
                except KeyboardInterrupt:
                    print("Stopped by the user. End of update.")
                    print(f"Number of iterations: {number_of_iterations}")
                    break
                except Exception as e:
                    print(f"Error while scraping {search_name}: {e}")
except KeyboardInterrupt:
    print("Interrupted by the user. End of update.")
    print(f"Number of iterations: {number_of_iterations}")
except Exception as e:
    print(f"Global error: {e}")
