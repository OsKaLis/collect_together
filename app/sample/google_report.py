from datetime import datetime


def spreadsheet_body(now_date_time: datetime):
    """Шаблон для создание электронной таблицы."""
    return {
        'properties': {'title': f'Отчёт на {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 11}}}]
    }


def permissions_body(email: str):
    """Шаблон для установки пользовательских разрешений."""
    return {'type': 'user', 'role': 'writer', 'emailAddress': email}


def update_body(
    now_date_time: datetime,
    charity_projects: list
):
    """Шаблон обновления данных."""
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for res in charity_projects:
        table_values.append(
            [res['name'], res['number_days'], res['description']]
        )
    return {'majorDimension': 'ROWS', 'values': table_values}
