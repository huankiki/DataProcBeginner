import requests
from lxml import etree
import re
import csv 


PAGE_NUM = 10

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

def get_category_url(url):
    '''
    行业类别，比如：人工智能、自然语言处理等
    '''
    html = requests.get(url,headers=headers)
    selector = etree.HTML(html.text)
    category_urls = selector.xpath('//div[@id="categs-nav"]/ul/li/a/@href')
    for category_url in category_urls:
        category = category_url.split("/")[-2]
        filename = "./" + category + ".csv"
        fp = open(filename,'wt',newline='',encoding='utf-8')
        writer = csv.writer(fp)
        writer.writerow(('title', 'type',  'company', 'city', 'time', 'url'))

        for i in range(1, PAGE_NUM+1):
            page_url = category_url + "?p=" + str(i)
            get_job_info(page_url, writer)
        fp.close()


def get_job_info(url, writer):
    '''
    全职 爱因互动招聘AI知识编辑及审核主管 爱因互动科技发展（北京）有限公司 北京 job_url
    包含： 职位类别 job_url job_title job_company job_city job_time
    只爬取日期较近的10页职位
    '''
    html = requests.get(url,headers=headers)
    selector = etree.HTML(html.text)
    job_rows = selector.xpath('//*[@id="job-listings"]/div[@class]')
    
    try:
        for job_row in job_rows:
            # time
            time = job_row.xpath('//span[@class="time-posted"]/text()')[0].strip()
            title = job_row.xpath('//span[@class="row-info"]/a/@title')[0].strip()
            job_url = job_row.xpath('//span[@class="row-info"]/a/@href')[0].strip()
            type = job_row.xpath('//span[@class="row-info"]/img/@alt')[0].strip()
            company_city = job_row.xpath('//span[@class="row-info"]')[0].xpath('string(.)').split("at")[-1].strip().split("in")
            if len(company_city) == 2:
                company = company_city[0].strip()
                city = company_city[1].strip()
            else:
                company_city = company_city[0].split(',')
                company = company_city[0].strip()
                city = company_city[1].strip()
            #print(title, type, company, city, time, job_url) 

            writer.writerow((title, type, company, city, time, job_url))
    
    except IndexError:
        pass


if __name__ == '__main__':
    url = 'http://www.nlpjob.com/jobs/'
    get_category_url(url)

