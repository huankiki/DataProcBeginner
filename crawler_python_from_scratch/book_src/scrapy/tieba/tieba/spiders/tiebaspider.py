import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from tieba.items import TiebaItem

class tieba(CrawlSpider):
    name = 'tieba'
    start_urls = ['https://www.zhihu.com/topic/19552832/top-answers?page=1']

    def parse(self, response):
        item = TiebaItem()
        selector = Selector(response)
        infos = selector.xpath('//div[@class="zu-top-feed-list"]/div')
        for info in infos:
            try:
                question = info.xpath('div/div/h2/a/text()').extract()[0].strip()
                favour = info.xpath('div/div/div[1]/div[1]/a/text()').extract()[0]
                user = info.xpath('div/div/div[1]/div[3]/span/span[1]/a/text()').extract()[0]
                user_info = info.xpath('div/div/div[1]/div[3]/span/span[2]/text()').extract()[0].strip()
                content = info.xpath('div/div/div[1]/div[5]/div/text()').extract()[0].strip()

                item['question'] = question
                item['favour'] = favour
                item['user'] = user
                item['user_info'] = user_info
                item['content'] = content

                yield item
            except IndexError:
                pass

        urls = ['https://www.zhihu.com/topic/19552832/top-answers?page={}'.format(str(i)) for i in range(2,50)]
        for url in urls:
            yield Request(url,callback=self.parse)