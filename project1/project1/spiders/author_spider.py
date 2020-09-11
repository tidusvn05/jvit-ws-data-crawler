import scrapy
import logging


class AuthorSpider(scrapy.Spider):
  name="author"

  start_urls = ['http://quotes.toscrape.com/']

  def parse(self, response):
    logger = logging.getLogger()
    all_author_links = response.css('.quote .author +  a')
    yield from response.follow_all(all_author_links, self.parse_author)
    
    next_page_url = response.css('li.next a')
    # yield from response.follow(next_page_url, self.parse)    
    yield from response.follow_all(next_page_url, self.parse)    


  # parse author links
  def parse_author(self, response):
    fullname = response.css('.author-title::text').get().strip()
    birthdate = response.css('.author-born-date::text').get().strip()
    hometown = response.css('.author-born-location::text').get().replace('in ', '').strip()
    description = response.css('.author-description::text').get().strip()

    print(dict(fullname=fullname, birthdate=birthdate, hometown=hometown, description=description ))
    yield {
      'fullname': fullname,
      'birthdate': birthdate,
      'hometown': hometown,
      'description': description,
    }