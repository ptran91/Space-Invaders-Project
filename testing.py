class Testing:
    def __init__(self, name:str):
        self.name = name
        Testing.print_message(f'Running tests on {self.name.upper()}')

    def end(self):
        Testing.print_message(f'Ending tests on class {self.name.upper()}', end=True)

    @staticmethod
    def print_message(msg, end=False):
        if not end:
            print()
        print('=' * 50)
        print(msg)
        print('=' * 50)
