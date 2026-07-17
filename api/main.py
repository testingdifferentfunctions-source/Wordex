from aiogram.types import (Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery)

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from peewee import *
import random
import os
from fastapi import FastAPI, Request
from db import (GreekMonthsWords, GreekNationalitiesWords, GreekOppositesWords,
                GreekGreetingsWords, GreekPronounsWords, GreekColorsWords)


app = FastAPI()

try:
    from dotenv import load_dotenv
    load_dotenv()

except ImportError:
    pass

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)

dp = Dispatcher()
router = Router()

dp.include_router(router)


class TestStates(StatesGroup):
    questions_number = State()
    waiting_for_answer = State()


class TestCallback(CallbackData, prefix="test"):
    answer_id: int


class QuestionsCallback(CallbackData, prefix="test"):
    questions_amount: str


@router.message(Command("start"))
async def start_the_bot(message: Message):
    menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Англійська",
                                                                                callback_data="english_section")],
                                                          [InlineKeyboardButton(text="Французька",
                                                                                callback_data="french_section")],
                                                          [InlineKeyboardButton(text="Німецька",
                                                                                callback_data="german_section")],
                                                          [InlineKeyboardButton(text="Іспанська",
                                                                                callback_data="spanish_section")],
                                                          [InlineKeyboardButton(text="Грецька",
                                                                                callback_data="greek_section")],
                                                          [InlineKeyboardButton(text="Про проєкт",
                                                                                callback_data="about")],
                                                          ])

    await message.answer("<blockquote>Віиаємо у Wordex!</blockquote>\n"
                              "<b>Wordex</b> - це бот, що призначений для вивчення слів різних мов світу.\n"
                              "\n"
                              "Щоб продовжити далі оберіть мову для вивчення",
                              parse_mode=ParseMode.HTML, reply_markup=menu_keyboard)


@router.callback_query(F.data == "home")
async def home_menu(callback: CallbackQuery):
    menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Англійська",
                                                                                callback_data="english_section")],
                                                          [InlineKeyboardButton(text="Французька",
                                                                                callback_data="french_section")],
                                                          [InlineKeyboardButton(text="Німецька",
                                                                                callback_data="german_section")],
                                                          [InlineKeyboardButton(text="Іспанська",
                                                                                callback_data="spanish_section")],
                                                          [InlineKeyboardButton(text="Грецька",
                                                                                callback_data="greek_section")],
                                                          [InlineKeyboardButton(text="Про проєкт",
                                                                                callback_data="about")],
                                                          ])

    await callback.message.answer("<blockquote>Вітаємо у Wordex!</blockquote>\n"
                                      "<b>Wordex</b> - це бот, що призначений для вивчення слів різних мов світу.\n"
                                      "\n"
                                      "Щоб продовжити далі оберіть мову для вивчення",
                                      parse_mode=ParseMode.HTML, reply_markup=menu_keyboard)


@router.callback_query(F.data == "english_section")
async def english_section_option(callback: CallbackQuery):
    await callback.message.answer("Поки нічого немає", parse_mode=ParseMode.HTML)


@router.callback_query(F.data == "french_section")
async def french_section_option(callback: CallbackQuery):
    await callback.message.answer("Поки нічого немає", parse_mode=ParseMode.HTML)


@router.callback_query(F.data == "german_section")
async def german_section_option(callback: CallbackQuery):
    await callback.message.answer("Поки нічого немає", parse_mode=ParseMode.HTML)


@router.callback_query(F.data == "spanish_section")
async def spanish_section_option(callback: CallbackQuery):
    await callback.message.answer("Поки нічого немає", parse_mode=ParseMode.HTML)


@router.callback_query(F.data == "greek_section")
async def greek_section_option(callback: CallbackQuery, state: FSMContext):
    await state.update_data(lang="greek")

    section_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Привітання",
                                                                                   callback_data="greek_section_1")],
                                                             [InlineKeyboardButton(text="Займенники",
                                                                                   callback_data="greek_section_2")],
                                                             [InlineKeyboardButton(text="Кольори",
                                                                                   callback_data="greek_section_3")],
                                                             [InlineKeyboardButton(text="Місяці",
                                                                                   callback_data="greek_section_4")],
                                                             [InlineKeyboardButton(text="Нації",
                                                                                   callback_data="greek_section_5")],
                                                             [InlineKeyboardButton(text="Протилежності",
                                                                                   callback_data="greek_section_6")],
                                                             [InlineKeyboardButton(text="Назад",
                                                                                   callback_data="home")],
                                                            ])

    await callback.message.answer("Оберіть тематику слів", parse_mode=ParseMode.HTML,
                                  reply_markup=section_keyboard)


@router.callback_query(F.data.in_(["greek_section_1", "greek_section_2", "greek_section_3", "greek_section_4",
                                   "greek_section_5", "greek_section_6", "edit_questions_number"]))
async def questions_option(callback: CallbackQuery, state: FSMContext):
    if callback.data != "edit_questions_number":
        await state.update_data(section=callback.data)

    questions_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="10",
                                                                                     callback_data="10")],
                                                             [InlineKeyboardButton(text="15",
                                                                                   callback_data="15")],
                                                             [InlineKeyboardButton(text="20",
                                                                                   callback_data="20")],
                                                             [InlineKeyboardButton(text="Назад",
                                                                                   callback_data="greek_section")],
                                                             ])

    await callback.message.answer("Оберіть кількість питань", parse_mode=ParseMode.HTML,
                                  reply_markup=questions_keyboard)

    await state.set_state(TestStates.questions_number)


@router.callback_query(F.data.in_(["10", "15", "20"]))
async def get_questions(callback: CallbackQuery, state: FSMContext):
    all_questions = int(callback.data)

    await state.set_state(TestStates.waiting_for_answer)
    await state.update_data(score=0, mistakes=0, total_questions=0, used_words=[], words=[],
                            selected_answers=[], right_answers=[], current_variants=[], all_questions=all_questions)

    edit_data = await state.get_data()
    preferred_language = edit_data.get("lang")
    preferred_section = edit_data.get("section")

    await state.update_data(lang=preferred_language, section=preferred_section)

    print(f"DEBUG: Мова = {preferred_language}, Секція = {preferred_section}")

    if preferred_language == "greek":
        if preferred_section == "greek_section_1":
            await greek_greetings_creation(callback, state)

        elif preferred_section == "greek_section_2":
            await greek_pronouns_creation(callback, state)

        elif preferred_section == "greek_section_3":
            await greek_colors_creation(callback, state)

        elif preferred_section == "greek_section_4":
            await greek_months_creation(callback, state)

        elif preferred_section == "greek_section_5":
            await greek_nations_creation(callback, state)

        elif preferred_section == "greek_section_6":
            await greek_opposites_creation(callback, state)

    await callback.answer()


async def greek_greetings_creation(callback: CallbackQuery, state: FSMContext):
    user_choice = await state.get_data()
    used_words = user_choice.get("used_words", [])

    query = GreekGreetingsWords.select()
    if used_words:
        query = query.where(GreekGreetingsWords.greek_original.not_in(used_words))

    if query.count() == 0:
        used_words.clear()
        query = GreekGreetingsWords.select()

    random_word = query.order_by(fn.Random()).get()
    rand_word = random_word.greek_original
    rand_word_translate = random_word.greek_translated

    predicted_answers = [rand_word_translate]
    random_variants = list(GreekGreetingsWords.select().order_by(fn.Random()).limit(5))

    for variant in random_variants:
        if len(predicted_answers) == 3:
            break

        translated_variant = variant.greek_translated
        if translated_variant not in predicted_answers:
            predicted_answers.append(translated_variant)

    print(predicted_answers)
    random.shuffle(predicted_answers)
    print(predicted_answers)

    answers_keyboard = InlineKeyboardBuilder()

    for ids, predicted_answer in enumerate(predicted_answers):
        answers_keyboard.button(text=predicted_answer,
                                callback_data=TestCallback(answer_id=ids).pack()
                                )

        answers_keyboard.adjust(1)
    await state.update_data(current_variants=predicted_answers.copy())

    await callback.message.answer(f"<b>{rand_word}</b>", reply_markup=answers_keyboard.as_markup(),
                                  parse_mode=ParseMode.HTML)
    predicted_answers.clear()

    await state.update_data(right_answer=rand_word_translate, current_word=rand_word)
    await state.set_state(TestStates.waiting_for_answer)

    used_words.append(rand_word)


async def greek_pronouns_creation(callback: CallbackQuery, state: FSMContext):
    user_choice = await state.get_data()
    used_words = user_choice.get("used_words", [])

    query = GreekPronounsWords.select()
    if used_words:
        query = query.where(GreekPronounsWords.greek_original.not_in(used_words))

    if query.count() == 0:
        used_words.clear()
        query = GreekPronounsWords.select()

    random_word = query.order_by(fn.Random()).get()
    rand_word = random_word.greek_original
    rand_word_translate = random_word.greek_translated

    predicted_answers = [rand_word_translate]
    random_variants = list(GreekPronounsWords.select().order_by(fn.Random()).limit(5))

    for variant in random_variants:
        if len(predicted_answers) == 3:
            break

        translated_variant = variant.greek_translated
        if translated_variant not in predicted_answers:
            predicted_answers.append(translated_variant)

    print(predicted_answers)
    random.shuffle(predicted_answers)
    print(predicted_answers)

    answers_keyboard = InlineKeyboardBuilder()

    for ids, predicted_answer in enumerate(predicted_answers):
        answers_keyboard.button(text=predicted_answer,
                                callback_data=TestCallback(answer_id=ids).pack()
                                )

        answers_keyboard.adjust(1)
    await state.update_data(current_variants=predicted_answers.copy())

    await callback.message.answer(f"<b>{rand_word}</b>", reply_markup=answers_keyboard.as_markup(),
                                  parse_mode=ParseMode.HTML)
    predicted_answers.clear()

    await state.update_data(right_answer=rand_word_translate, current_word=rand_word)
    await state.set_state(TestStates.waiting_for_answer)

    used_words.append(rand_word)


async def greek_colors_creation(callback: CallbackQuery, state: FSMContext):
    user_choice = await state.get_data()
    used_words = user_choice.get("used_words", [])

    query = GreekColorsWords.select()
    if used_words:
        query = query.where(GreekColorsWords.greek_original.not_in(used_words))

    if query.count() == 0:
        used_words.clear()
        query = GreekColorsWords.select()

    random_word = query.order_by(fn.Random()).get()
    rand_word = random_word.greek_original
    rand_word_translate = random_word.greek_translated

    predicted_answers = [rand_word_translate]
    random_variants = list(GreekColorsWords.select().order_by(fn.Random()).limit(5))

    for variant in random_variants:
        if len(predicted_answers) == 3:
            break

        translated_variant = variant.greek_translated
        if translated_variant not in predicted_answers:
            predicted_answers.append(translated_variant)

    print(predicted_answers)
    random.shuffle(predicted_answers)
    print(predicted_answers)

    answers_keyboard = InlineKeyboardBuilder()

    for ids, predicted_answer in enumerate(predicted_answers):
        answers_keyboard.button(text=predicted_answer,
                                callback_data=TestCallback(answer_id=ids).pack()
                                )

        answers_keyboard.adjust(1)
    await state.update_data(current_variants=predicted_answers.copy())

    await callback.message.answer(f"<b>{rand_word}</b>", reply_markup=answers_keyboard.as_markup(),
                                  parse_mode=ParseMode.HTML)
    predicted_answers.clear()

    await state.update_data(right_answer=rand_word_translate, current_word=rand_word)
    await state.set_state(TestStates.waiting_for_answer)

    used_words.append(rand_word)


async def greek_months_creation(callback: CallbackQuery, state: FSMContext):
    user_choice = await state.get_data()
    used_words = user_choice.get("used_words", [])

    query = GreekMonthsWords.select()
    if used_words:
        query = query.where(GreekMonthsWords.greek_original.not_in(used_words))

    if query.count() == 0:
        used_words.clear()
        query = GreekMonthsWords.select()

    random_word = query.order_by(fn.Random()).get()
    rand_word = random_word.greek_original
    rand_word_translate = random_word.greek_translated

    predicted_answers = [rand_word_translate]
    random_variants = list(GreekMonthsWords.select().order_by(fn.Random()).limit(5))

    for variant in random_variants:
        if len(predicted_answers) == 3:
            break

        translated_variant = variant.greek_translated
        if translated_variant not in predicted_answers:
            predicted_answers.append(translated_variant)

    print(predicted_answers)
    random.shuffle(predicted_answers)
    print(predicted_answers)

    answers_keyboard = InlineKeyboardBuilder()

    for ids, predicted_answer in enumerate(predicted_answers):
        answers_keyboard.button(text=predicted_answer,
                                callback_data=TestCallback(answer_id=ids).pack()
                                )

        answers_keyboard.adjust(1)
    await state.update_data(current_variants=predicted_answers.copy())

    await callback.message.answer(f"<b>{rand_word}</b>", reply_markup=answers_keyboard.as_markup(),
                                  parse_mode=ParseMode.HTML)
    predicted_answers.clear()

    await state.update_data(right_answer=rand_word_translate, current_word=rand_word)
    await state.set_state(TestStates.waiting_for_answer)

    used_words.append(rand_word)


async def greek_nations_creation(callback: CallbackQuery, state: FSMContext):
    user_choice = await state.get_data()
    used_words = user_choice.get("used_words", [])

    query = GreekNationalitiesWords.select()
    if used_words:
        query = query.where(GreekNationalitiesWords.greek_original.not_in(used_words))

    if query.count() == 0:
        used_words.clear()
        query = GreekNationalitiesWords.select()

    random_word = query.order_by(fn.Random()).get()
    rand_word = random_word.greek_original
    rand_word_translate = random_word.greek_translated

    predicted_answers = [rand_word_translate]
    random_variants = list(GreekNationalitiesWords.select().order_by(fn.Random()).limit(5))

    for variant in random_variants:
        if len(predicted_answers) == 3:
            break

        translated_variant = variant.greek_translated
        if translated_variant not in predicted_answers:
            predicted_answers.append(translated_variant)

    print(predicted_answers)
    random.shuffle(predicted_answers)
    print(predicted_answers)

    answers_keyboard = InlineKeyboardBuilder()

    for ids, predicted_answer in enumerate(predicted_answers):
        answers_keyboard.button(text=predicted_answer,
                                callback_data=TestCallback(answer_id=ids).pack()
                                )

        answers_keyboard.adjust(1)
    await state.update_data(current_variants=predicted_answers.copy())

    await callback.message.answer(f"<b>{rand_word}</b>", reply_markup=answers_keyboard.as_markup(),
                                  parse_mode=ParseMode.HTML)
    predicted_answers.clear()

    await state.update_data(right_answer=rand_word_translate, current_word=rand_word)
    await state.set_state(TestStates.waiting_for_answer)

    used_words.append(rand_word)


async def greek_opposites_creation(callback: CallbackQuery, state: FSMContext):
    user_choice = await state.get_data()
    used_words = user_choice.get("used_words", [])

    query = GreekOppositesWords.select()
    if used_words:
        query = query.where(GreekOppositesWords.greek_original.not_in(used_words))

    if query.count() == 0:
        used_words.clear()
        query = GreekOppositesWords.select()

    random_word = query.order_by(fn.Random()).get()
    rand_word = random_word.greek_original
    rand_word_translate = random_word.greek_translated

    predicted_answers = [rand_word_translate]
    random_variants = list(GreekOppositesWords.select().order_by(fn.Random()).limit(5))

    for variant in random_variants:
        if len(predicted_answers) == 3:
            break

        translated_variant = variant.greek_translated
        if translated_variant not in predicted_answers:
            predicted_answers.append(translated_variant)

    print(predicted_answers)
    random.shuffle(predicted_answers)
    print(predicted_answers)

    answers_keyboard = InlineKeyboardBuilder()

    for ids, predicted_answer in enumerate(predicted_answers):
        answers_keyboard.button(text=predicted_answer,
                                callback_data=TestCallback(answer_id=ids).pack()
                                )

        answers_keyboard.adjust(1)
    await state.update_data(current_variants=predicted_answers.copy())

    await callback.message.answer(f"<b>{rand_word}</b>", reply_markup=answers_keyboard.as_markup(),
                                  parse_mode=ParseMode.HTML)
    predicted_answers.clear()

    await state.update_data(right_answer=rand_word_translate, current_word=rand_word)
    await state.set_state(TestStates.waiting_for_answer)

    used_words.append(rand_word)


@router.callback_query(TestStates.waiting_for_answer, TestCallback.filter())
async def get_answer(callback: CallbackQuery, callback_data: TestCallback, state: FSMContext):
    user_choice = await state.get_data()

    right_answer = user_choice.get("right_answer")
    score = user_choice.get("score", 0)
    mistakes = user_choice.get("mistakes", 0)
    total_questions = user_choice.get("total_questions", 0)
    preferred_language = user_choice.get("lang")
    preferred_section = user_choice.get("section")

    used_words = user_choice.get("used_words", [])
    words = user_choice.get("words", [])
    selected_answers = user_choice.get("selected_answers", [])
    right_answers = user_choice.get("right_answers", [])
    current_variants = user_choice.get("current_variants", [])
    all_questions = user_choice.get("all_questions")

    selected_answer_id = callback_data.answer_id
    selected_answer = current_variants[selected_answer_id]
    total_questions += 1

    if selected_answer == right_answer:
        score += 1

    elif selected_answer != right_answer:
        mistakes += 1
        previous_word = user_choice.get("current_word")

        words.append(previous_word)
        selected_answers.append(selected_answer)
        right_answers.append(right_answer)

    await state.update_data(score=score, mistakes=mistakes, total_questions=total_questions, used_words=used_words,
                            words=words, selected_answers=selected_answers, right_answers=right_answers,
                            all_questions=all_questions)

    if total_questions == all_questions:
        used_words.clear()

        await callback.message.answer(f"<blockquote>Результати тесту</blockquote>\n"
                                      f"============================\n"
                                      f"<b>Кількість питань:</b> {total_questions}\n"
                                      f"<b>Правильні відповіді:</b> {score}\n"
                                      f"<b>Неправильні відповіді:</b> {mistakes}",
                                      parse_mode=ParseMode.HTML)

        for a, b, c in zip(words, selected_answers, right_answers):
            await callback.message.answer(f"<blockquote>Розбір помилок</blockquote>\n"
                                          f"===========================\n"
                                          f"<b>Слово:</b> {a}\n"
                                          f"<b>Ваш вибір:</b> {b}\n"
                                          f"<b>Правильний переклад:</b> {c}",
                                          parse_mode=ParseMode.HTML)

        words.clear()
        selected_answers.clear()
        right_answers.clear()

        menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Повторити",
                                                                                    callback_data=f"{all_questions}"
                                                                                    )],
                                                              [InlineKeyboardButton(text="Змінити кількість питань",
                                                                                    callback_data=f"edit_questions_number",
                                                                                    )],
                                                              [InlineKeyboardButton(text="Змінити тематику",
                                                                                    callback_data=f"{preferred_language}_section"
                                                                                    )],
                                                              [InlineKeyboardButton(text="Меню",
                                                                                    callback_data="home")],
                                                              ])

        await callback.message.answer("<blockquote>=== Тест закінчено ===</blockquote>", reply_markup=menu_keyboard,
                                      parse_mode=ParseMode.HTML)

        await state.update_data(score=0, mistakes=0, total_questions=0, used_words=[],
                                words=[], selected_answers=[], right_answers=[])

    else:
        if preferred_language == "greek":
            if preferred_section == "greek_section_1":
                await greek_greetings_creation(callback, state)

            elif preferred_section == "greek_section_2":
                await greek_pronouns_creation(callback, state)

            elif preferred_section == "greek_section_3":
                await greek_colors_creation(callback, state)

            elif preferred_section == "greek_section_4":
                await greek_months_creation(callback, state)

            elif preferred_section == "greek_section_5":
                await greek_nations_creation(callback, state)

            elif preferred_section == "greek_section_6":
                await greek_opposites_creation(callback, state)

    await callback.answer()


@router.callback_query(F.data == "about")
async def about_option(callback: CallbackQuery):
    menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад",
                                                                                callback_data="home")],
                                                          ])

    await callback.message.answer("<blockquote>Про проєкт</blockquote>\n"
                                       "<b>Wordex</b> - це бот, що призначений для вивчення слів різних мов світу.\n"
                                       "\n"
                                       "<blockquote>Про розробника проєкту.</blockquote>\n"
                                       "Крім розробки різноманітних програм, сайтів та онлайн-платформ, "
                                       "я є автором власного блогу з програмування під назвою <b>Magnifique numérique</b>.\n"
                                       "\n"
                                       "<blockquote>Посилання на мої соцмережі, блог і т. д.</blockquote>\n"
                                       "- <a href='https://magnifiquedigitalworld.vercel.app/'>Власний сайт</a>\n"
                                       "- <a href='https://uq2xd.weblium.site'>Блог на Друкарні</a>\n"
                                       "- <a href='https://t.me/learn4prog'>Телеграм канал</a>\n"
                                       "- <a href='https://github.com/testingdifferentfunctions-source'>Github</a>",
                                       parse_mode=ParseMode.HTML, reply_markup=menu_keyboard)


@app.post("/api/webhook")
async def webhook(request: Request):
    update_data = await request.json()
    update = types.Update(**update_data)
    await dp.feed_update(bot=bot, update=update)
    return {"status": 200}