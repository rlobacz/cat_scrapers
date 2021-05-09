from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import re

startTime = time.time()
dict_data = []
linki = []
allData = []

#Set up the path to the chrome driver
gecko_path = 'chromedriver.exe'

page_url = 'https://vcahospitals.com/know-your-pet/cat-breeds'
options = webdriver.chrome.options.Options()
options.headless = True
driver = webdriver.Chrome(options=options, executable_path=gecko_path)
# Parse the page source using get() function
driver.get(page_url)

element = driver.find_element_by_xpath("//*[@id='Main']/div[1]/div/div/div/div[2]")
all_links = element.find_elements_by_tag_name("a")

for link in all_links:
	a = link.get_attribute("href")
# Generate a list of links for each cat
	linki.append(a)


# Loop through each link to gather information about cats
for link in linki:

	traits=[]

# Open specyfic link
	driver.get(url=link)

# Storing values collected from the page in variables
	name_xpath = driver.find_element_by_xpath('//*[@id="Main"]/article/div/header/h1')
	lifespan_xpath = driver.find_element_by_xpath('//p[@class="life-span"]/strong')
	weight_xpath = driver.find_element_by_xpath('//p[@class="weight"]/strong')

#	For this variables we get list but list has no attribute 'text', so to get the text of each webElement we used loop to create new list with the text elements
#   Futher the items from the new list will be joined into a single sentence
	history_xpath = driver.find_elements_by_xpath('//div[@class="rich-text-panel"]/ul[1]//li')
	h=[]
	for value in history_xpath:
		h.append(value.text)

	behavior_xpath = driver.find_elements_by_xpath('//div[@class="rich-text-panel"]/ul[2]//li')
	b=[]
	for value in behavior_xpath:
		b.append(value.text)

	look_xpath = driver.find_elements_by_xpath('//div[@class="rich-text-panel"]/ul[3]//li')
	l=[]
	for value in look_xpath:
		l.append(value.text)

	grooming_xpath = driver.find_elements_by_xpath('//div[@class="rich-text-panel"]/ul[4]//li')
	g=[]
	for value in grooming_xpath:
		g.append(value.text)

# The last two sections (nutritional needs and fun facts) have different structure, so we applied conditional statements
	if driver.find_elements_by_xpath('//div[@class="rich-text-panel"]/ul[7]//li[1]'):
		nutritrional_needs_xpath = driver.find_elements_by_xpath('//div[@class="rich-text-panel"]/ul[6]//li')
		fun_facts_xpath = driver.find_elements_by_xpath('//div[@class="rich-text-panel"]/ul[7]//li')
	elif driver.find_elements_by_xpath('//div[@class="rich-text-panel"]/ul[6]//li'):
		nutritrional_needs_xpath = driver.find_elements_by_xpath('//div[@class="rich-text-panel"]/ul[5]//li')
		fun_facts_xpath = driver.find_elements_by_xpath('//div[@class="rich-text-panel"]/ul[6]//li')
	else:
		nutritrional_needs_xpath = driver.find_elements_by_xpath('//*[@id="Main"]/article/div/div/p[11]')
		fun_facts_xpath = driver.find_elements_by_xpath('//div[@class="rich-text-panel"]/ul[5]//li')

	n=[]
	for value in nutritrional_needs_xpath:
		n.append(value.text)

	f=[]
	for value in fun_facts_xpath:
		f.append(value.text)



# Seeing that xpaths are repeatable for traits, loop is used.
# On the page are missing values in trait rating (1-5), so the missing values are assumed to be zero
	for i in range(1,9):
		try:
			trait = driver.find_element_by_xpath('//div[@class="traits-container"]/ul/li[%s]/span'%(i)).text
			traits.append(trait[-6:-5])
		except:
			traits.append(0)


# Adding collected data to the dictionary
	rowData = dict(name = name_xpath.text,
			lifespan = lifespan_xpath.text,
			weight=weight_xpath.text,
			lap_cat= traits[0],
			intelligence=traits[1],
			ease_of_training=traits[2],
			grooming_requirements=traits[3],
			shedding=traits[4],
			good_with_children=traits[5],
			good_with_dogs=traits[6],
			chattiness=traits[7],
			history=' '.join(h),
			behavior=' '.join(b),
			look=' '.join(l),
			grooming =' '.join(g),
			nutritrional_needs=' '.join(n),
			fun_facts=' '.join(f)
			 )

# Creating list (allData) of dictionaries (rowData)
	allData.append(rowData)

# Saving data into a CSV file
df = pd.DataFrame(allData)
df.to_csv("seleniumCatsData.csv", sep=";", index=False)

# Closing the current open window on which driver has focus on
driver.close()

# Measuring code execution time
print("--- %s seconds ---" % (time.time() - startTime))
