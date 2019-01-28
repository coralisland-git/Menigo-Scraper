# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ChainItem(Item):

    Product_Name = Field()

    Supplier_Name = Field()

    Article_Number = Field()

    Supplier_Article_Number = Field()

    Category = Field()

    Volumn = Field()

    Alcohol_Percent = Field()

    Country = Field()

    Year = Field()

    Producer = Field()

    Region = Field()

    EAN_GTIN = Field()

    Package = Field()
