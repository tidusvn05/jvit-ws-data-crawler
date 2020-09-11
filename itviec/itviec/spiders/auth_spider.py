import scrapy
import logging
import json


def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    
    pass


class AuthSpider(scrapy.Spider):
  name="auth"

  start_urls = ['https://itviec.com/sign_in']
  job_list_url = 'https://itviec.com/it-jobs'

  def parse(self, response):
    # print('joblist: %s', self.job_list_url)
    # return
    return scrapy.FormRequest.from_response(
        response,
        formdata={'user[email]': 'tidusvn05@gmail.com', 'user[password]': 'omTK3OEZbDfIwonA7IwzDS4J'},
        callback=self.after_login
    )

  def after_login(self, response):
    # self.log("authentication_failed")
    self.log(response)
    # if authentication_failed(response):
    #   self.logger.error("Login failed")
    #   return

    # continue scraping with authenticated session...
    job_list_url = 'https://itviec.com/it-jobs'
    yield scrapy.Request(self.job_list_url, callback = self.parse_job_list)

  def parse_job_list(self, response):
    job_links = response.css('.job .title a')
   
    self.log(job_links)
    
    # crawl & parse all urls
    yield from response.follow_all(job_links, self.parse_job)

    # check next page
    next_page_urls = response.css('#show_more a.more-jobs-link')
    yield from response.follow_all(next_page_urls, self.parse_job_list)


  def parse_job(self, response):
    self.log("aaaa")
    title = response.css('.job_info .job_title::text').get().strip()
    salary = response.css('.salary .salary-text::text').get().strip()
    address = response.css('.address__full-address span::text').get().strip()

    tags = response.css('.job_info .tag-list a span::text').getall()
    tags = [item.strip() for item in tags]

    # data = self.parse_data_from_data_string(response)
    # print( dict(title=title, tags=tags) )
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


    yield {
      'title': title,
      'job_type': job_type,
      # 'tags': tags,
      'salary': salary,
      'skills': skills,
      'address': address,
      'company_name': company_name,
      'company_description': company_description,
      
    }


  # def parse_data_from_data_string(response):
  #   data_in_string = response.css('script[type="application/ld+json"]::text').get().strip()

  #   data = json.loads(data_in_string)

  #   print(data)
  #   print(dict(company_name=data.hiringOrganization.name ))