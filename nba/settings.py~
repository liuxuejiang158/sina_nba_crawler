# -*- coding: utf-8 -*-

# Scrapy settings for nba project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'nba'

SPIDER_MODULES = ['nba.spiders']
NEWSPIDER_MODULE = 'nba.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nba (+http://www.yourdomain.com)'
ITEM_PIPELINES = {
    'scrapy_mongodb.MongoDBPipeline': 300,
}

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'nba'

LOG_FILE = 'scrapy.log'
LOG_LEVEL = 'INFO'
DOWNLOAD_DELAY = 0
MEMUSAGE_LIMIT_MB = 0

# FEED_URI = "file:///home/shellbye/scrapy.json"
# FEED_FORMAT = "json"
# did not work exceptions.AttributeError: 'dict' object has no attribute 'fields'

COOKIES_ENABLES = False


