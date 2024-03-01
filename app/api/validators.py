from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
    name_project: str,
    session: AsyncSession,
) -> None:
    """Проверка на дупликат."""
    obj_project = await charity_project_crud.get_project_id_by_name(
        name_project, session
    )
    if obj_project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Запрос на наличие проекта."""
    obj_project = await charity_project_crud.get(project_id, session)
    if obj_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найдена!'
        )
    return obj_project


async def checking_invested_amount_field(
    project_id: int,
    session: AsyncSession,
) -> None:
    """Проверка на полностью инвестированый проект."""
    obj_project = await charity_project_crud.get(project_id, session)
    if obj_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def checking_total_amount_field(
    full_amount: int,
    invested_amount: int,
) -> None:
    """Проверка обновления поля (full_amount) на допустимое значение."""
    if full_amount < invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нелья установить значение full_amount меньше уже вложенной суммы.'
        )


async def check_charity_project_fully_invested(
    check_fully_invested: bool,
) -> None:
    """Проверка на полнастью инвестированый проект."""
    if check_fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
