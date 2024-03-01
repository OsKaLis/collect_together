from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        name_project: str,
        session: AsyncSession,
    ) -> Optional[int]:
        project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == name_project
            )
        )
        return project_id.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[dict[str, str, str]]:
        all_project = await session.execute(
            select([CharityProject.id,
                    CharityProject.name,
                    CharityProject.create_date,
                    CharityProject.close_date,
                    CharityProject.description]).where(
                CharityProject.fully_invested == 1
            )
        )
        resulting_data = []
        sorting_data = []
        for project in all_project.all():
            data_project = {}
            data_time_spent = {}
            data_project['id'] = project['id']
            data_project['name'] = project['name']
            number_days = project['close_date'] - project['create_date']
            data_time_spent['id'] = project['id']
            data_time_spent['number_days'] = number_days.total_seconds()
            data_project['number_days'] = str(number_days)
            data_project['description'] = project['description']
            sorting_data.append(data_time_spent)
            resulting_data.append(data_project)

        for index in range(len(sorting_data) - 1):
            for key in range(len(sorting_data) - index - 1):
                left_number_days = sorting_data[key]['number_days']
                right_number_days = sorting_data[key + 1]['number_days']
                if left_number_days > right_number_days:
                    buffer = sorting_data[key]
                    sorting_data[key] = sorting_data[key + 1]
                    sorting_data[key + 1] = buffer

        result = []
        for data_time_spent in sorting_data:
            for data_project in resulting_data:
                if data_time_spent['id'] == data_project['id']:
                    result.append(
                        {'name': data_project['name'],
                         'number_days': data_project['number_days'],
                         'description': data_project['description']}
                    )
        return result


charity_project_crud = CRUDCharityProject(CharityProject)
