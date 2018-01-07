# -*- coding: utf-8 -*-
"""
@brief:   Extract judicial acts from `bsr.sudrf.ru` (update database)
@package: judicial
@file:    settings.py
@author:  dmryutov (dmryutov@gmail.com)
@version: 1.0
@date:    03.11.2017 -- 04.11.2017
"""
import re
import os

# Links to all acts
ALL_ACTS = r'https://bsr.sudrf.ru/bigs/portal.html#%7B%22mode%22:%22QUERY_HISTORY%22,%22historyQueryId%22:%22B6A74295-C7E2-4A42-B3A1-CB790A82DB22%22%7D'  # pylint: disable=line-too-long
# Defendant keywords
KEYWORDS = {
    'одсудимого', 'одсудимой', 'одсудимая', 'одсудимый',
    'сужденный', 'сужденная', 'сужденного', 'сужденной', 'сужденого', 'сужденой'
    'суждённый', 'суждённая', 'суждённого', 'суждённой',
    'удимый', 'удимая', 'удимого ранее', 'удимой ранее',
    'бвиняемого', 'бвиняемой', 'бвиняемый', 'бвиняемая',
    'аявителя', 'в отношении'
}
# List of month names
MONTH_LIST = {
    'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа',
    'сентября', 'октября', 'ноября', 'декабря'
}

# Name masks
NAME_MASK = re.compile(r'('+ '|'.join(KEYWORDS) +r')[а-яё]*[ -:]*'+
                       r'(([А-ЯЁ][а-яё]{1,}\s*){3},|'+  # Пахно Денис Геннадьевич,
                       r'([А-ЯЁ][а-яё]{1,}\s*)([А-ЯЁ]\.\s*){1,2}|'+  # Багнюк Д.С.
                       r'([А-ЯЁ]\.\s*){1,2}([А-ЯЁ][а-яё]{1,}\s*)|'+  # Д.С. Багнюк
                       r'([А-ЯЁ]\.\s*){1,3}|'+  # К.Р.Н.
                       r'[А-ЯЁ0-9]{2,})')  # ФИО1
NAME_MASK2 = re.compile(r'(([А-ЯЁ][а-яё]{1,}\s*){3},|'+  # Пахно Денис Геннадьевич,
                        r'([А-ЯЁ][а-яё]{1,}\s*)([А-ЯЁ]\.\s*){1,2}|'+  # Багнюк Д.С.
                        r'([А-ЯЁ]\.\s*){1,2}([А-ЯЁ][а-яё]{1,}\s*)|'+  # Д.С. Багнюк
                        r'([А-ЯЁ]\.\s*){1,3})',  # К.Р.Н.
                        re.I)  # pylint: disable=no-member
FIO_N = re.compile(r'(ФИО|Ф\.И\.О\.)')
NAME_AND_WORD = re.compile(r'^[А-ЯЁ]\. [а-яё]{1,}$')

# Bad words and endings
BAD_ENDINGS = [' по ', ' на ', ',']
BAD_WORDS = {'посредством', 'характеризуется', 'избрана', 'меры', 'возбуждено', 'путем'}
BAD_WORDS2 = {
    'Судебная', 'Преступления совершены', 'Преступление совершено', 'Судья',
    '...', '**', 'по ', 'На основании', 'года. ', 'г. ', 'п. '
}
BAD_WORDS3 = {'ДД.ММ.', 'судья', 'судьей', 'судью', 'судьи'}

# Chrome browser driver path
DRIVER_PATH = os.path.join(os.getcwd(), 'drivers', 'chromedriver')
# Browser loading timeout
TIMEOUT = 20
# Path to database file
DATABASE_PATH = '/Users/dmryutov/Desktop/Judicial/db.sqlite'
# Columns for fast search
FAST_COLUMN_LIST = [
    'old_id',
    'search_number',
    'act_number',
    'instance',
    'article',
    'document_type',
    'region',
    'court_name',
    'result',
    'judge',
    'lawyer',
    'victim_representative',
    'defender',
    'representative',
    'prosecutor',
    'receipt_date',
    'decision_date',
    'entry_date',
    'defendant'
]
# Columns for full search
FULL_COLUMN_LIST = [
    'search_number',
    'act_number',
    'proceedings_type',
    'instance',
    'article',
    'document_type',
    'region',
    'court_name',
    'result',
    'judge',
    'lawyer',
    'claimant',
    'inquirer',
    'debtor',
    'another_participants',
    'interested_person',
    'victim_representative',
    'defender',
    'applicant',
    'plaintiff',
    'public_defender',
    'inquiry',
    'respondent',
    'victim',
    'representative',
    'prosecutor',
    'investigative_body_head',
    'witness',
    'investigator',
    'third_party',
    'document_registration_year',
    'receipt_date',
    'decision_date',
    'entry_date',
    'defendant'
]
