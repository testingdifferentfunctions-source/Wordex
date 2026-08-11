from peewee import *

db = SqliteDatabase("api/database.db")


class EnglishAnimalsWords(Model):
    english_original = CharField()
    english_translated = CharField()

    class Meta:
        database = db
#
#
# class FrenchWords(Model):
#     french_original = CharField()
#     french_translated = CharField()
#
#     class Meta:
#         database = db
#
#
# class GermanWords(Model):
#     german_original = CharField()
#     german_translated = CharField()
#
#     class Meta:
#         database = db
#
#
# class SpanishWords(Model):
#     spanish_original = CharField()
#     spanish_translated = CharField()
#
#     class Meta:
#         database = db
#
#
# class PortugueseWords(Model):
#     spanish_original = CharField()
#     spanish_translated = CharField()
#
#     class Meta:
#         database = db

class GreekGreetingsWords(Model):
    greek_original = CharField()
    greek_translated = CharField()

    class Meta:
        database = db


class GreekPronounsWords(Model):
    greek_original = CharField()
    greek_translated = CharField()

    class Meta:
        database = db


class GreekColorsWords(Model):
    greek_original = CharField()
    greek_translated = CharField()

    class Meta:
        database = db


class GreekMonthsWords(Model):
    greek_original = CharField()
    greek_translated = CharField()

    class Meta:
        database = db


class GreekNationalitiesWords(Model):
    greek_original = CharField()
    greek_translated = CharField()

    class Meta:
        database = db


class GreekOppositesWords(Model):
    greek_original = CharField()
    greek_translated = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([EnglishAnimalsWords], safe=True)


# if GreekGreetingsWords.select().count() == 0:
#     for greek_word, greek_translation in greek_greetings_dict.items():
#         english_row = GreekGreetingsWords(greek_original=greek_word, greek_translated=greek_translation)
#         english_row.save()
#
# elif GreekPronounsWords.select().count() == 0:
#     for greek_word, greek_translation in greek_pronouns_dict.items():
#         english_row = GreekPronounsWords(greek_original=greek_word, greek_translated=greek_translation)
#         english_row.save()
#
# elif GreekColorsWords.select().count() == 0:
#     for greek_word, greek_translation in greek_colors_dict.items():
#         english_row = GreekColorsWords(greek_original=greek_word, greek_translated=greek_translation)
#         english_row.save()
#
# elif GreekMonthsWords.select().count() == 0:
#     for greek_word, greek_translation in greek_months_dict.items():
#         english_row = GreekMonthsWords(greek_original=greek_word, greek_translated=greek_translation)
#         english_row.save()
#
# elif GreekNationalitiesWords.select().count() == 0:
#     for greek_word, greek_translation in greek_nationalities_dict.items():
#         english_row = GreekNationalitiesWords(greek_original=greek_word, greek_translated=greek_translation)
#         english_row.save()
#
# elif GreekOppositesWords.select().count() == 0:
#     for greek_word, greek_translation in greek_opposites_dict.items():
#         english_row = GreekOppositesWords(greek_original=greek_word, greek_translated=greek_translation)
#         english_row.save()

# if EnglishAnimalsWords.select().count() == 0:
#     for english_word, english_translation in english_animals_dict.items():
#         english_row = EnglishAnimalsWords(english_original=english_word, english_translated=english_translation)
#         english_row.save()

print("Created!")
db.close()
