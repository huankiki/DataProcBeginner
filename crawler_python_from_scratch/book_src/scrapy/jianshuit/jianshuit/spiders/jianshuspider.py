import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from jianshuit.items import JianshuitItem

class jianshuit(CrawlSpider):
    name = 'jianshu'
    start_urls = ['http://www.jianshu.com/c/V2CqjW?order_by=added_at&page=1']

    def parse(self, response):
        item = JianshuitItem()
        selector = Selector(response)
        infos = selector.xpath('//ul[@class="note-list"]/li')
        for info in infos:
            try:
                user = info.xpath('div/div[1]/div/a/text()').extract()[0]
                time = info.xpath('div/div[1]/div/span/@data-shared-at').extract()[0]
                title = info.xpath('div/a/text()').extract()[0]
                view = info.xpath('div/div[2]/a[1]/text()').extract()[1].strip()
                comment = info.xpath('div/div[2]/a[2]/text()').extract()[1].strip()
                like = info.xpath('div/div[2]/span/text()').extract()[0].strip()
                if info.xpath('div/div[2]/span[2]/i'):
                    gain = info.xpath('div/div[2]/span[2]/text()').extract()[0].strip()
                else:
                    gain = '0'

                item['user'] = user
                item['time'] = time
                item['title'] = title
                item['view'] = view
                item['comment'] = comment
                item['like'] = like
                item['gain'] = gain
                yield  item

            except IndexError:
                pass
        urls = ['http://www.jianshu.com/c/V2CqjW?order_by=added_at&page={}'.format(str(i)) for i in range(2, 101)]
        for url in urls:
            yield Request(url, callback=self.parse)