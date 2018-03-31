class Message:
    def __init__(self,
                 *,
                 success: bool=True,
                 message: str=''):
        self.success = success
        self.message = message

    def __str__(self):
        return f'{"+OK" if self.success else "-ERR"}{self.message}\n'
