import scrapy
import json

class jobsSpider(scrapy.Spider):
  name = "jobs2"

  start_urls = ['https://itviec.com/it-jobs']

  def parse(self, response):
    # get all urls
    all_urls = response.css('.job .title a')
    yield from response.follow_all(all_urls, self.parse_job)

    #  crawl next page
    next_page_url = response.css('#show_more a')
    yield from response.follow_all(next_page_url, self.parse)

  
  # parse a job
  def parse_job(self, response):
    print('parse job:')
    # title = response.css('.job_title::text').get().strip()
    # address = response.css('.address__full-address span::text').get().strip()
    # tags = response.css('.tag-list a span::text').getall()
    # company_name = response.css('.inside h3.name a::text').get()


    data_in_string = response.css('script[type="application/ld+json"]::text').get().strip()
    data = json.loads(data_in_string)
    title = data['title']
    company_name = data['hiringOrganization']['name']
    company_description = data['hiringOrganization']['description']
    skills = data['skills']
    datePosted = data['datePosted']
    industry = data['industry']
    job_type = data['employmentType']
    addressArr = data['jobLocation'][0]['address']
    address = addressArr['streetAddress'] + ', ' + addressArr['addressLocality'] + ', ' + addressArr['addressRegion'] 

    # print(data)
    # print(dict(
    #   company_name=data['hiringOrganization']['name']
    # ))

    yield {
      'title': title,
      'job_type': job_type,
      # 'tags': tags,
      # 'salary': salary,
      'skills': skills,
      'company_name': company_name,
      'company_description': company_description,
      'address': address
    }


   
      


