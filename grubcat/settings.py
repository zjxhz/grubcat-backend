
#set product as false to enable dev settings
PRODUCT = True

if PRODUCT:
    from settings_product import *
else:
    from settings_dev import *