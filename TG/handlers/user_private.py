from aiogram import  F, types, Router
from aiogram.filters import CommandStart, Command, or_f
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_products
from filters.chat_types import ChatTypeFilter
from keyboards.reply import get_keyboard


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "Привет, я виртуальный помощник",
        reply_markup=get_keyboard(
            "Мужская одежда",
            "Женская одежда",
            "Как найти?",
            "Меню",
            placeholder="Что вас интересует?",
            sizes=(2,2)
        ),
    )


@user_private_router.message(or_f(Command("men"), (F.text.lower().contains('мужск'))))
async def men_cmd(message: types.Message):
    await message.answer("Ассортимент мужской одежды")



@user_private_router.message(or_f(Command("women"), (F.text.lower().contains('женск'))))
async def women_cmd(message: types.Message):
    await message.answer("Ассортимент женской одежды")



@user_private_router.message(or_f(Command("adress"), (F.text.lower().contains('найти'))))
async def menu_cmd(message: types.Message):
    await message.answer("Вот как можно меня найти: ...")



#@user_private_router.message(F.text.lower() == 'меню')
@user_private_router.message(or_f(Command("menu"), (F.text.lower() == 'меню')))
async def menu_cmd(message: types.Message, session: AsyncSession()):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\</strong>\n{product.description}\nСтоимость: {round(product.price, 2)}",
        )
    await message.answer("Вот меню")


