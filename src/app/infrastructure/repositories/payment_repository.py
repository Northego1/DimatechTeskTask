import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.payment import Payment
from app.infrastructure.models.payment_model import PaymentModel


class PaymentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_payment(self, payment: Payment) -> uuid.UUID | None:
        payment_model = PaymentModel.from_domain(payment)
        self.session.add(payment_model)
        try:
            await self.session.flush()
        except IntegrityError:
            return None
        return payment_model.id
