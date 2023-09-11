from rich.console import Console


CONSOLE = Console()


def get_input(message, password=None, skip_leading_newline=False):
    if not skip_leading_newline or password:
        print('\n',)
    return CONSOLE.input(message + '\n', password=password)

