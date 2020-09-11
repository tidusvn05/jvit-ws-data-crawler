import scrapy
import logging
import json
from scrapy_selenium import SeleniumRequest

SCROLL_DOWN='window.scrollTo(0,document.body.scrollHeight);'


class NctSpider(scrapy.Spider):
  name="nct"

  start_urls = ['https://www.nhaccuatui.com/bai-hat/top-20.au-my.html']

  # def __init__(self):
  

  def start_requests(self):
    for url in self.start_urls:
      yield SeleniumRequest(url=url, callback=self.parse)

  def parse(self, response):
    self.log(">>>>> aa")
    title = response.css('.tile_box_key h1::text').get()
    ranking = response.css('.list_show_chart li')

    for rank_item in ranking:
      rank = rank_item.css('.chart_tw::text').get()
      title = rank_item.css('.box_info_field h3 a::text').get()
      singers = rank_item.css('.box_info_field .list_name_singer a::text').getall()

      print(dict(
        rank=rank,
        title=title,
        singers=", ".join(singers)
      ))