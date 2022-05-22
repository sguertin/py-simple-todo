from PySimpleGUI import Frame, Input, Window


class ItemView(Frame):
    def __init__(self, layout: list):
        super().__init__("", layout=layout)


class ListView(Window):
    def __init__(self, title: str, layout: list):
        super().__init__(title, layout)


class ManageItemView(Window):
    window: Window
    category_field: Input

    def __init__(self, title: str, layout: list, category_field: Input):
        super().__init__(title, layout)
        self.category_field = category_field

    def update_category(self, value: str) -> None:
        self.category_field.update(value)
