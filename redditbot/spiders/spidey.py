import scrapy


class QuotesSpider(scrapy.Spider):
    name = "redditbot"
    start_urls = [
        'https://www.reddit.com/r/politics/?count=25&after=t3_7ax8lb',
    ]

    def parse(self, response):

        titles = response.css('.title.may-blank::text').extract()
        votes = response.css('.score.unvoted::text').extract()
        times = response.css('time::attr(title)').extract()
        comments = response.css('.comments::text').extract()

        for item in zip(titles,votes,times,comments):
        #create a dictionary to store the scraped info
            scraped_info = {
               'title' : item[0],
               'vote' : item[1],
               'created_at' : item[2],
               'comments' : item[3],
            }

            #yield or give the scraped info to scrapy
            yield scraped_info

        next_page = response.css('span.next-button a::attr(href)').extract()
        #next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page[0], callback=self.parse)