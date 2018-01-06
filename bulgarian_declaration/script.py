# -*- coding: utf-8 -*-
"""
@brief:   Converter bulgarian declarations to SQL queries (Oracle)
@package: declaration2sql
@file:    declaration2sql.py
@author:  dmryutov (dmryutov@gmail.com)
@version: 1.1
@date:    16.11.2017 -- 06.01.2018
"""
import datetime
import os
import re

from lxml import etree


MONTH = {
    'январь': '01',
    'февраль': '02',
    'март': '03',
    'апрель': '04',
    'май': '05',
    'июнь': '06',
    'июль': '07',
    'август': '08',
    'сентябрь': '09',
    'октябрь': '10',
    'ноябрь': '11',
    'декабрь': '12'
}

TABLE1 = [
    'vid_sobstvennosti',
    'mesto',
    'administrativnyi_center',
    'ploschad',
    'ploshad_stroenia',
    'god_priobretenia',
    'fio_sobstvennika',
    'dolya_sobstvennosti',
    'stoimost',
    'pravo_na_priobretenie',
    'proishozhdenie_ds',
    'type'
]
TABLE2 = [
    'vid_sobstvennosti',
    'mesto',
    'administrativnyi_center',
    'ploschad',
    'ploshad_stroenia',
    'fio_sobstvennika',
    'dolya_sobstvennosti',
    'stoimost',
    'pravo_na_priobretenie',
    'type'
]
TABLE3 = [
    'vid',
    'marka',
    'stoimost',
    'god_priobretenia',
    'fio_sobstvennika',
    'dolya_sobstvennosti',
    'pravo_na_priobretenie',
    'proishozhdenie_ds',
    'type'
]
TABLE5 = [
    'vid',
    'marka',
    'stoimost',
    'fio_sobstvennika',
    'dolya_sobstvennosti',
    'pravo_na_priobretenie',
    'type'
]
TABLE6 = [
    'summa',
    'valuta',
    'ekvivalent',
    'fio_sobstvennika',
    'proishozhdenie_ds'
]
TABLE7 = [
    'summa',
    'valuta',
    'ekvivalent',
    'fio_sobstvennika',
    'v_strane',
    'vne_strany',
    'proishozhdenie_ds'
]
TABLE8 = [
    'vid_zadolzhennosti',
    'summa',
    'valuta',
    'ekvivalent',
    'fio_sobstvennika',
    'pravovoe_obosnovanie',
    'ot_grazhdanina_bolgarii',
    'ot_inostrannogo_grazdanina'
]
TABLE9 = [
    'vid_zadolzhennosti',
    'summa',
    'valuta',
    'ekvivalent',
    'fio_sobstvennika',
    'pravovoe_obosnovanie',
    'naimenovanie_banka',
    'drugoi_kreditor'
]
TABLE10 = [
    'vid',
    'nomer',
    'cb',
    'ekvivalent',
    'emitent',
    'summa',
    'fio_sobstvennika',
    'pravovoe_obosnovanie',
    'proishozhdenie_ds'
]
TABLE11 = [
    'vid',
    'dolevoe_uchastie',
    'organizacia',
    'mesto',
    'stoimost',
    'fio_sobstvennika',
    'pravovoe_obosnovanie',
    'proishozhdenie_ds',
    'type'
]
TABLE12 = [
    'vid',
    'dolevoe_uchastie',
    'organizacia',
    'mesto',
    'stoimost',
    'fio_sobstvennika',
    'pravovoe_obosnovanie',
    'type'
]
TABLE13 = [
    'vid',
    'declarant',
    'suprug'
]
TABLE14 = [
    'vid',
    'summa',
    'valuta',
    'ekvivalent',
    'ot_supruga',
    'suprugu',
    'type'
]
TABLE15 = [
    'vid',
    'summa',
    'valuta',
    'ekvivalent',
    'ot_declaranta',
    'declarantu',
    'ot_supruga',
    'suprugu',
    'type'
]


def insert_query(table, fields, values):
    """
    @brief: Build `INSERT` query
    @param table: Table name
    @param fields: Table fields
    @param values: Cell values
    @return: `INSERT` query
    @since: 1.0
    """
    return "    INSERT INTO {} ({}) VALUES ({});\n".format(table, ', '.join(fields),
                                                           ', '.join(values))


def process_table(decl_id, table, name, fields, extra=[]):  # pylint: disable=dangerous-default-value
    """
    @brief: Build `INSERT` query
    @param decl_id: Declaration id
    @param table: Table XML-node
    @param name: Table name
    @param fields: Table fields
    @param extra: Extra cell values
    @return: `INSERT` query
    @since: 1.0
    """
    query = ''
    if table.get('Declared') == 'True':
        for row in table:
            values = [prepare_value(val.text, fields[i]) for i, val in enumerate(row[1:])]
            # Check if line is not empty ('NULL')
            if values != ['NULL'] * len(values):
                query += insert_query(name, ['id', 'decl_id'] + fields,
                                      ['id_seq.NEXTVAL', decl_id] + values + extra)
    return query


def is_date(input_str, fmt):
    """
    @brief: Check if str is date in format `dd.mm.yyyy`
    @param input_str: Input string
    @return: True if string is date
    @since: 1.0
    """
    try:
        datetime.datetime.strptime(input_str, fmt)
        return True
    except ValueError:
        return False


def prepare_value(value, field=None):
    """
    @brief: Prepare cell value
    @param value: Input value
    @param field: Field name
    @return: Clean cell value
    @since: 1.0
    """
    if field in ['summa', 'stoimost', 'ekvivalent', 'ploschad', 'ploshad_stroenia',
                 'declarant', 'suprug', 'year', 'god_priobretenia']:
        number = re.findall(r'\d+', str(value).replace(' ', ''))
        value = number[0] if number else ''

    """elif is_date(value, '%d.%m.%Y'):
        return "TO_DATE('{}', 'dd.mm.yyyy')".format(value)
    elif is_date(value, '%d,%m,%Y'):
        return "TO_DATE('{}', 'dd,mm,yyyy')".format(value)
    elif is_date(value, '%d/%m/%Y'):
        return "TO_DATE('{}', 'dd/mm/yyyy')".format(value)
    elif is_date(value, '%d-%m-%Y'):
        return "TO_DATE('{}', 'dd-mm-yyyy')".format(value)
    elif is_date(value, '%d.%m%Y'):
        return "TO_DATE('{}', 'dd.mmyyyy')".format(value)
    elif is_date(value, '%d%m.%Y'):
        return "TO_DATE('{}', 'ddmm.yyyy')".format(value)
    elif is_date(value, '%d.%m.%Yг.'):
        return "TO_DATE('{}', 'dd.mm.yyyy')".format(value[:-2])
    elif is_date(value, '%d.%m.%Yг'):
        return "TO_DATE('{}', 'dd.mm.yyyy')".format(value[:-1])
    elif is_date(value, '%d.%m.%y'):
        return "TO_DATE('{}', 'dd.mm.yy')".format(value)
    elif value[2:-4] in MONTH:
        value = value[0:2] +'.'+ MONTH[value[2:-4]] +'.'+ value[-4:]
        return "TO_DATE('{}', 'dd.mm.yyyy')".format(value)
    elif is_date(value[:-1] +'1'+ value[-1], '%d.%m.%Y'):
        return "TO_DATE('{}', 'dd.mm.yyyy')".format(value[:-1] +'1'+ value[-1])
    elif is_date(value[:-1], '%d.%m.%Y'):
        return "TO_DATE('{}', 'dd.mm.yyyy')".format(value[:-1])"""  # pylint: disable=pointless-string-statement

    if value is None or value == '':
        return 'NULL'
    value = str(value).replace('\n', ' ').replace('\r', ' ').replace("'", '"') \
                      .replace(';', ',').strip()
    return "'"+ value +"'"


def proc_begin(output_file):
    """
    @brief: Generate function block begining
    @param output_file: Output file handler
    @since: 1.0
    """
    output_file.write('DECLARE cnt NUMBER(11,0); BEGIN\n\n')


def proc_end(output_file):
    """
    @brief: Generate function block ending
    @param output_file: Output file handler
    @since: 1.0
    """
    output_file.write('END;')


def extract_person_info(tree):
    """
    @brief: Extract person information and generate queries
    @param tree: XML-tree
    @return: Queries, Person ID subquery
    @since: 1.0
    """
    data = {}
    query = ''
    person_name = work_code = 'NULL'
    for node in tree.xpath('//Personal')[0]:
        if not node.text or node.text.strip() == '':
            continue
        elif node.tag == 'Name':
            data['name'] = node.text
            person_name = node.text
        elif node.tag == 'Work':
            data['work'] = node.text
        elif node.tag == 'Position':
            data['position'] = node.text
        elif node.tag == 'WorkCode':
            data['work_code'] = node.text
            work_code = node.text
        elif node.tag == 'EGN':
            data['egn'] = node.text
        elif node.tag == 'PassportNumber':
            data['passport_number'] = node.text
        elif node.tag == 'PassportData':
            data['passport_data'] = node.text
        elif node.tag == 'Address':
            data['address'] = node.text

    query += "SELECT COUNT(1) INTO cnt FROM person WHERE name = '{}' AND work_code = '{}';\n" \
                .format(person_name, work_code)
    query += "IF cnt = 0 THEN\n"
    query += insert_query('person',
                          ['id'] + [key for key in data],
                          ['id_seq.NEXTVAL'] + [prepare_value(val) for val in data.values()])
    query += "END IF;\n"
    person_id = "(SELECT id FROM person WHERE name = '{}' AND work_code = '{}' AND ROWNUM = 1)" \
                    .format(person_name, work_code)

    return query, person_id


def extract_declaration_info(tree, person_id):
    """
    @brief: Extract person information and generate queries
    @param tree: XML-tree
    @param person_id: Person ID subquery
    @return: Queries, Declaration ID subquery
    @since: 1.0
    """
    data = {}
    query = ''
    control_hash = 'NULL'
    for node in tree.xpath('//DeclarationData')[0]:
        if not node.text or node.text.strip() == '':
            continue
        elif node.tag == 'EntryNumber':
            data['entry_number'] = node.text
        elif node.tag == 'EntryDate':
            data['entry_date'] = node.text.replace(' ', '')
        elif node.tag == 'DeclarationType':
            data['declaration_type'] = node.text
        elif node.tag == 'Year':
            data['year'] = node.text
        elif node.tag == 'DeclarationDate':
            data['declaration_date'] = node.text.replace(' ', '')
        elif node.tag == 'AgreementDate':
            data['agreement_date'] = node.text.replace(' ', '')
        elif node.tag == 'ControlHash':
            data['control_hash'] = node.text
            control_hash = node.text

    query += ("SELECT COUNT(1) INTO cnt FROM declaration WHERE person_id = {} "
              "AND control_hash = '{}';\n").format(person_id, control_hash)
    query += "IF cnt = 0 THEN\n"
    query += insert_query('declaration',
                          ['id', 'person_id'] + [key for key in data],
                          ['id_seq.NEXTVAL', person_id] + \
                          [prepare_value(val) for val in data.values()])
    decl_id = ("(SELECT id FROM declaration WHERE person_id = {} "
               "AND control_hash = '{}' AND ROWNUM = 1)").format(person_id, control_hash)

    return query, decl_id


def process_file(output_file, file_name):
    """
    @brief: Process file and generate queries
    @param output_file: Output file handler
    @param file_name: Input file name
    @since: 1.0
    """
    # Write file name as title
    output_file.write('/** ' + file_name + ' **/\n')
    proc_begin(output_file)

    # Load file
    tree = etree.parse(file_name).getroot()  # pylint: disable=no-member
    tables = tree.xpath('//Tables')[0]

    # Person info
    person_query, person_id = extract_person_info(tree)

    # Declaration info
    decl_query, decl_id = extract_declaration_info(tree, person_id)

    # Table data
    query = person_query + decl_query
    query += process_table(decl_id, tables[0], 'nedvizhimoe_imuschestvo', TABLE1, ['0'])  # 1
    query += process_table(decl_id, tables[1], 'nedvizhimoe_imuschestvo', TABLE1, ['1'])  # 1.1
    query += process_table(decl_id, tables[2], 'nedvizhimoe_imuschestvo', TABLE2, ['2'])  # 2
    query += process_table(decl_id, tables[3], 'transport', TABLE3, ['0'])  # 3
    query += process_table(decl_id, tables[4], 'transport', TABLE3, ['1'])  # 3.1
    query += process_table(decl_id, tables[5], 'transport', TABLE3, ['2'])  # 4
    query += process_table(decl_id, tables[6], 'transport', TABLE5, ['3'])  # 5
    query += process_table(decl_id, tables[7], 'nalichnie_ds', TABLE6)  # 6
    query += process_table(decl_id, tables[8], 'bankovskie_depozity', TABLE7)  # 7
    query += process_table(decl_id, tables[9], 'debitorskay_zadolzhnost', TABLE8)  # 8
    query += process_table(decl_id, tables[10], 'kreditorskay_zadolzhnost', TABLE9)  # 9
    query += process_table(decl_id, tables[11], 'akcii', TABLE10)  # 10
    query += process_table(decl_id, tables[12], 'doli_v_ooo', TABLE11, ['0'])  # 11
    query += process_table(decl_id, tables[13], 'doli_v_ooo', TABLE12, ['1'])  # 12
    query += process_table(decl_id, tables[14], 'dohody_ne_ot_zp', TABLE13)  # 13
    query += process_table(decl_id, tables[15], 'ds_v_polzu_declaranta', TABLE14, ['0'])  # 14
    query += process_table(decl_id, tables[16], 'ds_v_polzu_declaranta', TABLE15, ['1'])  # 15

    query += "END IF;\n"

    # Write result
    output_file.write(query + '\n')
    output_file.write('END;\n/\n\n')


def main():
    """
    @brief: Main function
    @since: 1.0
    """
    input_dir = input('Input directory path: ')
    output_file = input('Output file name (without extension): ')
    output_file = open(output_file + '.sql', mode='w', encoding='utf-8')

    #proc_begin(output_file)

    file_count = 0
    for root, _, files in os.walk(input_dir):
        for name in files:
            name = os.path.join(root, name)
            if name.lower().endswith('.xml'):
                if file_count > 0 and file_count % 100 == 0:
                    print(file_count)
                #print(name)
                process_file(output_file, name)
                file_count += 1

    print('Processed files: %d' % file_count)
    #proc_end(output_file)
    output_file.close()


if __name__ == '__main__':
    main()
    input("Press Enter to exit...")
