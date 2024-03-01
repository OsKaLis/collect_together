from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession


def closing_data(
    obj: object,
    session,
    invested_amount: int,
    create: bool = False,
):
    """Закрывает инвестиции или проект (CharityProject или Donation)."""
    dt = datetime.now()
    if create:
        obj_close = obj.dict(exclude_unset=True)
        obj_close['fully_invested'] = True
        obj_close['invested_amount'] = invested_amount
        obj_close['close_date'] = dt
        return obj_close
    obj.fully_invested = True
    obj.invested_amount += invested_amount
    obj.close_date = dt
    session.add(obj)
    session.commit()


async def calculation_investments(
    obj_new: object,
    obj_desired: object,
    session: AsyncSession,
    current_invested_amount: int = 0,
    update: bool = False,
):
    """Основная функция расщёта."""
    ceiling_current = obj_new.full_amount - current_invested_amount
    while True:
        data_desired = await obj_desired.get_first_false_fully_invested(
            session
        )
        if data_desired is None:
            new_data = obj_new.dict(exclude_unset=True)
            if not update:
                new_data['invested_amount'] = (obj_new.full_amount -
                                               ceiling_current)
            break
        introduction = data_desired.full_amount
        introduction -= data_desired.invested_amount
        if ceiling_current < introduction:
            data_desired.invested_amount += ceiling_current
            session.add(data_desired)
            session.commit()
            new_data = closing_data(
                obj_new, session, obj_new.full_amount, True
            )
            break
        if obj_new.full_amount == introduction:
            closing_data(data_desired, session, introduction)
            new_data = closing_data(
                obj_new, session, obj_new.full_amount, True
            )
            break
        ceiling_current -= introduction
        closing_data(data_desired, session, introduction)
    return new_data
