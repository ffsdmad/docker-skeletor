MENU_CLASSES = enumerate(("top", "footer",))

ICON_CLASSES = enumerate(("top", "footer",))

LAYER_CLASSES = (

)


SUBPRODUCT_TYPES = (
    ("power", "Источники питания"),
    ("control", "Контроллеры"),
    ("lenta", "Лента"),
    ("nakladka", "Накладки FOTON"),
    ("profile", "Профиль"),
    ("ramka", "Рамки / накладки"),
    ("lamp", "Светильники"),
    ("chair", "Стулья"),
    ("track", "Треки"),
    (None, "Другое"),
)

PRODUCT_FLAGS = (
    ("draw_first", "draw_first"),
    ("show_trigger", "show_trigger"),
    ("is_vivod", "is_vivod"),
    ("add_to_cart", "add_to_cart"),
    ("custom_params", "custom_params"),
    ("show_category_color", "показывать цвет в карточке продукта"),
    ("is_main_sub", "is_main_sub"),
    ("is_dependent", "is_dependent"),
)


MANAGER_PRICES = (
    (0, "0"),
    (1, "1"),
    (2, "2"),
)


(STAFF, USER, BUYER, DESIGNER, PARTNER) = ("staff", "user", "buyer", "designer", "partner")

USER_TYPES = (
    (USER, "нет роли"),
    (STAFF, "сотрудник"),
    (BUYER, "покупатель"),
    (DESIGNER, "дизайнер"),
    (PARTNER, "партнёр"),
)
