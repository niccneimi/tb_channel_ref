from aiogram.fsm.state import StatesGroup, State

class sender(StatesGroup):
    sender1 = State()

class finance(StatesGroup):
    finance1 = State()
    finance2 = State()

class change_sub(StatesGroup):
    change_sub1 = State()

class g_refers(StatesGroup):
    g_refers1 = State()

class ban(StatesGroup):
    ban1 = State()