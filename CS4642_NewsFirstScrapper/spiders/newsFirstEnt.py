import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class NewsSpider(scrapy.Spider):

    name = "NewsENT"

    start_urls = [
        'https://www.newsfirst.lk/category/entertainment/'
    ]

    def parse(self, response):
        #from small colums
        for news in response.xpath('//div[@class="sub-1-news-block cat-bar-entertainment-full"]'):
                print "small"   
                item= CrawlerItem()
                item['link'] =news.css('a::attr(href)').extract_first() #link 
                item['title']=news.css('h2::text').extract_first(), #header
                item['date']=news.css('p::text').extract_first().strip('\n'), #date
                item['time']=news.css('abbr::text').extract_first(),  #time
                item['cat']="ENT"  #cat
                request=scrapy.Request( item['link'],callback=self.parse_next)
                request.meta['item']=item
                yield request  

        #from big colums
        for news in response.xpath('//div[@class="main-news-block cat-bar-entertainment-full"]'):
                print "big"   
                item= CrawlerItem()
                item['link'] =news.css('a::attr(href)').extract_first() #link 
                item['title']=news.css('h1::text').extract_first(), #header
                item['date']=news.css('p::text').extract_first().strip('\n'), #date
                item['time']=news.css('abbr::text').extract_first(),  #time
                item['cat']="ENT"  #cat
                request=scrapy.Request( item['link'],callback=self.parse_next)
                request.meta['item']=item
                yield request
        next_page = response.css('a[class*="next page-numbers"] ::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
   
    def parse_next(self,response):
        item = response.meta['item']
        para_o=unicode("")
        for para in response.xpath('//div[@class="text-left w-300 editor-styles"]//p'):
            if para.css('p::text').extract_first() is not None: 
              para_o+=para.css('p::text').extract_first()
        item['para'] = para_o
        yield item

class CrawlerItem(scrapy.Item):

    title = scrapy.Field()
    date = scrapy.Field(output_processor=MapCompose(unicode.strip))
    time = scrapy.Field()
    link = scrapy.Field()
    para = scrapy.Field()
    cat  = scrapy.Field()

    def set_all(self, value):
        for keys, _ in self.fields.items():
            self[keys] = value

# class MyItemLoader(ItemLoader):
#     default_output_processor = TakeFirst()

#     message_in = MapCompose(unicode, unicode.strip)
#     message_out = Join()