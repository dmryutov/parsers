# -*- coding: utf-8 -*-
"""
@brief:   Extract judicial acts from `bsr.sudrf.ru` (update database)
@package: judicial
@file:    update.py
@author:  dmryutov (dmryutov@gmail.com)
@version: 1.0
@date:    03.11.2017 -- 04.11.2017
"""
import re
import sqlite3

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException

import update_settings as settings


def convert_date(date):
    """
    @brief: Convert date format from `dd.mm.yyyy` to `yyyy-mm-dd`
    @param date: Input date
    @return: Date in new format
    @since: 1.0
    """
    return date[6:] +'-'+ date[3:5] +'-'+ date[:2]


def find_name(elements):
    """
    @brief: Find name of law offender in document
    @param elements: Document paragraphs
    @return: Name of law offender
    @since: 1.0
    """
    name = ''
    for j in range(len(elements) - 1):
        try:
            text = elements[j].text + ' ' + elements[j+1].text
            match = settings.NAME_MASK.search(text)
            if match:
                name = match.group(2)
                for ending in settings.BAD_ENDINGS:
                    if name.endswith(ending):
                        name = name[:-1 * len(ending)]
                name = name.strip()
                if name in settings.MONTH_LIST:
                    name = text[:text.index(',')].strip()
                break
        except Exception:  # pylint: disable=broad-except
            name = ''
    return name


def clear_name(name):
    """
    @brief: Clear defendant name
    @param name: Degendant name
    @return: Clean name
    @since: 1.0
    """
    match = re.search('^[а-я].+?', name)
    if match:
        match2 = settings.NAME_MASK.search(name)
        name = ''
        if match2:
            name = match2.group(2)

    match = settings.FIO_N.search(name)
    if match:
        name = ''

    match = settings.NAME_AND_WORD.search(name)
    if any(word in name for word in settings.BAD_WORDS) or match:
        name = name.split()[0]

    if any(name.startswith(word) for word in settings.BAD_WORDS2) or \
       any(word in name for word in settings.BAD_WORDS3):
        name = ''

    match = settings.NAME_MASK2.search(name)
    if match and len(match.group(1)) < len(name):
        name = match.group(1)
        if any(name.startswith(word) for word in settings.BAD_WORDS2) or \
           any(word in name for word in settings.BAD_WORDS3):
            name = ''

    if len(name) > 150:
        name = ''

    name = ' '.join(name.split())  # Replace multiple spaces
    return name


def extract_new_links(browser, cursor):
    """
    @brief: Extract links to new acts
    @param browser: Browser handler
    @param cursor: Database connection cursor
    @return: Links to new acts
    @since: 1.0
    """
    print('Searching new acts...')
    # Load site
    browser.get(settings.ALL_ACTS)

    i = 0
    links = set()
    prev_progress = ''
    # Iterate while "Next" button is enabled
    while True:
        try:
            progress = browser.find_element_by_css_selector('#bottomResultCountOuter') \
                              .text.encode()
            if prev_progress == progress:
                continue

            acts = browser.find_elements_by_class_name('resultOuter')
            for act in acts:
                link = act.find_element_by_class_name('openCardLink')
                href = link.get_attribute('href')
                fields = act.find_elements_by_class_name('additional-field-value')
                try:
                    res = cursor.execute(("SELECT EXISTS ("
                                          "SELECT 1 FROM dirty WHERE "
                                          "act_number = ? AND "
                                          "document_type = ? AND "
                                          "receipt_date = ? AND "
                                          "decision_date = ? AND "
                                          "region = ? AND "
                                          "court_name = ? AND "
                                          "result = ? "
                                          "LIMIT 1"
                                          ");"), (
                                              link.text[15:],
                                              fields[0].text,
                                              convert_date(fields[1].text),
                                              convert_date(fields[2].text),
                                              fields[3].text,
                                              fields[4].text,
                                              fields[5].text))
                    if not res.fetchone()[0]:
                        links.add(href)
                except IndexError:
                    pass

            i += 1
            prev_progress = progress
            print('Page:', i)

            button = browser.find_element_by_css_selector('#pager .nextPage')
            if 'disablePage' in button.get_attribute('class'):
                break
            button.click()
        except StaleElementReferenceException:
            pass
        except Exception:  # pylint: disable=broad-except
            browser.refresh()

    print('NEW ACTS:', len(links))
    return links


def extract_acts(browser, connection, cursor, links):
    """
    @brief: Extract acts content to database
    @param browser: Browser handler
    @param connection: Database handler
    @param cursor: Database connection cursor
    @param links: Links to new acts
    @return: List of links to new acts
    @since: 1.0
    """
    print('Extracting acts...')
    for i, link in enumerate(links):
        # Load site
        browser.get(link)
        browser.refresh()

        # Iterate while "Next" button is enabled
        try:
            values = [i]
            elements = browser.find_elements_by_class_name('docValue')
            # Iterate through all fields except last one (34 - 1 = 33)
            for element in elements[:33]:
                values.append(element.text)

            # You have to switch to the iframe like so
            frame = browser.find_element_by_class_name('field-iframe')
            browser.switch_to_frame(frame)

            elements = browser.find_elements_by_tag_name('p')
            values.append(find_name(elements))

            # Insert record into tables
            cursor.execute(("INSERT INTO dirty "
                            "("+ ','.join(settings.FULL_COLUMN_LIST) +")"
                            " VALUES "
                            "("+ ','.join('?' * len(settings.FULL_COLUMN_LIST)) +")"), values)
            name = clear_name(values[34])
            if name != '':
                cursor.execute(("INSERT INTO clean "
                                "("+ ','.join(settings.FAST_COLUMN_LIST) +")"
                                " VALUES "
                                "("+ ','.join('?' * len(settings.FAST_COLUMN_LIST)) +")"), (
                                    cursor.lastrowid,  # old_id
                                    i,          # search_number
                                    values[1],  # act_number
                                    values[3],  # instance
                                    values[4],  # article
                                    values[5],  # document_type
                                    values[6],  # region
                                    values[7],  # court_name
                                    values[8],  # result
                                    values[9],  # judge
                                    values[10], # lawyer
                                    values[16], # victim_representative
                                    values[17], # defender
                                    values[24], # representative
                                    values[25], # prosecutor
                                    values[31], # receipt_date
                                    values[32], # decision_date
                                    values[33], # entry_date
                                    name        # defendant
                                ))
            connection.commit()
            print('Act:', i+1)
        except Exception:  # pylint: disable=broad-except
            pass
    print('Done!')


def main():
    """
    @brief: Main function
    @since: 1.0
    """
    # Initialize driver connection
    browser = webdriver.Chrome(executable_path=settings.DRIVER_PATH)
    browser.implicitly_wait(settings.TIMEOUT)
    # Initialize database connection
    connection = sqlite3.connect(settings.DATABASE_PATH)
    cursor = connection.cursor()

    # Extract new links and acts
    links = extract_new_links(browser, cursor)
    extract_acts(browser, connection, cursor, links)

    # Close all connections
    browser.close()
    browser.quit()
    connection.close()


if __name__ == '__main__':
    main()
