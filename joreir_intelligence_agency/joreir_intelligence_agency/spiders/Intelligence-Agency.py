import scrapy

# link_articles =  response.xpath('//a[starts-with(@href,"collection") and (parent::h3|parent::h2)]/@href').getall()
# titles_articles =  response.xpath('//h1[@class="documentFirstHeading"]/text()').get()
# documents_articles = response.xpath('//div[@class="field-item even"]//p[not(@class)]/text()').get


class SpiderCIA(scrapy.Spider):
    name = 'cia'
    start_urls = [
        'https://www.cia.gov/library/readingroom/historical-collections'

    ]

    custom_settings = {
        'FEED_URI': 'cia.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):

        link_declassified = response.xpath(
            '//a[starts-with(@href,"collection") and (parent::h3|parent::h2)]/@href').getall()

        for link in link_declassified:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):

        link = kwargs['url']
        title = response.xpath(
            '//h1[@class="documentFirstHeading"]/text()').get()
        information = response.xpath(
            '//div[@class="field-item even"]//p[not(@class)]/text()').get()
        yield{
            'url': link,
            'title': title,
            'body': information

        }
