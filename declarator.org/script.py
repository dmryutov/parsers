# -*- coding: utf-8 -*-
"""
@brief:  Extract information from income declarations of officials from `declarator.org`
@file:   script.py
@author: dmryutov (dmryutov@gmail.com)
@date:   29.03.2017 -- 10.04.2017
"""
import csv
import re


PROPERTY_PARSER = {
    1: parse_income,
    2: parse_estate,
    3: parse_transport,
    4: parse_account,
    5: parse_stocks
}
ITEM_TYPE_LIST = {
    'Доход': 1,
    'Недвижимое имущество': 2,
    'Транспортные средства': 3,
    'Счета': 4,
    'Акции и ценные бумаги': 5
}
ORG_LIST = {}
PDL_LIST = []
INCOME_LIST = []
ESTATE_LIST = []
TRANSPORT_LIST = []
ACCOUNT_LIST = []
STOCKS_LIST = []


def load_organization_list():
    """
    @brief: Load list of organizations with links
    """
    with open('authority_links.txt', 'rb') as org_file:
        for line in org_file:
            key, value = line.split('||')
            ORG_LIST[key] = value.strip()
    return ORG_LIST


def parse_name(text):
    """
    @brief: Explode name string
    @param text: Input name string
    @return: tuple (last_name, name, second_name)
    """
    elements = text.split(' ')
    if len(elements) == 3:
        last_name, name, second_name = elements
    elif len(elements) == 2:
        last_name, name = elements
        if name.find('.') > -1:
            elements = name.split('.')
            second_name = elements[1] + '.'
            name = elements[0] + '.'
        else:
            second_name = name
            name = ''
    else:
        last_name, old_name, name, second_name = elements
        if old_name[0] == '(':
            last_name += ' ' + old_name
        elif second_name.lower() == 'оглы':
            second_name = name + ' ' + second_name
        else:
            name = old_name + ' ' + name
    return last_name, name, second_name


def parse_income(text, owner):
    """
    @brief: Parse income string
    @param text: Input property data
    @param owner: Owner of property
    """
    pos = text.find(':') if (text.find(':') < text.find('руб.')) else -1
    owner = text[:pos].strip() if (pos > -1) else ''
    pos = pos+1 if (pos > -1) else 0
    pos2 = text.find('. (')
    amount = text[pos:pos2-6].replace(' ', '').replace(',', '.')
    pos2 = pos2+3 if (pos2 > -1) else len(text)
    note = text[pos2:-1].strip()
    INCOME_LIST.append([owner, amount, note])


def parse_estate(text, owner):
    """
    @brief: Parse real estate string
    @param text: Input property data
    @param owner: Owner of property
    """
    pos = text.find(':')
    owner = text[:pos] if (pos > -1) else ''
    pos = pos+1 if (pos > -1) else 0

    match = re.search(r', ([0-9]+(?:|\.[0-9]+) кв\.)', text[pos+1:])
    square = match.group(1) if match else ''
    pos3 = text.find(square)
    estate_type = text[pos:pos3].strip()[:-1]

    match = re.search(u', ([А-ЯЁ].+)', estate_type.decode('utf8'))
    place = ''
    if match:
        place = match.group(1).encode('utf8')
        estate_type = estate_type[:estate_type.find(place) - 2]

    pos3 = pos + 2 if pos3 < 0 else pos3 + len(square) + 4
    note = text[pos3:].strip()
    if square == '' and estate_type == '':
        note = text
    if note and note[0] == '(':
        note = note[1:-1]
    square = square[:-5].replace(' ', '').replace(',', '.')
    ESTATE_LIST.append([owner, estate_type, place, square, note])


def parse_transport(text, owner):
    """
    @brief: Parse transport string
    @param text: Input property data
    @param owner: Owner of property
    """
    pos = text.find(':') if (text.find(':') < text.find(',')) else -1
    owner = text[:pos] if (pos > -1) else ''
    pos = pos+1 if (pos > -1) else 0
    pos2 = text.find(',')
    car_type = text[pos:pos2].strip()
    car = text[pos2+1:].strip()
    TRANSPORT_LIST.append([owner, car_type, car])


def parse_account(text, owner):
    """
    @brief: Parse account string
    @param text: Input property data
    @param owner: Owner of property
    """
    pos = text.find(':')
    owner = text[:pos] if (pos > -1) else ''
    pos2 = text.find('. (')
    amount = text[pos+1:pos2-6].replace(' ', '').replace(',', '.')
    pos2 = pos2+3 if (pos > -1) else len(text)
    org = text[pos2:-1].strip()
    ACCOUNT_LIST.append([owner, amount, org])


def parse_stocks(text, owner):
    """
    @brief: Parse stocks string
    @param text: Input property data
    @param owner: Owner of property
    """
    pos = text.find(':')
    owner = text[:pos] if (pos > -1) else ''
    pos2 = text[pos+1:].strip().split(' ')
    amount = pos2[0].strip().replace(',', '.')
    unit = pos2[1].strip() if len(pos2) > 1 else ''

    org = ' '.join(pos2[2:]).strip()
    STOCKS_LIST.append([owner, amount, unit, org])


def get_pdl_id(name, pdl_file, pdl_link):
    """
    @brief: Get pdl id
    @param name: Name string
    @param pdl_file: Output pdl file handler
    @param pdl_link: Link to pdl page
    @return: Pdl id
    """
    try:
        pdl_id = PDL_LIST.index(name) + 1
    except ValueError:
        PDL_LIST.append(name)
        pdl_id = len(PDL_LIST)
        csv_writer(pdl_file).writerow([pdl_id] + parse_name(name) + [pdl_link])
    return pdl_id


def csv_writer(output_file):
    """
    @brief: Get CSV writer
    @param output_file: Output file handler
    @return: CSV writer
    """
    return csv.writer(output_file, delimiter=';', quoting=csv.QUOTE_ALL)


def write_property(row_list, output_file, decl_id):
    """
    @brief: Write property row to CSV file
    @param row_list: List of rows which should be written to file
    @param output_file: Output file handler
    @param decl_id: Declaration id
    """
    for item in row_list:
        csv_writer(output_file).writerow([decl_id] + item)


def main():
    """
    @brief: Main function
    """
    load_organization_list()

    with open('example/declarations.csv', 'rb') as input_file, \
         open('out_pdl.csv', 'wb') as pdl_file, \
         open('out_decl.csv', 'wb') as decl_file, \
         open('out_income.csv', 'wb') as income_file, \
         open('out_estate.csv', 'wb') as estate_file, \
         open('out_transport.csv', 'wb') as transport_file, \
         open('out_accounts.csv', 'wb') as accounts_file, \
         open('out_stocks.csv', 'wb') as stocks_file:

        for i, row in enumerate(csv.reader(input_file, delimiter=';')):
            if i == 0 or len(row) < 4:
                continue

            offset = int(len(row) >= 7)

            item_type = 0
            for item in row[1].split(' |'):
                text = item.strip()
                if text == '':
                    continue
                if text in ITEM_TYPE_LIST:
                    item_type = ITEM_TYPE_LIST[text]
                    continue

                pos = text.find(':') if (text.find(':') < text.find('руб.')) else -1
                PROPERTY_PARSER[item_type](text, text[:pos] if (pos > -1) else '')

            csv_writer(decl_file).writerow([
                i,  # decl_id
                get_pdl_id(row[0], pdl_file, row[5 + offset]),  # pdl_id
                row[2],  # decl_year
                row[4 + offset],  # decl_type
                '' if len(row) < 7 else row[3],  # pdl_job
                row[3 + offset],  # pdl_org
                ORG_LIST.get(row[3 + offset], '')
            ])

            write_property(INCOME_LIST, income_file, i)
            write_property(ESTATE_LIST, estate_file, i)
            write_property(TRANSPORT_LIST, transport_file, i)
            write_property(ACCOUNT_LIST, accounts_file, i)
            write_property(STOCKS_LIST, stocks_file, i)

            if i % 100 == 0:
                print i

if __name__ == '__main__':
    main()
