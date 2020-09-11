import scrapy
import logging
import json


class JobsSpider(scrapy.Spider):
  name="itviec"

  start_urls = ['https://itviec.com/it-jobs']

  def parse(self, response):
    job_links = response.css('.job .title a')
    yield from response.follow_all(job_links, self.parse_job)

    # check next page and crawl again
    # next_page_urls = response.css('#show_more a.more-jobs-link')
    # yield from response.follow_all(next_page_urls, self.parse)

  # parse jobs links
  def parse_job(self, response):
    self.log("aaaa")
    title = response.css('.job_info .job_title::text').get().strip()
    tags = response.css('.job_info .tag-list a span::text').getall()
    tags = [item.strip() for item in tags]
    # salary = response.css('.salary .salary-text::text').get().strip()
    # data = self.parse_data_from_data_string(response)

    data_in_string = response.css('script[type="application/ld+json"]::text').get().strip()
    data = json.loads(data_in_string)
    company_name = data['hiringOrganization']['name']
    company_description = data['hiringOrganization']['description']
    skills = data['skills']
    datePosted = data['datePosted']
    industry = data['industry']
    job_type = data['employmentType']
    addressArr = data['jobLocation'][0]['address']
    address = addressArr['streetAddress'] + ', ' + addressArr['addressLocality'] + ', ' + addressArr['addressRegion'] 

    print(data)
    print(dict(
      company_name=data['hiringOrganization']['name']
    ))


    print( dict(title=title, tags=tags) )
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

  
  # def parse_data_from_data_string(response):
  #   data_in_string = response.css('script[type="application/ld+json"]::text').get().strip()

  #   data = json.loads(data_in_string)

  #   print(data)
  #   print(dict(
  #     company_name=data.hiringOrganization.name 
  #   ))

  #   return data

