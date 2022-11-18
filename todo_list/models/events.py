from todo_list.models.enum import StringEnum


class Events(StringEnum):
    CANCEL = "-CANCEL-"
    COMPLETE = "-COMPLETE-"
    EDIT = "-EDIT-"
    EXIT = "-EXIT-"
    SAVE = "-SAVE-"
