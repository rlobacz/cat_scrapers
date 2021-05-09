# Instruction
This repository consist 3 scrapers that scrape data about cats. Each scraper is located in separate folder.

***BeautifulSoup*** <br>
To run this scraper user should type in terminal: python soup_scraper.py <br>
This will initate scraping procedure and produce csv file with output, named: data_cats.csv
Library requirements: urllib, bs4, re, csv, io, time

***Scrapy*** <br>
To run this scraper user should type in terminal: scrapy crawl cats -o data_cats.csv <br>
This will initate scraping procedure and produce csv file with output, named: data_cats.csv
Library requirements: scrapy

***Selenium*** <br>
To run this scraper user should type in terminal: python sel_scraper.py <br>
This will initate scraping procedure and produce csv file with output, named: seleniumCatsData.csv
Library requirements: selenium, time, pandas, re
