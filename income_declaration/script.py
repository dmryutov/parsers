# -*- coding: utf-8 -*-
"""
@brief:  Extract information from income declarations of officials
@file:   script.py
@author: dmryutov (dmryutov@gmail.com)
@date:   29.03.2017 -- 25.04.2017
"""
import csv


TRANSPORT_TYPE = [
    'автомобиль', 'Автомобиль легковой', 'Автомобиль грузовой', 'Автоприцеп',
    'Мототранспортное средство', 'Водный транспорт', 'Воздушный транспорт',
    'Сельхоз техника', 'Иное'
]
ORG_LIST = {}
PDL_LIST = []
INCOME_LIST = []
ESTATE_LIST = []
TRANSPORT_LIST = []


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
    @return: list (last_name, name, second_name)
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
    return [last_name, name, second_name]


def parse_income(row, owner):
    """
    @brief: Parse income string
    @param row: Input property data
    @param owner: Owner of property
    """
    try:
        amount = float(row[13].strip().replace(' ', '').replace(',', '.'))
        if amount != 0:
            note = row[14].strip()
            INCOME_LIST.append([owner, amount, note])
    except Exception:  # pylint: disable=broad-except
        pass


def parse_estate(row, owner):
    """
    @brief: Parse real estate string
    @param row: Input property data
    @param owner: Owner of property
    """
    # Real estate (own)
    try:
        square = float(row[7].strip().replace(' ', '').replace(',', '.'))
        estate_type = row[5].strip()
        place = row[8].strip()
        note = 'Собственность: ' + row[6].strip()
        ESTATE_LIST.append([owner, estate_type, place, square, note])
    except Exception:  # pylint: disable=broad-except
        pass

    # Real estate (is use)
    try:
        square = float(row[10].strip().replace(' ', '').replace(',', '.'))
        estate_type = row[9].strip()
        place = row[11].strip()
        note = 'В пользовании'
        ESTATE_LIST.append([owner, estate_type, place, square, note])
    except Exception:  # pylint: disable=broad-except
        pass


def parse_transport(row, owner):
    """
    @brief: Parse transport string
    @param row: Input property data
    @param owner: Owner of property
    """
    text = row[12].strip()
    if text != '':
        for transport_type in TRANSPORT_TYPE:
            pos = text.find(transport_type)
            if pos > -1:
                car_type = text[:pos+len(transport_type)].strip()
                car = text[pos+len(transport_type):].strip()
                break
        else:
            car_type = row[12].strip()
            car = ''
        TRANSPORT_LIST.append([owner, car_type, car])

def get_pdl_id(name, pdl_file):
    """
    @brief: Get pdl id
    @param name: Name string
    @param pdl_file: Output pdl file handler
    @return: Pdl id
    """
    try:
        pdl_id = PDL_LIST.index(name) + 1
    except ValueError:
        PDL_LIST.append(name)
        pdl_id = len(PDL_LIST)
        csv_writer(pdl_file).writerow([pdl_id] + parse_name(name))
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
         open('out_transport.csv', 'wb') as transport_file:

        decl_id = 0
        prev_pdl_id = 0
        prev_year = 0

        for i, row in enumerate(csv.reader(input_file, delimiter=';')):
            if i == 0 or not row:
                continue

            decl_year = row[1].strip()
            pdl_org = row[0].strip()
            owner = row[3].strip()

            parse_income(row, owner)
            parse_estate(row, owner)
            parse_transport(row, owner)

            pdl_id = get_pdl_id(row[2], pdl_file)
            # Get declaration id
            if prev_pdl_id != pdl_id or prev_year != decl_year:
                decl_id += 1
                csv_writer(decl_file).writerow([
                    decl_id,
                    pdl_id,
                    decl_year,
                    row[4].replace('  ', ' ').strip(),  # pdl_job
                    pdl_org,
                    ORG_LIST.get(pdl_org, '')
                ])

            write_property(INCOME_LIST, income_file, decl_id)
            write_property(ESTATE_LIST, estate_file, decl_id)
            write_property(TRANSPORT_LIST, transport_file, decl_id)

            prev_pdl_id = pdl_id
            prev_year = decl_year
            del INCOME_LIST[:]
            del ESTATE_LIST[:]
            del TRANSPORT_LIST[:]

            if i % 100 == 0:
                print i


if __name__ == '__main__':
    main()
