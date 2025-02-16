# Scraping Scripts Overview

The different scrapping scripts are located in the `scrapping` folder. Each script is responsible for scrapping a specific website. The scripts are written in Python and use the `BeautifulSoup` library to parse the HTML content of the websites. The data is then stored in a CSV file in the `data` folder.

The `load_big_scrapped_company.py` script is responsible for loading the data from the CSV files into the database. The script reads the CSV files and inserts the data into the corresponding tables in the database. It creates a temporary table to store the data and then inserts the data into the main table.

The `load_small_scrapped_company.py` script is responsible for loading the data from the CSV files into the database. The script reads the CSV files and inserts the data into the corresponding tables in the database. It processes the data and inserts it into the main table by batch.
