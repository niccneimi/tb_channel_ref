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
    await message.answer("Текст приветствия",reply_markup=mk.main_kb)
    await state.clear()
#####################################################################
    
##############################BUTTONS################################
@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def check_new_user(message: ChatMemberUpdated, state: FSMContext):
    if message.invite_link!=None:
        if not db.new_exists(message.from_user.username):
            db.edit_balance(str(message.invite_link.invite_link))
            db.add_new(message.from_user.username)
        

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
            await message.answer(f"Вы пригласили: {db.get_balance(message.from_user.id)}")
#####################################################################

##############################START##################################
async def main():
    await dp.start_polling(bot,allowed_updates=["message", "inline_query", "chat_member"])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())