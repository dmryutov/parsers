# -*- coding: utf-8 -*-
"""
@brief:  Clear downloaded data
@file:   clear.py
@author: dmryutov (dmryutov@gmail.com)
@date:   10.05.2017
"""
import csv
import re


KEYWORDS = {
    'одсудимого', 'одсудимой', 'одсудимая', 'одсудимый',
    'сужденный', 'сужденная', 'сужденного', 'сужденной', 'сужденого', 'сужденой'
    'суждённый', 'суждённая', 'суждённого', 'суждённой',
    'удимый', 'удимая', 'удимого ранее', 'удимой ранее',
    'бвиняемого', 'бвиняемой', 'бвиняемый', 'бвиняемая',
    'аявителя', 'в отношении', 'одозреваемого'
}
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
BAD_WORDS = {'посредством', 'характеризуется', 'избрана', 'меры', 'возбуждено', 'путем'}
BAD_WORDS2 = {
    'Судебная', 'Преступления совершены', 'Преступление совершено', 'Судья',
    '...', '**', 'по ', 'На основании', 'года. ', 'г. ', 'п. '
}
BAD_WORDS3 = {'ДД.ММ.', 'судья', 'судьей', 'судью', 'судьи'}


def main():
    """
    @brief: Main function
    """
    with open('act.txt', 'r', encoding='utf8') as input_file, \
         open('act2.txt', 'w', encoding='utf8') as output_file:

        reader = csv.reader(input_file, delimiter=';')
        csv_writer = csv.writer(output_file, delimiter=';', quoting=csv.QUOTE_ALL)
        for i, row in enumerate(reader):
            if i == 0:
                continue

            name = row[-1]

            match = re.search('^[а-я].+?', name)
            if match:
                match2 = NAME_MASK.search(name)
                name = ''
                if match2:
                    name = match2.group(2)

            match = FIO_N.search(name)
            if match:
                name = ''

            match = NAME_AND_WORD.search(name)
            if any(word in name for word in BAD_WORDS) or match:
                name = name.split()[0]

            if any(name.startswith(word) for word in BAD_WORDS2) or \
               any(word in name for word in BAD_WORDS3):
                name = ''

            match = NAME_MASK2.search(name)
            if match and len(match.group(1)) < len(name):
                name = match.group(1)
                if any(name.startswith(word) for word in BAD_WORDS2) or \
                   any(word in name for word in BAD_WORDS3):
                    name = ''

            if len(name) > 150:
                name = ''

            name = ' '.join(name.split())  # Replace multiple spaces

            if name != '':
                csv_writer.writerow(row[:-1]+[name])


if __name__ == '__main__':
    main()
