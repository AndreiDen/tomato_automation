from pages.page_one_options import OPTIONS
from playwright.sync_api import Page
import re


class StepOneDesktop:
    def __init__(self, page):
        self.page: Page = page
        self.desktop = self.page.locator(
            "//div[contains(@class, 'pricing_leftWrapper') and contains(@class, 'pricing_desctop')]")
        self.print_type = PrintType(self.page, self.desktop)
        # self.lamination = Lamination(self.page, self.desktop)
        self.material_melovan_offset = MaterialMelovanOffset(self.page, self.desktop)
        self.material_melovan_digital = MaterialMelovanDigital(self.page, self.desktop)
        self.material_design = MaterialDesign(self.page, self.desktop)
        self.material_3d = Material3d(self.page, self.desktop)

        self.tooltip = Tooltip(self.page, self.desktop)
        self.priceSelector = PriceSelector(self.page, self.desktop)
        self.confirmation_popup = ConfirmationPopup(self.page, self.desktop)


class PrintType:
    def __init__(self, page, desktop):
        self.page = page
        self.desktop = desktop

    def set_print_type(self, print_type: OPTIONS.PRINT):
        # locator = self.desktop.locator()
        # self.desktop.locator(f'text={print_type}').click()
        self.desktop.locator(f"//button[text()[contains(.,'{print_type}')]]").click()


class Lamination:
    def __init__(self, page, desktop):
        self.page = page
        self.desktop = desktop

    def set_lamination_type(self, lamination_type: OPTIONS.LAMINATION_TYPE):
        self.desktop.locator(f'text={lamination_type}').click()

    def set_lamination_thickness_option(self, lamination_thickness: OPTIONS.LAMINATION_THICKNESS):
        self.desktop.locator(f'text={lamination_thickness}').click()

    def is_lamination_thickness_option_unavailable(self):
        pass


class SharedOptions:
    def __init__(self, page, desktop):
        self.page = page
        self.desktop = desktop

    def set_size(self, size: OPTIONS.SIZE):
        self.desktop.locator(f'text={size}').click()

    def set_full_color_sides(self, full_color_sides: OPTIONS.FULL_COLOR_PRINT):
        self.desktop.locator(f'text={full_color_sides}').click()

    def set_rounding(self, rounding: OPTIONS.ROUNDING):
        self.desktop.locator(f"//button[text()='{rounding}']").click()

        # self.desktop.locator(f'text={rounding}').click()

    def set_quantity(self, quantity: OPTIONS.QUANTITY):
        pricing_locator = self.desktop.locator("//div[contains(@class, 'pricing_whideSelector')]")
        # pricing_locator.locator(f'text={quantity}').click()
        pricing_locator.locator(f"//button[text()='{quantity}']").click()


    def set_lamination_type(self, lamination_type: OPTIONS.LAMINATION_TYPE):
        self.desktop.locator(f'text={lamination_type}').click()

    def set_thickness(self, thickness: OPTIONS.LAMINATION_THICKNESS):
        self.desktop.locator(f'text={thickness}').click()


class MaterialMelovanOffset(SharedOptions):
    def __init__(self, page, desktop):
        super().__init__(page, desktop)
        self.page = page
        self.desktop = desktop

    def set_material_melovan(self):
        self.desktop.locator(f'text={OPTIONS.MATERIAL.MELOVAN}').click()


class MaterialMelovanDigital(SharedOptions, Lamination):
    def __init__(self, page, desktop):
        super().__init__(page, desktop)
        self.page = page
        self.desktop = desktop

    def set_material_melovan(self):
        self.desktop.locator(f'text={OPTIONS.MATERIAL.MELOVAN}').click()


class Material3d(SharedOptions, Lamination):
    def __init__(self, page, desktop):
        super().__init__(page, desktop)
        self.page = page
        self.desktop = desktop

    def set_meterial_3d(self):
        self.desktop.locator(f'text={OPTIONS.MATERIAL.WITH_3D}').click()

    def set_foil_and_varnish_side(self, foil_side: OPTIONS.FOIL_SIDE):
        self.desktop.locator(f'text={foil_side}').click()

    def set_varnish_front(self, varnish_front: OPTIONS.VARNISH_FRONT):
        varnish_front_options = self.desktop.locator(
            "//span[text()[contains(.,'3D-лак выборочный на лицевой стороне')]]/ancestor::section")
        varnish_front_options.locator(f'text="{varnish_front}"').click()

    def set_varnish_back(self, varnish_back: OPTIONS.VARNISH_BACK):
        varnish_back_options = self.desktop.locator(
            "//span[text()[contains(.,'3D-лак выборочный на оборотной стороне')]]/ancestor::section")
        varnish_back_options.locator(f'text="{varnish_back}"').click()

    def set_foil_front(self, foil_front: OPTIONS.FOIL_OPTIONS):
        foil_front_options = self.desktop.locator(
            "//span[text()[contains(.,'3D-фольга на лицевой стороне')]]/ancestor::section")
        foil_front_options.locator(foil_front).click()

    def set_foil_back(self, foil_back: OPTIONS.FOIL_OPTIONS):
        foil_back_options = self.desktop.locator(
            "//span[text()[contains(.,'3D-фольга на обратной стороне')]]/ancestor::section")
        foil_back_options.locator(foil_back).click()


class MaterialDesign(SharedOptions):
    def __init__(self, page, desktop):
        super().__init__(page, desktop)
        self.page = page
        self.desktop = desktop

    def set_material_designer(self):
        self.desktop.locator(f'text={OPTIONS.MATERIAL.DESIGNERS}').click()


class PriceSelector:
    def __init__(self, page, desktop):
        self.page = page
        self.desktop = desktop
        self.section_time_first = self.desktop.locator(
            "//div[contains(@class, 'price-selector_wrapper')]/div[3]")
        self.section_time_second = self.desktop.locator(
            "//div[contains(@class, 'price-selector_wrapper')]/div[5]")
        self.section_price_order_first = self.desktop.locator(
            "//div[contains(@class, 'price-selector_wrapper')]/div[4]")
        self.section_price_order_second = self.desktop.locator(
            "//div[contains(@class, 'price-selector_wrapper')]/div[6]")

    def get_ready_time_first(self):
        ready_in_days = self.section_time_first.locator('div[class^="price-selector_days"]').inner_text()
        parsed_ready_in_days =ready_in_days.split()[0]
        ready_date = self.section_time_first.locator('div[class^="price-selector_date"]').inner_text()
        parsed_ready_date = re.search(" (?<=Будет готово: ).*", ready_date)[0].strip()
        return parsed_ready_in_days, parsed_ready_date

    def get_ready_time_second(self):
        ready_in_days = self.section_time_second.locator('div[class^="price-selector_days"]').inner_text()
        parsed_ready_in_days =ready_in_days.split()[0]
        ready_date = self.section_time_second.locator('div[class^="price-selector_date"]').inner_text()
        parsed_ready_date = re.search(" (?<=Будет готово: ).*", ready_date)[0].strip()
        return parsed_ready_in_days, parsed_ready_date

    def get_price_first(self):
        price = self.section_price_order_first.locator('div[class^="price-selector_price"]').inner_text().split()[0]
        return int(price)

    def get_price_second(self):
        price = self.section_price_order_second.locator('div[class^="price-selector_price"]').inner_text().split()[0]
        return int(price)

    def select_term_first(self):
        self.section_price_order_first.locator('button').click()

    def select_term_second(self):
        self.section_price_order_second.locator('button').click()


class Tooltip:
    def __init__(self, page, desktop):
        self.page = page
        self.desktop = desktop

    def is_visible(self):
        pass

    def get_image_name(self):
        pass

    def get_title(self):
        pass

    def get_subscript(self):
        pass

class ConfirmationPopup:
    def __init__(self, page, desktop):
        self.page = page
        self.desktop = desktop

    def confirm(self):
        self.page.locator("text='Далее'").click()

class StepOneMobile:
    pass
