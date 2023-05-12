from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from sql_func import count, select_all, select
from config import admins


class AdvertCallback(CallbackData, prefix="advert"):
    name: str
    id: int

class SettingCallback(CallbackData, prefix="setting"):
    name: str

class CreateCallback(CallbackData, prefix="create"):
    name: str

class EditCallback(CallbackData, prefix="edit"):
    name: str
    id: int

class EditDataCallback(CallbackData, prefix = 'edit_data'):
  name: str
  id: int
  type: str


def IsAdmin(id):
    return id in admins


#Клиентские кнопки

def search_kb(id):
    kb = InlineKeyboardBuilder()

    kb.button(text="Кредитная карта", callback_data=AdvertCallback(name="card", id=1))
    kb.button(text="Займ | под 0%", callback_data=AdvertCallback(name="loan", id=1))
    kb.button(text="Кредит | 7.9%", callback_data=AdvertCallback(name="credit", id=1))
    kb.button(
        text="Дебитовая карта",
        callback_data=AdvertCallback(name="debit_card", id=1),
    )
    kb.button(text="Осаго / Каско", callback_data=AdvertCallback(name="casco", id=1))

    if IsAdmin(id):
        kb.button(text="⚙️ Настройки", callback_data="settings")

    kb.adjust(1)
    return kb.as_markup()

def swap_kb(text_url: str, url: str, name: str, id: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=text_url, url=url)],
        [
            InlineKeyboardButton(
                text="⬅️⬅️",
                callback_data=AdvertCallback(
                    name=name, id=id - 1 if id != 1 else count(name)
                ).pack(),
            ),
            InlineKeyboardButton(text="Меню", callback_data="search"),
            InlineKeyboardButton(
                text="➡➡",
                callback_data=AdvertCallback(
                    name=name, id=id + 1 if id + 1 <= count(name) else 1
                ).pack(),
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)

#Admin Buttons
def setting_search():
    kb = InlineKeyboardBuilder()

    kb.button(text="Кредитная карта", callback_data=SettingCallback(name="card"))
    kb.button(text="Займ | под 0%", callback_data=SettingCallback(name="loan"))
    kb.button(text="Кредит | 7.9%", callback_data=SettingCallback(name="credit"))
    kb.button(
        text="Дебитовая карта",
        callback_data=SettingCallback(name="debit_card"),
    )
    kb.button(text="Осаго / Каско", callback_data=SettingCallback(name = "casco"))

    kb.adjust(1)
    return kb.as_markup()

def setting_kb(name: str):
  kb = InlineKeyboardBuilder()
  kb.button(
    text = '↩️Назад',
    callback_data = 'settings'
  )
  for id in select_all(name):
    data = select(name, id)
    kb.button(
      text = data[2],
      callback_data = EditCallback(name = name, id = id)
    )
  kb.button(
    text = '➕ Добавить',
    callback_data = CreateCallback(name = name)
  )
  kb.adjust(1)
  return kb.as_markup()


def edit_kb(name: str, id: int):
  kb = InlineKeyboardBuilder()
  data = select(name)
  kb.button(
    text = '↩️Назад',
    callback_data = SettingCallback(name = name)
  )
  kb.button(
    text = 'Изменить фото',
    callback_data = EditDataCallback(name = name, id = id, type = 'photo')
  )
  kb.button(
    text = 'Изменить текст',
    callback_data = EditDataCallback(name = name, id = id, type = 'text')
  )
  kb.button(
    text = 'Изменить текст кнопка',
    callback_data = EditDataCallback(name = name, id = id, type = 'text_button')
  )
  kb.button(
    text = 'Изменить ссылку кнопка',
    callback_data = EditDataCallback(name = name, id = id, type = 'url')
  )
  kb.adjust(1)  
  return kb.as_markup()
