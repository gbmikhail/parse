import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo[t][0]=4']

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[@class='_1h3Zg _2rfUm _2hCDz _21a7u']/a/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        vac_name = response.xpath("//h1/text()").extract_first()
        vac_salary = response.xpath("//span[@class='_1h3Zg _2Wp8I _2rfUm _2hCDz']/text()").extract()
        vac_url = response.url
        yield JobparserItem(name=vac_name, salary=vac_salary, url=vac_url)
