from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy import Request

from airbnb.items import AirbnbItem


class AirbnbSpider(BaseSpider):
    name = "airbnb"
    allowed_domains = ["airbnb.com.sg"]
    start_urls = [
        "https://www.airbnb.com.sg/s/Singapore"
    ]

    def parse(self, response):
        def clean_the_shit(shit):
            return max(shit.splitlines()).strip()

        responseSelector = Selector(response)
        listing_item = responseSelector.css('div.col-sm-12.row-space-2.col-md-6').css('div.listing')
        items_top = listing_item.css('div.panel-image.listing-img').css('div.listing-description')
        items_bottom = listing_item.css('div.panel-body.panel-card-section').css('div.media')
        items_image = listing_item.css('div.panel-image.listing-img')
        for bottom, top, image in zip(items_bottom, items_top, items_image):
            item = AirbnbItem()
            item['name'] = bottom.css('a').css('h3::text').extract()[0].strip()
            if item['name'] == '\u661f\u7ea7\u6c11\u5bbf \u8212\u9002\u5e72\u51c0  \u4ea4\u901a\u65b9\u4fbf':
                import ipdb; ipdb.set_trace()
            item['user_url'], item['room_url'] = bottom.xpath('a/@href').extract()
            type_and_reviews = bottom.css('div.text-muted.listing-location.text-truncate').css('a::text').extract()
            item['room_type'] = clean_the_shit(type_and_reviews[0])
            if len(type_and_reviews) == 2:
                item['reviews'] = clean_the_shit(type_and_reviews[1])[2:]
            item['summary'] = top.css('div.summary').css('p::text').extract()[0].strip()
            item['address'] = top.css('p.address').css('p::text').extract()[0]
            item['image'] = image.css('a.media-photo.media-cover').css('img').xpath('@src').extract()[0]
            # TODO: add cookie to get consistent prices
            item['price'] = int(image.css('a.link-reset.panel-overlay-bottom-left.panel-overlay-label.panel-overlay-listing-label').css('div').css('span.h3.text-contrast.price-amount::text').extract()[0])
            item['coin'] = ''.join(image.css('a.link-reset.panel-overlay-bottom-left.panel-overlay-label.panel-overlay-listing-label').css('div').css('sup.h6.text-contrast::text').extract())
            yield item

            # pagination
            next_page = responseSelector.xpath('//li[contains(@class, "next_page")]').xpath('a/@href')
            if next_page:
                url = response.urljoin(next_page[0].extract())
                yield Request(url, self.parse)
