import sqlite3
from itemadapter import ItemAdapter


class SQLiteDownloadlyPipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('downloadly.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS downloadly (
                title TEXT,
                info TEXT,
                page_url TEXT
            )
        ''')

    def close_spider(self, spider):
        self.connection.commit()
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT INTO downloadly (title, info, page_url) VALUES (?, ?, ?)
        ''', (item['title'], item['info'], item['page url']))
        return item
