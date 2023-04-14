from enum import Enum

class UserRoleEnum(Enum):
    ADMIN = "Role_admin"
    AFFILIATE = "Role_affiliate"
    DIRECT_SALE = "Role_direct_sale"
    SUB_VENDOR = "Role_sub_vendor"

class ModelNameEnum(Enum):
    USER_MODEL = 'user'
    PRODUCT_MODEL = "product"
    SETTING_MODEL = "setting"
    ORDER_MODEL = "order"