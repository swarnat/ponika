class TeltonikaApiException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

        self.errors = args[0]

    def __str__(self):
        return ", " . join([str(error) for error in self.errors])
