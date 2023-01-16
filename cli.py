import os
from typing import Dict, Any, List

import commands

VALUES: Dict[str, bool] = {"title": True, "url": True, "notes": False}


class Option:
    def __init__(self, name, command, prep_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        print(data)
        message = self.command.execute(data) if data else self.command.execute()
        print(message)

    def __repr__(self):
        return self.name


def get_user_input(data_names: Dict[str, bool]) -> Dict[str, Any]:
    user_data = {}
    for data_name, is_required in data_names.items():
        inp_value = input(f"Please write {data_name}: ")
        while not inp_value and is_required:
            inp_value = input(f"Please write {data_name}: ")
        user_data[data_name] = inp_value
    return user_data


def get_data_to_add(values: Dict[str, bool]=VALUES):
    return get_user_input(values)


def get_data_to_delete():
    return get_user_input({"Id": True})


def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)

OPTION = {
        'A': Option('Add a bookmark', commands.AddBookmarkCommand(), prep_call=get_data_to_add),
        'B': Option('List bookmarks by date', commands.ListBookmarksCommand()),
        'T': Option('List bookmarks by title', commands.ListBookmarksCommand(order_by='title')),
        'D': Option('Delete a bookmark', commands.DeleteBookmarkCommand(), prep_call=get_data_to_delete),
        'Q': Option('Quit', commands.QuitCommand())}


def loop():
    while True:
        for shortcut, option in OPTION.items():
            print(f'({shortcut}) {option}')
        commands_short = input("Choose option: ")
        if commands_short.upper() not in OPTION.keys():
            print('wrong command')
        else:
            option = OPTION[commands_short.upper()]
        option.choose()


if __name__ == "__main__":
    print("welcome to bark")
    commands.CreateBookmarksTableCommand().execute()

    loop()
    clear_screen()
