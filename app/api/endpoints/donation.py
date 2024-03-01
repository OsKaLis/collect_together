from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import (
    get_async_session, current_user, current_superuser
)
from app.models.user import User
from app.crud import donation_crud, charity_project_crud
from app.schemas.donation import (
    DonationDB, DonationCreate, DonationDBSuper
)
from app.services.investing import calculation_investments

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDBSuper],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donation_investing(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Получает список всех пожертвований."""
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation_investing(
    new_donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Сделать пожертвование.
    Доступла только авторизированым пользователям."""
    new_donation = await calculation_investments(
        new_donation, charity_project_crud, session
    )
    return await donation_crud.create(
        new_donation, session, user
    )


@router.get(
    '/my',
    response_model=list[DonationDB],
)
async def get_my_donation_investing(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Получить список моих пожертвований."""
    return await donation_crud.get_by_user(
        session=session, user=user
    )
