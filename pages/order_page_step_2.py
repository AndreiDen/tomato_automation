import re

from playwright.sync_api import Page
from pprint import pprint

class StepTwoDesktop:
    def __init__(self, page):
        self.page: Page = page
        self.order_details = OrderDetails(page)


class OrderDetails:
    def __init__(self, page):
        self.page: Page = page

    def get_details_list(self):
        ul_list = self.page.locator("//ul[starts-with(@class, 'template-info_businessCardInfo')]/li")
        details_list = ul_list.all_text_contents()
        return details_list

    def get_ready_date(self):
        date_element = self.page.locator("//div[starts-with(@class, 'template-info_readyAt')]")
        text_date = date_element.text_content()
        day_name, date = re.search("(?<=Будет готово: )(\w+)(.*)", text_date).groups()
        date = date.split()
        return day_name, date

    def get_price(self):
        pass