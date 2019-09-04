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
        self.file = codecs.open(timestamp + 'maoyan.csv', 'wb', encoding = 'utf-8')

    def process_item(self, item, spider):
        print('======================== Writting ...')
        line = json.dumps(dict(item), ensure_ascii = False) + '\n'
        self.file.write(line)
        return item

    def close_spider(self, spider):
        print('======================== Write done, close file')
        self.file.close()

class MysqlPipeline(object):
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod    
    def from_crawler(cls, crawler):
        return cls(
            host = crawler.settings.get('MYSQL_HOST'),
            database = crawler.settings.get('MYSQL_DATABASE'),
            user = crawler.settings.get('MYSQL_USER'),
            password = crawler.settings.get('MYSQL_PASSWORD'),
            port = crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.database, self.user, self.password, self.port, charset='utf-8')
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s']*len(data))
        sql = 'insert into %s (%s) values (%s)'%(item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item        
