from pages.page_one_options import OPTIONS

l = [value for name, value in vars(OPTIONS.FOIL_OPTIONS).items() if name.isupper()]
print(l)