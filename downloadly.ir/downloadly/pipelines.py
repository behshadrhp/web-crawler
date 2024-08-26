# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
from itemadapter import ItemAdapter

import pymongo

class MongoDownloadlyPipeline:
    collection_name = "best_course"
     
    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://root:bPil138APsssAVs0SAH@kingdoncl.a7law.mongodb.net/?retryWrites=true&w=majority&appName=KingDonCl")
        self.db = self.client["downloadly"]

    def close_spicer(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item
