import hashlib

from core.config import settings
from core.exception import BaseError


class PaymentVerifyUsecase:
    def execute(self, signature: str, data_str: str) -> None:
        sig_hash = hashlib.sha256(
            (data_str + settings.ts.TRANSACTION_KEY).encode(),
        ).hexdigest()
        if sig_hash != signature:
            raise BaseError(status_code=400, detail="Invalid signature")
