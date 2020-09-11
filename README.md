# jvit-ws-data-crawler


# Install
- pip install scrapy


## CLI
- create project: $ scrapy startproject project1
- run spider: $ scrapy crawl <spider_name>
- export to csv: $ scrapy crawl <spider_name> -o result.csv
- realtest url: $ scrapy shell <url>
- 

## References
- get first item: extract_first(), get()
- get array list: getall(), extract()
- >>> response.css('li.next a').attrib['href']

## Debug 
- scrapy shell "http://quotes.toscrape.com/page/1/"
- try with selector: response.css('title')
- ...

## Css extractor
- text: .css('a::text').get() => <a>text</a>
- atribute href: .css('a::attr(href)').get() => <a href='http://example.url'>text</a>

## Document
- https://www.linode.com/docs/development/python/use-scrapy-to-extract-data-from-html-tags/



# Example Spiders
- quotes spider:
  scrapy crawl quotes -o quotes.json

- scrapy selenium sample: https://github.com/tristanlatr/charityvillage_jobs

