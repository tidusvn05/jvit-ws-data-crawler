import scrapy
import logging


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            # 'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            # request to each url          
            yield scrapy.Request(url=url, callback=self.parse)

    # callback function
    def parse(self, response):
      logger = logging.getLogger()
      all_quotes = response.css('div.quote')
      for quote in all_quotes:
        text = quote.css('.text::text').get()
        author = quote.css('span .author::text').get()
        author_url = quote.css('span a::attr(href)').get()
        tags = quote.css("div.tags a.tag::text").getall()

        print(dict(text=text, author=author, author_url=author_url, tags=tags))
        yield {
          'text': text,
          'author': author,
          'tags': tags
        }

        # detect next page
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        
        # author_url = quote.xpath('//span/a/@href').get() # use xpath
        # logger.warning(quote.css('.text::text').get())
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page

        # # write to file
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)


