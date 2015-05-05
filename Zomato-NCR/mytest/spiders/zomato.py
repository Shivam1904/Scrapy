from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
 
from mytest.items import MytestItem
 
class ZomatoRest(CrawlSpider):
 
	name = "zomoatolist"
	allowed_domains = ["zomato.com"]
	start_urls = [
		"https://www.zomato.com/ncr/restaurants?page=%s"% page for page in xrange(1,349)
		]
	rules = (
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[contains(@class, "right res-right")]/ul[contains(@id, "pagination-control res-menu-paginator")]/li[contains(@id, "active")]/a')), callback='parse_listings', follow=True),
	)
 
	def parse_start_url(self, response): 
		return self.parse_listings(response)
 
	def parse_listings(self, response):
		sel = Selector(response)
		films = sel.xpath('//ol/li[contains(@class, "resZS mb5 pb5 bb even  status1")]')
		items = []
 		f = open('z.txt','a')
		for film in films:
			# Populate film fields
			item = MytestItem()
			item['rest'] = film.xpath('.//article[contains(@class, "search-result")]/div[contains(@class, "search_grid_left")]/div[contains(@class, "search-name")]/h3[contains(@class, "top-res-box-name")]/a/text()').extract()
			item['hlink'] = film.xpath('.//article[contains(@class, "search-result")]/div[contains(@class, "search_grid_left")]/div[contains(@class, "search-name")]/h3[contains(@class, "top-res-box-name")]/a/@href').extract()
			item = self.__normalise_item(item, response.url)
 			items.append(item)
		for i in range(0,len(items)):
		 	f.write(str(items[i]['rest'][0].encode('utf8'))+"	"+str(items[i]['hlink'][0].encode('utf8'))+"\n")
		print items
		return items
 
	def __normalise_item(self, item, base_url):
		'''
		Standardise and format item fields
		'''
 
		# Loop item fields to sanitise data and standardise data types
		# for key, value in vars(item).values()[0].iteritems():
		# 	item[key] = self.__normalise(item[key])
 
		# Clean year and convert year from string to float
		# item['year'] = item['year'].strip('()')
		# item['type'] = 'Movie'
 
		# if len(item['year']) > 4:
		# 	item['type'] = item['year'][5:]
		# 	item['year'] = item['year'][0:4]
		# item['year'] = self.__to_int(item['year'])
 
		# Convert rating from string to float
		# item['rating'] = self.__to_float(item['rating'])
 
		# Convert film URL from relative to absolute URL
		# item['film_url'] = self.__to_absolute_url(base_url, item['film_url'])
 
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
