from todo_list.models.enum import StringEnum


class Events(StringEnum):
    CANCEL = "-CANCEL-"
    COMPLETED = "-COMPLETE-"
    EDIT = "-EDIT-"
    EXIT = "-EXIT-"
    NEW = "-NEW-"
    REFRESH = "-REFRESH-"
    SAVE = "-SAVE-"
    SET_CATEGORY = "-SET-CATEGORY-"
