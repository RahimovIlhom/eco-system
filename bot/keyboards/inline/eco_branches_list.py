from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


class EcoBranchCallbackData(CallbackData, prefix="eco_branch"):
    branch_id: int
    lang: str
    level: int
    action: str


async def create_eco_callback_data(branch_id: int, lang: str = 'uz', level: int = 0, action: str = '') -> str:
    return EcoBranchCallbackData(branch_id=branch_id, lang=lang, level=level, action=action).pack()


async def eco_branches_inlines(lang: str = 'uz') -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 0
    keyboard = InlineKeyboardBuilder()
    branches = await db.get_branches()
    for branch in branches:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{branch['name_uz']}: {'🟢 Aktiv' if branch['is_active'] else '🔴 Noaktiv'}"
                if lang == 'uz' else f"{branch['name_ru']}: {'🟢 Активен' if branch['is_active'] else '🔴 Неактивен'}",
                callback_data=await create_eco_callback_data(branch_id=branch['id'], lang=lang, level=CURRENT_LEVEL+1)
            )
        )
    keyboard.row(
        InlineKeyboardButton(
            text='❌ Yopish' if lang == 'uz' else '❌ Закрыть',
            callback_data=await create_eco_callback_data(branch_id=0, lang=lang, level=CURRENT_LEVEL-1)
        )
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


async def eco_branch_detail(branch_id: int, lang: str = 'uz') -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1
    branch = await db.get_eco_branch(branch_id=branch_id)
    keyboard = InlineKeyboardBuilder()
    deactivate_btn = InlineKeyboardButton(
        text='🔴 Deaktivlash' if lang == 'uz' else '🔴 Деактивировать',
        callback_data=await create_eco_callback_data(branch_id=branch_id, lang=lang, level=CURRENT_LEVEL+1, action='deactivate')
    )
    activate_btn = InlineKeyboardButton(
        text='🟢 Faollashtirish' if lang == 'uz' else '🟢 Активировать',
        callback_data=await create_eco_callback_data(branch_id=branch_id, lang=lang, level=CURRENT_LEVEL+1, action='activate')
    )
    edit_btn = InlineKeyboardButton(
        text='✏️ Tahrirlash' if lang == 'uz' else '✏️ Редактировать',
        callback_data=await create_eco_callback_data(branch_id=branch_id, lang=lang, level=CURRENT_LEVEL+1, action='edit')
    )
    if branch['is_active']:
        keyboard.row(edit_btn, deactivate_btn)
    else:
        keyboard.row(edit_btn, activate_btn)
    remove_employee_btn = InlineKeyboardButton(
        text='🗑 Xodimni o\'chirish' if lang == 'uz' else '🗑 Удалить сотрудника',
        callback_data=await create_eco_callback_data(branch_id=branch_id, lang=lang, level=CURRENT_LEVEL+1, action='remove_employees_list')
    )
    add_employee_btn = InlineKeyboardButton(
        text='👥 Xodim qo\'shish' if lang == 'uz' else '👥 Добавить сотрудника',
        callback_data=await create_eco_callback_data(branch_id=branch_id, lang=lang, level=CURRENT_LEVEL+1, action='add_employee')
    )
    keyboard.row(remove_employee_btn, add_employee_btn)
    keyboard.row(
        InlineKeyboardButton(
            text='◀️ Orqaga' if lang == 'uz' else '◀️ Назад',
            callback_data=await create_eco_callback_data(branch_id=branch_id, lang=lang, level=CURRENT_LEVEL-1)
        )
    )
    return keyboard.as_markup()


async def get_employees_inlines_by_branch(branch_id: int, lang: str = 'uz') -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 2
    employees = await db.get_employees_by_branch(branch_id)
    keyboard = InlineKeyboardBuilder()
    for employee in employees:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{employee['fullname']} - {employee['phone']}",
                callback_data=await create_eco_callback_data(branch_id=branch_id, lang=lang, level=CURRENT_LEVEL+1, action=employee['tg_id'])
            )
        )
    keyboard.row(
        InlineKeyboardButton(
            text='◀️ Orqaga' if lang == 'uz' else '◀️ Назад',
            callback_data=await create_eco_callback_data(branch_id=branch_id, lang=lang, level=CURRENT_LEVEL-1)
        )
    )
    return keyboard.as_markup()
