from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.constants import TIME_PATTERN
from app.sample import (
    spreadsheet_body, permissions_body, update_body
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создание электронной таблицы в googleapis."""
    now_date_time = datetime.now().strftime(TIME_PATTERN)
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body(now_date_time))
    )
    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    """Разрешение прав для предоставление отчёта пользователю."""
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body(settings.email),
            fields="id"
        ))


async def spreadsheets_update_value(
    spreadsheet_id: str,
    charity_projects: list,
    wrapper_services: Aiogoogle
) -> None:
    """Структруирование даных для отчета в электроной таблице."""
    now_date_time = datetime.now().strftime(TIME_PATTERN)
    service = await wrapper_services.discover('sheets', 'v4')
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body(now_date_time, charity_projects)
        )
    )
