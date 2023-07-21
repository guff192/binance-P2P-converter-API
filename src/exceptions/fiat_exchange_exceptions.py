from fastapi import HTTPException


class BothAmountsError(HTTPException):
    """Both source and destination amounts provided"""
    def __init__(self):
        self.status_code = 400
        self.detail = 'You may set either src_amount or dst_amount, not both of them!'
        self.headers = None


