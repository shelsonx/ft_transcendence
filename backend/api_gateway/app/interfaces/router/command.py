
from typing import List


class Command:

    def __init__(self, command_name, do_fun, do_args, undo_fun, undo_args) -> None:
        self.command_name = command_name
        self.do_fun = do_fun
        self.do_args = do_args
        self.undo_fun = undo_fun
        self.undo_args = undo_args

    def execute(self) -> bool:
        return self.do_fun(self.do_args)

    def undo(self) -> bool:
        return self.undo_fun(self.undo_args)



class CommandStack:

    def __init__(self) -> None:
        self.stack: List[Command] = []

    def add_command(self, command: Command):
        self.stack.append(command)

    def remove_command(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        return None

    def execute(self, command: Command):
        if command.execute():
            self.add_command(command)
            return True
        self.undo()
        return False

    def undo(self):
        while True:
            command = self.remove_command()
            if command is None:
                break
            command.undo()


