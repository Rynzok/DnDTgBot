from aiogram.fsm.state import StatesGroup, State

class CreateHero(StatesGroup):
    main = State()
    characteristic = State()
    skill = State()
    save_dice = State()
    hits = State()
    ownership = State()
    ability = State()
    spells = State()
    attack = State()
    inventory = State()
    money = State()
    personality = State()