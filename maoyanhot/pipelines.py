# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import json
import codecs
import datetime

class TextPipeline(object):
    def __init__(self):
        self.score = 9

    def process_item(self, item, spider):
        if item['score']:
            if float(item['score']) <= float(self.score):
                item['score'] = '不好看'
            return item
        else:
            return DropItem('Missing Score')

class JsonPipeline(object):
    def __init__(self):
        print('======================== Openning file to write...')
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.file = codecs.open(timestamp + 'maoyan.json', 'wb', encoding = 'utf-8')

    def process_item(self, item, spider):
        print('======================== Writting ...')
        line = json.dumps(dict(item), ensure_ascii = False) + '\n'
        self.file.write(line)
        return item

    def close_spider(self, spider):
        print('======================== Write done, close file')
        self.file.close()
