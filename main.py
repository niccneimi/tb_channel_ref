##############################IMPORTS################################
from aiogram import Bot, Dispatcher, F
from aiogram.types import ChatMemberUpdated
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.filters import CommandStart,Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import asyncio, logging, markups as mk, time
from datetime import datetime, timedelta
from FSM import *
from config import *
from db import Database

bot = Bot(TOKEN)
dp = Dispatcher()
db = Database(r'domophone.db')
#####################################################################

##############################COMANDS################################
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    if message.from_user.id in admin_list:
        await message.answer(hello_text,reply_markup=mk.admin_main_kb)
    else:  
        await message.answer(hello_text,reply_markup=mk.main_kb)
    await state.clear()
#####################################################################
    
##############################BUTTONS################################
@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def check_new_user(message: ChatMemberUpdated, state: FSMContext):
    if message.invite_link!=None:
        if not db.new_exists(message.from_user.username):
            db.edit_balance(str(message.invite_link.invite_link))
            db.edit_money(str(message.invite_link.invite_link),40)
            db.add_new(message.from_user.username)
            db.add_new_ref_id(str(message.invite_link.invite_link),message.from_user.username)

@dp.message(change_sub.change_sub1)
async def send_func(message: Message, state: FSMContext):
    mesg = message.text
    if mesg != "Отмена":
        try:
            mesg = int(mesg)
            for usr in db.get_all_users():
                db.fast_ed_money(usr[1],(db.get_money(usr[1])//db.get_change())*int(mesg))
            db.edit_change(int(mesg))
            await message.answer('Цена успешно изменена',reply_markup=mk.admin_main_kb)
            await state.clear()
        except:
            await message.answer("Некорректное число! Попробуйте ещё раз")
    else:
        await message.answer("Изменение отменено!",reply_markup=mk.admin_main_kb)
        await state.clear()

@dp.message(sender.sender1)
async def send_func(message: Message, state: FSMContext):
    mesg = message.text
    if mesg != "Отмена":
        for users_id in db.get_all_users():
            try:
                await bot.send_message(users_id[1],mesg)
            except:
                pass
        await message.answer("Рассылка завершена!",reply_markup=mk.admin_main_kb)
    else:
        await message.answer("Рассылка отменена!",reply_markup=mk.admin_main_kb)
    await state.clear()

@dp.message(finance.finance1)
async def send_func(message: Message, state: FSMContext):
    card_data = message.text
    if card_data != "Отмена":
        await message.answer("Введите необходимую сумму одним числом без пробелов")
        await state.update_data(card_data = card_data)
        await state.set_state(finance.finance2)
    else:
        if message.from_user.id in admin_list:
            rp_mkp = mk.admin_main_kb
        else:
            rp_mkp = mk.main_kb
        await message.answer('Вывод средств отменён',reply_markup=rp_mkp)
        await state.clear()
    
@dp.message(finance.finance2)
async def send_func(message: Message, state: FSMContext):
    mesg = message.text
    data = await state.get_data()
    if mesg != "Отмена":
        mesg_link = db.get_inv_url(message.from_user.id)
        try:
            vivod = -int(mesg)
            if db.get_money(message.from_user.id)>=int(mesg) and int(mesg)>0:
                db.edit_money(mesg_link,vivod)
                tmp_us_name = []
                for us_name in db.get_new_by_ref_id(message.from_user.id):
                    tmp_us_name.append("@"+us_name[0])
                tmp_us_name = '\n'.join(tmp_us_name)
                for admin in admin_list:
                    await bot.send_message(admin,f'Запрос вывода средств от @{message.from_user.username}\nДанные карты:\n{data["card_data"]}\nСумма: {mesg} рублей\nЕго реф-ссылка: {mesg_link}\nЕго рефералы:\n{tmp_us_name}')
                await message.answer('Запрос отправлен на проверку!',reply_markup=mk.main_kb)
                await state.clear()
            else:
                await message.answer(f'Вывод суммы {mesg} невозможен, проверьте корректность введённой суммы, и попробуте ещё раз. Нехватка средств')
        except:
            await message.answer(f'Вывод суммы {mesg} невозможен, проверьте корректность введённой суммы, и попробуте ещё раз')
    else:
        if message.from_user.id in admin_list:
            rp_mkp = mk.admin_main_kb
        else:
            rp_mkp = mk.main_kb
        await message.answer('Вывод средств отменён',reply_markup=rp_mkp)
        await state.clear()

@dp.message()
async def echo(message: Message, state: FSMContext):
    msg = message.text
    if message.chat.type == 'private':
        if msg == "🔗 Получить ссылку":
            if not db.get_try_free(message.from_user.id):
                expire_date = datetime.now() + timedelta(days=1000)
                link = await bot.create_chat_invite_link(channel_id, expire_date=expire_date)
                await message.answer(f"Ваша ссылка:\n<code>{link.invite_link}</code>",parse_mode='html')
                db.add_inv_url(message.from_user.id,str(link.invite_link))
                db.edit_try_free(message.from_user.id)
            else:
                await message.answer(f"У вас уже есть активная ссылка:\n<code>{db.get_inv_url(message.from_user.id)}</code>",parse_mode='html')
        if msg == "📈 Cтатистика":
            await message.answer(f"Вы пригласили: {db.get_balance(message.from_user.id)}\nБаланс: {db.get_money(message.from_user.id)} рублей")
        if msg == '📝 Правила':
            await message.answer(rules)
        if msg == '💵 Выввод денег':
            if db.get_money(message.from_user.id)>=400:
                await message.answer("Пришлите данные вашей карты для вывода средств",reply_markup=mk.cancel_button)
                await state.set_state(finance.finance1)
            else:
                await message.answer('Для вывода средств необходим минимальный баланс в 400 рублей')
        if message.from_user.id in admin_list:
            if msg == 'Сделать рассылку':
                await message.answer('Следующее присланное вами сообщение будет разослано всем пользователям бота',reply_markup=mk.cancel_button)
                await state.set_state(sender.sender1)
            if msg == 'Общая статистика':
                await message.answer(f'Всего пользуются ботом: {db.get_users_count()}')
            if msg == "Изменить цену":
                await message.answer(f'Введите цену за 1 подписчика числом без пробелов',reply_markup=mk.cancel_button)
                await state.set_state(change_sub.change_sub1)

#####################################################################

##############################START##################################
async def main():
    await dp.start_polling(bot,allowed_updates=["message", "inline_query", "chat_member"])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())