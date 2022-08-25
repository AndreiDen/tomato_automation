import re
import os

from playwright.sync_api import Page, expect
from pprint import pprint

class StepTwoDesktop:
    def __init__(self, page):
        self.page: Page = page
        self.order_details = OrderDetails(page)
        self.business_card = BusinessCardLayout(page)

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
        price = self.page.locator('//div[child::div[contains(@class, "template-info_readyAt")]]//span[contains(@class, "text_primary-big")]').inner_text()
        return int(price.strip(' руб'))


class BusinessCardLayout:
    def __init__(self, page):
        self.page: Page = page

    def upload_file(self, file):
        self.page.locator('//input').set_input_files([file])
        expect(self.page.locator("//span[contains(@class, 'template-preview_fileName')]")).to_be_visible()
        web_file_name = self.page.locator("//span[contains(@class, 'template-preview_fileName')]").inner_text()
        assert (web_file_name == os.path.basename(file))

    def remove_file(self):
        button_name = 'Удалить макет'
        self.page.locator(f"//button[text()='{button_name}']").click()
        expect(self.page.locator('text=Нажмите, чтобы загрузить макет или перетащите его сюда.')).to_be_visible()

    def get_front_page_image_url(self):
        source = self.page.locator("//div[contains(@class, 'template-preview_wrapper')]//img[contains(@class, 'template-preview_page')][1]").get_attribute('src')
        return source

    def get_back_page_image_url(self):
        source = self.page.locator("//div[contains(@class, 'template-preview_wrapper')]//img[contains(@class, 'template-preview_page')][2]").get_attribute('src')
        return source

    def get_page_quantity_verification_status(self):
        text = 'Количество страниц'
        return self._get_status_by_name(text)

    def get_file_format_verification_status(self):
        text = 'Формат'
        return self._get_status_by_name(text)

    def get_resolution_verification_status(self):
        text = 'Разрешение'
        return self._get_status_by_name(text)

    def get_images_present_verification_status(self):
        text = 'Изображения'
        return self._get_status_by_name(text)

    def get_overhang_verification_status(self):
        text = 'Вылеты 2mm'
        return self._get_status_by_name(text)

    def get_color_palette_verification_status(self):
        text = 'Цветовая палитра'
        return self._get_status_by_name(text)

    def get_fonts_verification_status(self):
        text = 'Шрифты'
        return self._get_status_by_name(text)

    def _get_status_by_name(self, text):
        object = self.page.locator(f'//div[contains(@class, "check-info") and descendant::span[text()="{text}"]]/img')
        status = object.get_attribute('src')
        return os.path.splitext(os.path.basename(status))[0].replace('check-', '')

