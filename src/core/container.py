from dependency_injector import containers, providers

from app.application.get_accounts_usecase import GetAccoutsUsecase
from app.application.get_payments_usecase import GetPaymentsUsecase
from app.application.get_users_usecase import GetUsersUsecase
from app.application.getme_usecase import GetMeUsecase
from app.application.login_usecase import LoginUsecase
from app.application.payment_usecase import PaymentUsecase
from app.application.payment_verify_usecase import PaymentVerifyUsecase
from app.application.register_user_usecase import RegisterUserUsecase
from app.infrastructure.security.security import Security
from core.config import settings
from core.database import DataBase
from core.uow import UnitOfWork


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["api.v1"])

    db = providers.Singleton(DataBase, settings.db.dsn)
    security = providers.Singleton(Security)
    uow = providers.Singleton(UnitOfWork, db)


    getme_usecase = providers.Factory(
        GetMeUsecase,
        uow=uow,
        security=security,
    )

    login_usecase = providers.Factory(
        LoginUsecase,
        uow=uow,
        security=security,
    )

    register_user_usecase = providers.Factory(
        RegisterUserUsecase,
        uow=uow,
        security=security,
    )

    get_users_usecase = providers.Factory(
        GetUsersUsecase,
        uow=uow,
    )

    get_payments_usecase = providers.Factory(
        GetPaymentsUsecase,
        uow=uow,
    )

    get_accounts_usecase = providers.Factory(
        GetAccoutsUsecase,
        uow=uow,
    )

    payment_verify_usecase = providers.Factory(
        PaymentVerifyUsecase,
    )

    payment_usecase = providers.Factory(
        PaymentUsecase,
        uow=uow,
    )


