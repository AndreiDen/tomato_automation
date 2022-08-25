import time
import re
import pytest
from playwright.sync_api import Page, expect, Browser, BrowserType, BrowserContext
from pprint import pprint

from config import Config
from pages.page_one_options import OPTIONS
from pages.order_page_step_1 import StepOneDesktop
from pages.order_page_step_2 import StepTwoDesktop

@pytest.mark.skip(reason="temporary test")
def test_run(page: Page, browser: Browser, browser_type: BrowserType):
    print('n')
    PRINT_TYPE = OPTIONS.PRINT.DIGITAL
    SIZE = OPTIONS.SIZE.EIGHTY_FIVE
    FOIL_SIDE = OPTIONS.FOIL_SIDE.BOTH
    FOIL_COLOR_FRONT = OPTIONS.FOIL_OPTIONS.RED
    VARNISH_FRONT_REQUIRED = OPTIONS.VARNISH_FRONT.REQUIRED
    VARNISH_BACK_REQUIRED = OPTIONS.VARNISH_BACK.REQUIRED
    QUANTITY = OPTIONS.QUANTITY.Q300

    pprint([PRINT_TYPE, SIZE, FOIL_SIDE, FOIL_COLOR_FRONT, VARNISH_FRONT_REQUIRED, VARNISH_BACK_REQUIRED])

    page.goto(f"{Config.ROOT_ADDRESS}/business-card")
    expect(page).to_have_title(re.compile("Calendar builder"))
    step_one = StepOneDesktop(page)
    step_one.print_type.set_print_type(print_type=PRINT_TYPE)
    step_one.material_3d.set_meterial_3d()
    step_one.material_3d.set_size(SIZE)
    step_one.material_3d.set_foil_and_varnish_side(FOIL_SIDE)
    step_one.material_3d.set_foil_front(FOIL_COLOR_FRONT)
    step_one.material_3d.set_varnish_front(VARNISH_FRONT_REQUIRED)
    step_one.material_3d.set_varnish_back(VARNISH_BACK_REQUIRED)
    step_one.material_3d.set_quantity(QUANTITY)

    print('\n')
    # step_one.priceSelector.get_price_regular()
    # step_one.priceSelector.get_price_urgent()
    # step_one.priceSelector.get_ready_time_regular()
    # step_one.priceSelector.get_ready_time_urgent()
    step_one.priceSelector.select_term_first()
    step_one.confirmation_popup.confirm()

    step_two = StepTwoDesktop(page)
    details_list = step_two.order_details.get_details_list()
    pprint(details_list)
    ready_date = step_two.order_details.get_ready_date()
    pprint(ready_date)
    time.sleep(2)


