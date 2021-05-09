from urllib import request
from bs4 import BeautifulSoup as BS
import re
import csv
import io
import time

#setting starting time
start = time.time()

#Part 1: scraping all the links
##########################################################
#reading initial url and feeding BS
url = 'https://vcahospitals.com/know-your-pet/cat-breeds'
html = request.urlopen(url)
bs = BS(html.read(), 'html.parser')

#finding urls
tags = bs.find_all('div',{'class':'content-wrapper callout-list-wrapper'})

#creating empty list of store each cat url
links_bs = []
#looping through tags to append list with complete urls
for i in tags:
    for j in i.find_all('a'):
        links_bs.append('https://vcahospitals.com' + j['href'])


#Part 2: Scraping data of specific cat
###########################################################################################
#creating empty list for storing output data
output_list = []
#adding first row to the empty list, this row is colnames for the data
output_list.append(['name', 'lifespan', 'weight','lap_cat','intelligence','ease_of_training',
      'grooming_requirements','shedding','good_with_children','good_with_dogs',
      'chattiness','history','behavior','look','grooming','nutritrional_needs',
      'fun_facts'])

#creating function that scrape data about single cat
def details_all(url):
    #requesting supplied url and feeding BS
    html = request.urlopen(url)
    bs = BS(html.read(), 'html.parser')

    #geting cat name, lifespan, weight - this part of the data is in header
    name = bs.find('h1').get_text()
    lifespan = bs.find('p', {'class': 'life-span'}).strong.get_text()
    weight = bs.find('p', {'class': 'weight'}).strong.get_text()
    #saving this data to temporary list
    foo_list = [name, lifespan, weight]

    #getting cat traits
    traits = bs.find_all('li', {'class': 'clearfix'})
    #there are 8 traits so I create temporary list of size 8
    stars = [0] * 8
    #looping through scraped elements named traits
    #counting how many active points each trait has
    for i in range(8):
        try:
            stars[i] = len(traits[i].find_all('li', {'class': 'active'}))
        except:
            stars[i] = 0
    #extending foo_list with traits values
    foo_list.extend(stars)

    #extracting text data about cat description
    history = bs.find(text=re.compile("History")).parent.find_next_sibling().get_text(strip=True, separator=' ')
    behavior = bs.find(text=re.compile("Behavior")).parent.find_next_sibling().get_text(strip=True, separator=' ')
    look = bs.find(text=re.compile("Look")).parent.find_next_sibling().get_text(strip=True, separator=' ')
    grooming = bs.find(text=re.compile("Nutritional")).parent.find_previous_sibling().get_text(strip=True, separator=' ')
    nutritrional_needs = bs.find(text=re.compile("Nutritional")).parent.find_next_sibling().get_text(strip=True, separator=' ')
    fun_facts = bs.find(text=re.compile("Fun Facts")).parent.find_next_sibling().get_text(strip=True, separator=' ')

    #extending foo_list with all the text data above
    foo_list.extend([history,behavior,look,grooming,nutritrional_needs,fun_facts])

    #appending output lust with foo_list
    #function will append global output_list
    output_list.append(foo_list)

#looping through links and applying to each of them, function that we created above
#we print also progress of the scraper
i=1
mian = str(len(links_bs))
for link in links_bs:
    print("Progress: " + str(i) + "/" + mian)
    details_all(link)
    i = i+1

#saving data to csv
with io.open('data_cats.csv', mode='w', encoding="utf-8") as csv_file:
    data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data.writerows(output_list)

end = time.time()
#printing how much time scraper worked
print("Beautiful Soup scraper ran in " + str(round(end-start,2)) + " seconds.")