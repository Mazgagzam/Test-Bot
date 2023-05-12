from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram.types.input_media_photo import InputMediaPhoto


from keyboards.search import *

from sql_func import select, count

router = Router()

#Клиентская часть

@router.callback_query(lambda call: call.data == "search")
async def search(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer_animation(
        animation="CgACAgIAAxkBAAIKSmRcoEiayNqtSyxUmEHHufz-sY8jAAI6KgAC5cnpSuDirP4l6MdJLwQ",
        caption="🤖 <b>Что Вас интересует?</b>",
        reply_markup=search_kb(call.from_user.id),
    )

@router.callback_query(AdvertCallback.filter())
async def advert_callback(call: CallbackQuery, callback_data: AdvertCallback):
    name, id = callback_data.name, callback_data.id
    advert = select(name, id)

    await call.message.edit_media(
      media = InputMediaPhoto(media = advert[1], caption = advert[2]),
      reply_markup = swap_kb(advert[3], advert[4], name=name, id=id)
    )

    await call.answer(text=f"ОТКРЫТА СТРАНИЦА {id} ИЗ {count(name)}")


#Админская часть

@router.callback_query(lambda call: call.data == 'settings')
async def settings(call: CallbackQuery):
  if call.message.animation:
    await call.message.delete()
    await call.message.answer(
      text = '⚙️ Настройки',
      reply_markup = setting_search()
    )
  else:
    await call.message.edit_text(
      text = '⚙️ Настройки',
      reply_markup = setting_search()
    )

@router.callback_query(SettingCallback.filter())
async def setting(call: CallbackQuery, callback_data: SettingCallback):
  await call.message.edit_text(
    text = call.message.text,
    reply_markup = setting_kb(callback_data.name)
  )

@router.callback_query(EditCallback.filter())
async def edit(call: CallbackQuery, callback_data: EditCallback):
  await call.message.delete()
  photo = select(callback_data.name, callback_data.id)
  await call.message.answer_photo(
    photo = photo[1],
    caption = photo[2],
    reply_markup = edit_kb(callback_data.name, callback_data.id)
  )
