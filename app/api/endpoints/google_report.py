from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import (
    get_async_session, get_service, current_superuser
)
from app.crud.charity_project import charity_project_crud
from app.services.google_report import (
    spreadsheets_create, set_user_permissions,
    spreadsheets_update_value,
)

router = APIRouter()


@router.post(
    '/',
    response_model=list[dict[str, str, str]],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    """Только для суперюзеров.
    формирует отчёт в гугл-таблице. В таблице закрытые проекты,
    отсортированные по скорости сбора средств"""
    charity_projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(spreadsheetid,
                                    charity_projects,
                                    wrapper_services)
    return charity_projects
