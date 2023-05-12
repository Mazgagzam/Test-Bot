from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from sql_func import select, append
from keyboards.simple_row import start_kb

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    await message.answer_animation(
        animation="CgACAgIAAxkBAAIKTWRcoJusez2Mo_6c-WzpGrkqwzT9AAJVKgAC5cnpStisY2fwXxl7LwQ",
        caption="<b>🤖Мастер подбора</b> ...\n\n<b>«Деньги Бот»</b> - Ваш надежный пощник в поиске лучше финансовых предложений.",
        reply_markup=start_kb(),
    )


@router.message(Command(commands=["cancel"]))
@router.message(Text(text="отмена", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Действие отменено", reply_markup=ReplyKeyboardRemove())


@router.message()
async def all_msg(message):
    await message.answer(str(message.photo[-1].file_id))
    print(message.photo[-1].file_id)
    await message.answer_animation(message.animation.file_id)
    # await message.answer_photo(photo = message.photo[-1].file_id, caption = message.html_text)
