from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from mytest.items import MytestItem
 
class IMDbNextPageSpider(CrawlSpider):
 
	name = "imdbn"
	allowed_domains = ["imdb.com"]
	start_urls = [
		"http://www.imdb.com/search/title?groups=top_1000&sort=user_rating&start=1&view=simple"
		]
	rules = (
		# Extract links for next pages
		# Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//div[contains(@class, "leftright")[1]//a[contains(., "Next")]')), callback='parse_listings', follow=True),
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[contains(@class, "leftright")]/div[contains(@id, "right")]/span/a')), callback='parse_listings', follow=True),
	)
 
	def parse_start_url(self, response): 
		return self.parse_listings(response)
 
	def parse_listings(self, response):
		sel = Selector(response)
		films = sel.xpath('//table[contains(@class, "results")]//tr[contains(@class, "even") or contains(@class, "odd")]')
		items = []
 		f = open('hsi.txt','a')
		for film in films:
			# Populate film fields
			item = MytestItem()
			item['title'] = film.xpath('.//td[contains(@class, "title")]/a/text()').extract()
			item['rating'] = film.xpath('.//td/b/text()').extract()
			item = self.__normalise_item(item, response.url)
 			items.append(item)
		for i in range(0,len(items)):
		 	f.write(str(items[i]['rating'])+"	"+str(items[i]['title'].encode('utf8'))+"\n")
		print type(items)
		return items
 
	def __normalise_item(self, item, base_url):
		'''
		Standardise and format item fields
		'''
 
		# Loop item fields to sanitise data and standardise data types
		for key, value in vars(item).values()[0].iteritems():
			item[key] = self.__normalise(item[key])
 
		# Convert rating from string to float
		item['rating'] = self.__to_float(item['rating'])

		return item
 
	def __normalise(self, value):
		# Convert list to string
		value = value if type(value) is not list else ' '.join(value)
		# Trim leading and trailing special characters (Whitespaces, newlines, spaces, tabs, carriage returns)
		value = value.strip()
 
		return value
 
	def __to_absolute_url(self, base_url, link):
		'''
		Convert relative URL to absolute URL
		'''
 
		import urlparse
 
		link = urlparse.urljoin(base_url, link)
 
		return link
 
	def __to_int(self, value):
		'''
		Convert value to integer type
		'''
 
		try:
			value = int(value)
		except ValueError:
			value = 0
 
		return value
 
	def __to_float(self, value):
		'''
		Convert value to float type
		'''
 
		try:
			value = float(value)
		except ValueError:
			value = 0.0
 
		return value