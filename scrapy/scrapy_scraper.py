# -*- coding: utf-8 -*-
import scrapy

#creating class to store scraped data
class Cats(scrapy.Item):
    name = scrapy.Field()
    lifespan = scrapy.Field()
    weight = scrapy.Field()
    history        = scrapy.Field()
    behavior       = scrapy.Field()
    look       = scrapy.Field()
    grooming = scrapy.Field()
    nutritrional_needs = scrapy.Field()
    fun_facts = scrapy.Field()

    lap_cat = scrapy.Field()
    intelligence = scrapy.Field()
    ease_of_training = scrapy.Field()
    grooming_requirements = scrapy.Field()
    shedding = scrapy.Field()
    good_with_children = scrapy.Field()
    good_with_dogs = scrapy.Field()
    chattiness = scrapy.Field()

#main class  function to scrape data
class LinksSpider(scrapy.Spider):
    #name of the scraper
    name = 'cats'
    allowed_domains = ['https://vcahospitals.com']
    #setting starting url
    start_urls = ['https://vcahospitals.com/know-your-pet/cat-breeds']
    #setting base url
    BASE_URL = 'https://vcahospitals.com'

    #function that crawl through links
    def parse(self, response):
        links = response.xpath('//div[@class="content-wrapper callout-list-wrapper"]//a//@href').getall()
        for link in links:
            absolute_url = self.BASE_URL + link
            #calling parse_attr function to scrape data
            yield scrapy.Request(absolute_url, callback=self.parse_attr, dont_filter=True)

    #function that scrape data of supplied cat url
    def parse_attr(self, response):
        #calling Cats class to store data
        p = Cats()

        #creating xpaths of text data
        name_xpath = '//*[@id="Main"]/article/div/header/h1/text()'
        lifespan_xpath = '//p[@class="life-span"]/strong/text()'
        weight_xpath = '//p[@class="weight"]/strong/text()'
        history_xpath        = '//div[@class="rich-text-panel"]/ul[1]//li//text()'
        behavior_xpath       = '//div[@class="rich-text-panel"]/ul[2]//li//text()'
        look_xpath       = '//div[@class="rich-text-panel"]/ul[3]//li//text()'
        grooming_xpath = '//div[@class="rich-text-panel"]/ul[4]//li//text()'
        if response.xpath('//div[@class="rich-text-panel"]/ul[6]//li//text()').getall()==[]:
            nutritrional_needs_xpath = '//div[@class="rich-text-panel"]/p//text()'
            fun_facts_xpath = '//div[@class="rich-text-panel"]/ul[5]//li//text()'
        else:
            nutritrional_needs_xpath = '//div[@class="rich-text-panel"]/ul[5]//li//text()'
            fun_facts_xpath = '//div[@class="rich-text-panel"]/ul[6]//li//text()'

        #storing text data in cleaned way
        history_text = ' '.join(response.xpath(history_xpath).getall())
        behavior_text = ' '.join(response.xpath(behavior_xpath).getall())
        look_text = ' '.join(response.xpath(look_xpath).getall())
        grooming_text = ' '.join(response.xpath(grooming_xpath).getall())
        nutritrional_needs_text = ' '.join(response.xpath(nutritrional_needs_xpath).getall())
        fun_facts_text = ' '.join(response.xpath(fun_facts_xpath).getall())
        name = response.xpath(name_xpath).get()
        lifespan = response.xpath(lifespan_xpath).get()
        weight = response.xpath(weight_xpath).get()

        #scraping traits data
        traits = response.xpath('//div[@class="traits-container"]/ul/li')
        #looping through traits to count how many
        traits = [len(element.xpath('ul/li[@class="active"]')) for element in traits]

        #dumping lit of traits to specific columns
        p['lap_cat'], p['intelligence'], p['ease_of_training'], p['grooming_requirements'], p['shedding'], \
        p['good_with_children'], p['good_with_dogs'], p['chattiness'] = traits

        #saving all the text data to Cats class
        p['name'] = name
        p['lifespan'] = lifespan
        p['weight'] = weight
        p['history']        = '"' + history_text + '"'
        p['behavior']       = '"' + behavior_text + '"'
        p['look']       = '"' + look_text + '"'
        p['grooming'] = '"' + grooming_text+ '"'
        p['nutritrional_needs'] = '"' + nutritrional_needs_text + '"'
        p['fun_facts'] = '"' + fun_facts_text + '"'

        #yielding to csv
        yield p