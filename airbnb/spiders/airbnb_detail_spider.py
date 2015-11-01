from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from airbnb.items import AirbnbItem

class AirbnbDetailSpider(CrawlSpider):
    name = "meetupDetail"
    allowed_domains = ["meetup.com"]
    start_urls = ["http://www.meetup.com/Search-Meetup-Karlsruhe/"]
    rules = [Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@id="recentMeetups"]//a[@class="event-title"]')), callback='parse_meetup')]

    def parse_meetup(self, response):
        sel = Selector(response)
        item = AirbnbItem()
        item['title'] = sel.xpath('//h1[@itemprop="name"]/text()').extract()
        item['link'] = response.url
        item['description'] = sel.xpath('//div[@id="past-event-description-wrap"]//text()').extract()
        yield item
