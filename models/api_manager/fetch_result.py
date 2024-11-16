class FetchResult:
    def __init__(self, success: bool, data: dict = None, status: int = 200, error: str = None, type_error: str = None):
        self.success = success
        self.data = data
        self.status = status
        self.error = error
        self.type_error = type_error