import time
import re
import os
import requests
import mimetypes
from pprint import pprint
from playwright.sync_api import Page, expect, Browser, BrowserType, BrowserContext

from config import Config
from definitions import TEST_FILES
from pages.page_one_options import OPTIONS
from pages.order_page_step_1 import StepOneDesktop
from pages.order_page_step_2 import StepTwoDesktop


PRINT_TYPE_OFFSET = OPTIONS.PRINT.OFFSET
MATERIAL = OPTIONS.MATERIAL.MELOVAN


def test_layout_90_valid_vertical(page: Page, browser: Browser, browser_type: BrowserType):
    SIZE_90 = OPTIONS.SIZE.NINETY
    FULL_COLOR_BOTH_SIDES = OPTIONS.FULL_COLOR_PRINT.TWO_SIDED
    print('n')

    page.goto(f"{Config.ROOT_ADDRESS}/business-card")
    expect(page).to_have_title(re.compile("Calendar builder"))

    step_one = StepOneDesktop(page)
    step_one.print_type.set_print_type(print_type=PRINT_TYPE_OFFSET)
    step_one.material_melovan_offset.set_material_melovan()
    step_one.material_melovan_offset.set_full_color_sides(full_color_sides=FULL_COLOR_BOTH_SIDES)
    step_one.material_melovan_offset.set_size(SIZE_90)
    step_one.priceSelector.select_term_first()
    step_one.confirmation_popup.confirm()

    step_two = StepTwoDesktop(page)
    step_two.business_card.upload_file(os.path.join(TEST_FILES, 'valid', '90х50 вертикальная верная.pdf'))

    front_page_image_link = step_two.business_card.get_front_page_image_url()
    response = requests.get(front_page_image_link)
    content_type = response.headers['content-type']
    extension = mimetypes.guess_extension(content_type)
    file_size = response.headers.get('Content-Length')

    assert (response.status_code == 200)
    assert (extension == '.png')
    assert (file_size == '56070')

    back_page_image_link = step_two.business_card.get_back_page_image_url()
    response = requests.get(back_page_image_link)
    content_type = response.headers['content-type']
    extension = mimetypes.guess_extension(content_type)
    file_size = response.headers.get('Content-Length')

    assert (response.status_code == 200)
    assert (extension == '.png')
    assert (file_size == '4270')

    assert ('success' == step_two.business_card.get_page_quantity_verification_status())
    assert ('success' == step_two.business_card.get_file_format_verification_status())
    assert ('success' == step_two.business_card.get_resolution_verification_status())
    assert ('success' == step_two.business_card.get_images_present_verification_status())
    assert ('success' == step_two.business_card.get_overhang_verification_status())
    assert ('success' == step_two.business_card.get_color_palette_verification_status())
    assert ('success' == step_two.business_card.get_fonts_verification_status())

    step_two.business_card.remove_file()