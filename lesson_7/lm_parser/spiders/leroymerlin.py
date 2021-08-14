import scrapy
from scrapy.http import HtmlResponse
from lm_parser.items import LeroymerlinParserItem
from scrapy.loader import ItemLoader


class LmSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(LmSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}&fromRegion=505']

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='bex6mjh_plp b1f5t594_plp iypgduq_plp nf842wf_plp']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        feature = {}
        # Характеристики
        dl_feature = response.xpath("//dl[@class='def-list']/div")
        for item in dl_feature:
            title = item.xpath("./dt/text()").extract_first()
            value = item.xpath("./dd/text()").extract_first()
            feature[title] = value.replace('\n', '').strip()  # Очень руки чесались сделать replace именно тут

        loader = ItemLoader(item=LeroymerlinParserItem(), response=response)
        loader.add_xpath("name", "//h1/text()")
        loader.add_xpath("price", "//span[@slot='price']/text()")
        loader.add_xpath("photos", "//picture[@slot='pictures']/source/@data-origin")
        loader.add_value("feature", feature)
        loader.add_value("url", response.url)

        yield loader.load_item()
        # name = response.xpath("//h1/span/text()").extract_first()
        # photos = response.xpath("//div[@class='gallery-img-frame js-gallery-img-frame']/@data-url").extract()
        # yield AvitoparserItem(name=name, photos=photos)
