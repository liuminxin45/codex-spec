class Search:
    def __init__(self):
        self.value = None
        self.error = None
        self.loading = False

    def start(self, query):
        self.loading = True
        return query

    def finish(self, token, value=None, error=None):
        self.value = value
        self.error = error
        self.loading = False
