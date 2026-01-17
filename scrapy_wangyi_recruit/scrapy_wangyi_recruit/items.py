# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyWangyiRecruitItem(scrapy.Item):
    name = scrapy.Field() # 职位名称
    ed_background = scrapy.Field() # 学历要求
    workplace = scrapy.Field()  #工作地点
    job_description = scrapy.Field() # 职位描述
    job_requirement = scrapy.Field() # 任职要求


    pass
