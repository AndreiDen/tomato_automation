import time
import re
from playwright.sync_api import Page, expect, Browser, BrowserType, BrowserContext
from pprint import pprint

from config import Config
from pages.page_one_options import OPTIONS
from pages.order_page_step_1 import StepOneDesktop
from pages.order_page_step_2 import StepTwoDesktop


PRINT_TYPE_OFFSET = OPTIONS.PRINT.DIGITAL
MATERIAL = OPTIONS.MATERIAL.MELOVAN


def test_digital_melovan_regular(page: Page, browser: Browser, browser_type: BrowserType):
    SIZE_85 = OPTIONS.SIZE.EIGHTY_FIVE
    FULL_COLOR_BOTH_SIDES = OPTIONS.FULL_COLOR_PRINT.TWO_SIDED
    ROUNDING_NEEDED = OPTIONS.ROUNDING.NEEDED
    QUANTITY_500 = OPTIONS.QUANTITY.Q500
    print('n')

    page.goto(f"{Config.ROOT_ADDRESS}/business-card")
    expect(page).to_have_title(re.compile("Calendar builder"))

    step_one = StepOneDesktop(page)
    step_one.print_type.set_print_type(print_type=PRINT_TYPE_OFFSET)

    step_one.material_melovan_offset.set_material_melovan()
    step_one.material_melovan_offset.set_size(SIZE_85)
    step_one.material_melovan_offset.set_full_color_sides(full_color_sides=FULL_COLOR_BOTH_SIDES)
    step_one.material_melovan_offset.set_rounding(rounding=ROUNDING_NEEDED)
    step_one.material_melovan_offset.set_quantity(QUANTITY_500)

    time.sleep(3)  # wait for price to update

    price_regular = step_one.priceSelector.get_price_first()
    price_urgent = step_one.priceSelector.get_price_second()
    ready_days_regular, ready_date_regular = step_one.priceSelector.get_ready_time_first()
    ready_days_urgent, ready_date_urgent = step_one.priceSelector.get_ready_time_second()

    assert (price_regular == 1973)
    assert (price_urgent == 3947)

    assert (ready_days_regular == '3')
    assert (ready_days_urgent == '1')

    assert (ready_date_regular == '30 августа')
    assert (ready_date_urgent == '26 августа')

    step_one.priceSelector.select_term_first()
    step_one.confirmation_popup.confirm()

    step_two = StepTwoDesktop(page)
    details_list = step_two.order_details.get_details_list()
    assert (PRINT_TYPE_OFFSET in details_list)
    assert (MATERIAL in details_list)
    assert (f'Размер визиток: {SIZE_85}' in details_list)
    assert ('Полноцветная печать с двух сторон' in details_list)
    assert (f'{QUANTITY_500} штук' in details_list)
    assert (f'Скругление углов: {ROUNDING_NEEDED}' in details_list)

    ready_day, ready_date = step_two.order_details.get_ready_date()
    assert (ready_day == 'вторник')
    assert (ready_date == ['30', 'августа'])

    price = step_two.order_details.get_price()
    assert (price == 1973)

def test_digital_melovan_urgent(page: Page, browser: Browser, browser_type: BrowserType):
    SIZE_85 = OPTIONS.SIZE.EIGHTY_FIVE
    FULL_COLOR_BOTH_SIDES = OPTIONS.FULL_COLOR_PRINT.TWO_SIDED
    ROUNDING_NEEDED = OPTIONS.ROUNDING.NEEDED
    QUANTITY_500 = OPTIONS.QUANTITY.Q500
    print('n')

    page.goto(f"{Config.ROOT_ADDRESS}/business-card")
    expect(page).to_have_title(re.compile("Calendar builder"))

    step_one = StepOneDesktop(page)
    step_one.print_type.set_print_type(print_type=PRINT_TYPE_OFFSET)

    step_one.material_melovan_offset.set_material_melovan()
    step_one.material_melovan_offset.set_size(SIZE_85)
    step_one.material_melovan_offset.set_full_color_sides(full_color_sides=FULL_COLOR_BOTH_SIDES)
    step_one.material_melovan_offset.set_rounding(rounding=ROUNDING_NEEDED)
    step_one.material_melovan_offset.set_quantity(QUANTITY_500)

    time.sleep(3)  # wait for price to update

    price_regular = step_one.priceSelector.get_price_first()
    price_urgent = step_one.priceSelector.get_price_second()
    ready_days_regular, ready_date_regular = step_one.priceSelector.get_ready_time_first()
    ready_days_urgent, ready_date_urgent = step_one.priceSelector.get_ready_time_second()

    assert (price_regular == 1973)
    assert (price_urgent == 3947)

    assert (ready_days_regular == '3')
    assert (ready_days_urgent == '1')

    assert (ready_date_regular == '30 августа')
    assert (ready_date_urgent == '26 августа')

    step_one.priceSelector.select_term_second()
    step_one.confirmation_popup.confirm()

    step_two = StepTwoDesktop(page)
    details_list = step_two.order_details.get_details_list()
    assert (PRINT_TYPE_OFFSET in details_list)
    assert (MATERIAL in details_list)
    assert (f'Размер визиток: {SIZE_85}' in details_list)
    assert ('Полноцветная печать с двух сторон' in details_list)
    assert (f'{QUANTITY_500} штук' in details_list)
    assert (f'Скругление углов: {ROUNDING_NEEDED}' in details_list)

    ready_day, ready_date = step_two.order_details.get_ready_date()
    assert (ready_day == 'пятница')
    assert (ready_date == ['26', 'августа'])

    price = step_two.order_details.get_price()
    assert (price == 3947)
