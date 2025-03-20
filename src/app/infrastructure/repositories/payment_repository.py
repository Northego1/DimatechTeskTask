from sqlalchemy.ext.asyncio import AsyncSession


class PaymentRepository:
    def __init__(self, conn: AsyncSession) -> None:
        self.conn = conn

