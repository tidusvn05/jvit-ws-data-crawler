import scrapy


class jobsSpider(scrapy.Spider):
  name = "jobs"

  start_urls = ['https://itviec.com/it-jobs']

  def parse(self, response):
    # 
    all_jobs = response.css('.job')
    
    for job in all_jobs:
      title = job.css('.title a::text').get()
      description = job.css('.description::text').get()

      print(dict(
        title=title,
        description=description
      ))
      yield {
        'title': title,
        'description': description,
      }


    # detect next page
    # next_page = response.css('#show_more a::attr(href)').get()
    # print('next_page: ', next_page)
    # if next_page is not None:
    #   yield response.follow(next_page, callback=self.parse)
      


