import sys
import json
import scrapy
from scrapy_wangyi_recruit.items import ScrapyWangyiRecruitItem


class RecruitPostSpider(scrapy.Spider):
    name = "recruit_post"
    allowed_domains = ["hr.163.com"]
    max_page = int(input('请输入最后一页：'))

    # 向列表页发送请求
    def start_requests(self):
        list_url = "https://hr.163.com/api/hr163/position/queryPage"
        # 这里直接用循环翻页了，不用注释的那个递归翻页方法了
        for page in range(1,self.max_page+1):
            data = {
                'currentPage':str(page),
                'pageSize':'10',
                'workType':'1'
            }
            yield  scrapy.Request(url=list_url,
                                  method='POST',
                                  # 如需必要，UA可以用UA池，导入random模块
                                  headers={
                                      'Content-Type': 'application/json;charset=UTF-8',
                                      'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
                                      'Referer':'https://hr.163.com/job-list.html?workType=1',
                                      'origin':'https://hr.163.com'
                                  },
                                  callback=self.parse,
                                  body=json.dumps(data),
                                  meta={'list_url':list_url,
                                        'data':data,})
    # 解析职位列表页的数据
    def parse(self, response):
        try:
            print('列表页数据解析中',response.url)
            content = response.json()
            # print(content)

            # 检查接口是否正常
            if content.get('code') != 200:
                msg = content.get('msg', '未知错误')
                print(f"接口返回异常 → code: {content.get('code')}, msg: {msg}, url: {response.url}")
                return

            # 获列表页数据
            job_list = content['data']['list']
            for work in job_list:
                job_id = work['id']
                job_name = work['name']
                ed_background = work['reqEducationName']
                place = work['workPlaceNameList'][0]
                detail_url = f'https://hr.163.com/api/hr163/position/query?id={job_id}'
                # 获得id之后拼接好url,向新的url发送接口请求，注意此时详情页的接口是get请求
                yield scrapy.Request(url=detail_url,
                                         callback=self.parse_detail,
                                         meta={'job_name':job_name, #meta可以传多个参数
                                               'ed_background':ed_background,
                                               'place':place,
                                               })
        except Exception as e:
            print('列表页数据获取失败，请检查',e)

        # self.page += 1
        # if self.page <= self.max_page:
        #     # https://hr.163.com/job-detail.html?id=73015&lang=zh
        #     # https://hr.163.com/job-detail.html?id=52693&lang=zh
        #     # https://hr.163.com/job-detail.html?id={id}&lang=zh
        #     lists_url = response.meta['list_url']
        #     data2 = response.meta['data']
        #     yield scrapy.FormRequest(url=lists_url,
        #                              callback=self.parse,
        #                              formdata=data2,
        #                              meta={'page':self.page}
        #                              )

    # 解析职位详情页数据
    def parse_detail(self,response):
        try:
            print('详情页解析中...',response.url)
            content = response.json()

            # 检查接口是否正常
            if content.get('code') != 200:
                msg = content.get('msg', '未知错误')
                print(f"接口返回异常 → code: {content.get('code')}, msg: {msg}, url: {response.url}")
                return

            # 获取详情页具体数据
            job_description = content['data']['description']
            job_requirement = content['data']['requirement']
            job_name = response.meta['job_name']
            place = response.meta['place']
            ed_background = response.meta['ed_background']
            # print(f'职位名称：{job_name},工作地点：{place},学历要求：{ed_background},职位描述:{job_description}，职位要求：{job_requirement}')
            job = ScrapyWangyiRecruitItem(name=job_name,
                                          ed_background=ed_background,
                                          workplace=place,
                                          job_description=job_description,
                                          job_requirement=job_requirement)
            yield job
        except Exception as e:
            print("详情页获取数据失败，请检查",e)






