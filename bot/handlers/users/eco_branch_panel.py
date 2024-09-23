from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from filters import ChatTypeFilter, AdminFilter
from loader import dp, db, bot
from keyboards.inline import eco_branches_inlines, EcoBranchCallbackData, eco_branch_detail, get_employees_inlines_by_branch
from keyboards.default import employee_menu


@dp.message(ChatTypeFilter('private'), AdminFilter(), lambda msg: msg.text in ["🏢 Punktlar", "🏢 Пункты"])
async def eco_branch_list_panel(message: Union[Message, CallbackQuery], lang='uz'):
    if isinstance(message, Message):
        lang = 'ru' if message.text == "🏢 Пункты" else 'uz'
        await message.answer(message.text, reply_markup=await eco_branches_inlines(lang))
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_text("🏢 Пункты" if lang == 'uz' else "🏢 Punktlar", reply_markup=await eco_branches_inlines(lang))


@dp.callback_query(AdminFilter(), EcoBranchCallbackData.filter())
async def eco_branch_callback(call: CallbackQuery, callback_data: EcoBranchCallbackData, state: FSMContext):
    branch_id = callback_data.branch_id
    lang = callback_data.lang
    level = callback_data.level
    action = callback_data.action
    if level == -1:
        await call.message.delete()
    elif level == 0:
        await eco_branch_list_panel(call, lang)
    elif level == 1:
        await eco_branch_detail_func(call, branch_id, lang)
    elif level == 2:
        if action == 'deactivate':
            await deactivate_eco_branch_func(call, branch_id, lang)
        elif action == 'activate':
            await activate_eco_branch_func(call, branch_id, lang)
        elif action == 'edit':
            await edit_eco_branch_func(call, branch_id, lang, state)
        elif action == 'remove_employees_list':
            await remove_employees_list_func(call, branch_id, lang=lang)
        elif action == 'add_employee':
            await add_employee_func(call, branch_id, lang=lang, state=state)
    elif level == 3:
        await remove_employee_func(call, branch_id, action, lang)


async def eco_branch_detail_func(call, branch_id, lang):
    eco_branch = await db.get_eco_branch(branch_id)
    employees = await db.get_employees_by_branch(branch_id)

    # Formatlangan matn
    if lang == 'uz':
        message_text = (
            f"🆔 ID: {eco_branch['id']}\n"
            f"🏢 Nomi: {eco_branch['name_uz']}\n"
            f"👤 Egasining FIO: {eco_branch['chief_name']}\n"
            f"📞 Telefon: {eco_branch['phone']}\n"
            f"📍 Manzil: {eco_branch['address_uz']}\n"
            f"🕒 Ish vaqti: {eco_branch['start_time']} - {eco_branch['end_time']}\n"
            f"📅 Ish kunlari: {eco_branch['working_days']}\n"
            f"📍 Koordinatalar: {eco_branch['latitude']}, {eco_branch['longitude']}\n"
            f"ℹ️ Ma'lumot: {eco_branch['information']}\n"
            f"⏳  Aktivlik vaqti: {eco_branch['activity_time'].strftime('%H:%M, %d-%m-%Y, %A')}\n\n"
            f"Holat: {'🟢 Aktiv' if eco_branch['is_active'] else '🔴 Noaktiv'}"
        )
        if employees:
            employees_text = "\n".join([f"{i + 1}. {employee['fullname']} - {employee['phone']}" for i, employee in enumerate(employees)])
            message_text += f"\n\n<b>Xodimlar</b>\n{employees_text}"
    else:  # rus tili uchun
        message_text = (
            f"🆔 ID: {eco_branch['id']}\n"
            f"🏢 Название: {eco_branch['name_ru']}\n"
            f"👤 ФИО начальника: {eco_branch['chief_name']}\n"
            f"📞 Телефон: {eco_branch['phone']}\n"
            f"📍 Адрес: {eco_branch['address_ru']}\n"
            f"🕒 Время работы: {eco_branch['start_time']} - {eco_branch['end_time']}\n"
            f"📅 Рабочие дни: {eco_branch['working_days']}\n"
            f"📍 Координаты: {eco_branch['latitude']}, {eco_branch['longitude']}\n"
            f"ℹ️ Информация: {eco_branch['information']}\n"
            f"⏳  Время активности: {eco_branch['activity_time'].strftime('%H:%M, %d-%m-%Y, %A')}\n\n"
            f"Статус: {'🟢 Активен' if eco_branch['is_active'] else '🔴 Неактивен'}"
        )
        if employees:
            employees_text = "\n".join([f"{i + 1}. {employee['fullname']} - {employee['phone']}" for i, employee in enumerate(employees)])
            message_text += f"\n\n<b>Сотрудники</b>\n{employees_text}"

    if isinstance(call, CallbackQuery):
        await call.message.edit_text(message_text, reply_markup=await eco_branch_detail(branch_id, lang))
    elif isinstance(call, Message):
        await call.answer(message_text, reply_markup=await eco_branch_detail(branch_id, lang))


async def deactivate_eco_branch_func(call, branch_id, lang):
    await db.deactivate_eco_branch(branch_id)
    await eco_branch_detail_func(call, branch_id, lang)
    await call.message.answer("✅ Eko punkt aktivsizlantirildi!" if lang == 'uz' else "✅ Eko пункт был деактивирован!")
    MESSAGES = {
        'uz': "Eko punkt aktivsiztirildi!",
        'ru': "Эко пункт был деактивирован!"
    }
    employees = await db.get_employees_by_eco_branch(branch_id)
    if employees:
        for emp in employees:
            try:
                await bot.send_message(emp['chat_id'], MESSAGES[emp['lang']], reply_markup=ReplyKeyboardRemove())
            except Exception:
                pass


async def activate_eco_branch_func(call, branch_id, lang):
    await db.activate_eco_branch(branch_id)
    await eco_branch_detail_func(call, branch_id, lang)
    MESSAGES = {
        'uz': "Eko punkt muvaffaqiyatli aktivlashtirildi!",
        'ru': "Еко пункт был успешно активирован!",
    }
    await call.message.answer("✅ Eko punkt muvaffaqiyatli aktivlashtirildi!" if lang == 'uz' else "✅ Eko пункт был успешно активирован!")
    employees = await db.get_employees_by_eco_branch(branch_id)
    if employees:
        for emp in employees:
            try:
                await bot.send_message(emp['chat_id'], MESSAGES[emp['lang']], reply_markup=await employee_menu(emp['lang']))
            except Exception:
                pass


async def edit_eco_branch_func(call, branch_id, lang, state: FSMContext = None):
    from .admin_handler import add_or_edit_eco_branch
    await call.message.edit_text("Eko punktni o'zgartirish!" if lang == 'uz' else "Изменить Eko пункт!",
                                 reply_markup=None)
    await add_or_edit_eco_branch(call.message, state, branch_id)


async def remove_employees_list_func(call, branch_id, lang):
    TEXTS = {
        'uz': "O'chirish uchun xodimni tanlang!",
        'ru': "Выберите сотрудника для удаления!"
    }
    await call.message.edit_text(TEXTS[lang], reply_markup=await get_employees_inlines_by_branch(branch_id, lang))


async def remove_employee_func(call, branch_id, employee_id, lang):
    await db.remove_employee(employee_id)
    await eco_branch_detail_func(call, branch_id, lang)
    await call.message.answer("✅ Xodim muvaffaqiyatli o'chirildi!" if lang == 'uz' else "✅ Сотрудник был успешно удален!")


async def add_employee_func(call, branch_id, lang, state: FSMContext = None):
    from .admin_handler import add_employee_handler
    await call.message.edit_text("Xodimni qo'shish!" if lang == 'uz' else "Добавить сотрудника!", reply_markup=None)
    await add_employee_handler(call.message, state, branch_id, lang)
