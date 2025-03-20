class BaseError(Exception):
    def __init__(
            self,
            status_code: int = 500,
            detail: str = "Unkown Error",
            *args: object
    ) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(*args)