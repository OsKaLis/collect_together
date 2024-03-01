from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import donation_crud, charity_project_crud
from app.core import get_async_session, current_superuser
from app.api.validators import (
    check_name_duplicate, check_charity_project_exists,
    checking_invested_amount_field,
    checking_total_amount_field,
    check_charity_project_fully_invested,
)
from app.services.investing import calculation_investments
from app.schemas.charity_project import (
    CharityProjectDB, CharityProjectCreate,
    CharityProjectUpdate
)

router = APIRouter()


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=list[CharityProjectDB],
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session),
):
    """Доступно всем.
    Получает список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    new_charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Создает благотворительный проект."""
    await check_name_duplicate(new_charity_project.name, session)
    new_charity_project = await calculation_investments(
        new_charity_project, donation_crud, session
    )
    return await charity_project_crud.create(
        new_charity_project, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Удаляет проект. Нельзя удалить проект,
    в который уже были инвестированы средства, его можно только закрыть."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await checking_invested_amount_field(project_id, session)
    return await charity_project_crud.remove(
        charity_project, session
    )


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def charity_project_update(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Закрытый проект нельзя редактировать,
    также нельзя установить требуемую сумму меньше уже вложенной."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_charity_project_fully_invested(
        charity_project.fully_invested
    )
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        await checking_total_amount_field(
            obj_in.full_amount,
            charity_project.invested_amount
        )
        obj_in = await calculation_investments(
            obj_in, donation_crud, session,
            charity_project.invested_amount, True
        )
        charity_project = await charity_project_crud.update(
            charity_project, obj_in, session, True
        )
    else:
        charity_project = await charity_project_crud.update(
            charity_project, obj_in, session
        )
    return charity_project
