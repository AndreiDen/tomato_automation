import time
import re
from playwright.sync_api import Page, expect, Browser, BrowserType, BrowserContext

from config import Config
import pages.order_page_step_1
from pages.page_one_options import OPTIONS
from pages.order_page_step_1 import StepOneDesktop


def test_run(page: Page, browser: Browser,browser_type: BrowserType):
    page.goto(f"{Config.ROOT_ADDRESS}/business-card")
    expect(page).to_have_title(re.compile("Calendar builder"))
    step_one = StepOneDesktop(page)
    step_one.print_type.set_print(print_type=OPTIONS.PRINT.DIGITAL)
    # step_one.print_type.set_print(print_type=OPTIONS.PRINT.OFFSET)
    # step_one.print_type.set_print(print_type=OPTIONS.PRINT.DIGITAL)
    # step_one.material_3d.set_meterial_3d()
    # step_one.material_3d.set_foil_and_varnish_side(OPTIONS.FOIL_SIDE.BOTH)
    # step_one.material_3d.set_foil_front(OPTIONS.FOIL_OPTIONS.RED)
    # step_one.material_3d.set_varnish_front(OPTIONS.VARNISH_FRONT.REQUIRED)
    # step_one.material_3d.set_varnish_back(OPTIONS.VARNISH_BACK.REQUIRED)

    # for option in [value for name, value in vars(OPTIONS.FOIL_OPTIONS).items() if name.isupper()]:
    #     step_one.material_3d.set_foil_front(option)
    #     time.sleep(1)
    print('\n')
    step_one.priceSelector.get_price_regular()
    step_one.priceSelector.get_price_urgent()
    step_one.priceSelector.get_ready_time_regular()
    step_one.priceSelector.get_ready_time_urgent()
    step_one.priceSelector.select_regular()

    time.sleep(2)


