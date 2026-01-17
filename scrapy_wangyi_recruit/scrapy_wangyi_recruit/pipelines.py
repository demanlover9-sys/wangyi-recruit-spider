# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


class ScrapyWangyiRecruitPipeline:
    def open_spider(self, spider):
        if spider.name == 'recruit_post':
            self.jobs = []
            self.f = open(f'{spider.name}.csv', 'w',encoding='utf-8-sig',newline='')
            # 表头信息
            header = ['职位名称','工作地点','学历要求','职位描述','任职要求']
            self.writer = csv.DictWriter(self.f,fieldnames=header)
            # 不要写在process_item写表头,否则表头会重复写入
            self.writer.writeheader()


    def process_item(self, item, spider):
        if spider.name == 'recruit_post':
            # 这里用Scrapy 官方推荐的工具，能安全地从 Item 对象中取字段（即使字段不存在也不会报错）。
            adapter = ItemAdapter(item)
                # name = scrapy.Field()  # 职位名称
                # ed_background = scrapy.Field()  # 学历
                # workplace = scrapy.Field()  # 工作地点
                # job_description = scrapy.Field()  # 职位描述
                # job_requirement = scrapy.Field()  # 任职要求
            dic = {
                '职位名称': adapter.get('name', '未知').strip(),
                '工作地点': adapter.get('workplace', '不限').strip(),
                '学历要求': adapter.get('ed_background', '不限').strip(),
                '职位描述': adapter.get('job_description', '').replace('\n', ' ').replace('\r', ' ').strip(),
                '任职要求': adapter.get('job_requirement', '').replace('\n', ' ').replace('\r', ' ').strip(),
            }
            self.jobs.append(dic)
            self.writer.writerow(dic)


        return item

    def close_spider(self, spider):
        if spider.name == 'recruit_post':
            print(f'爬取结束，共获取{len(self.jobs)}条职位数据')
            self.f.close()
