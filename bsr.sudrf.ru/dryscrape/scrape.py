# -*- coding: utf-8 -*-
"""
@brief:  Extract judicial acts from `bsr.sudrf.ru`
@file:   scrape.py
@author: dmryutov (dmryutov@gmail.com)
@date:   23.04.2017 -- 29.04.2017
"""
import csv
import os
import sys

import dryscrape
from lxml import html

import settings

def find_name(elements):
    """
    @brief: Find name of law offender in document
    @param elements: Document paragraphs
    @return: Name of law offender
    """
    name = ''
    for j in range(len(elements) - 1):
        try:
            text = elements[j].text_content() + ' ' + elements[j+1].text_content()
            match = settings.NAME_MASK.search(text)
            if match:
                name = match.group(2)
                for ending in settings.BAD_ENDINGS:
                    if name.endswith(ending):
                        name = name[:-1 * len(ending)]
                name = name.strip()
                if name in settings.MONTH_LIST:
                    name = text[:text.index(',')]
                name = name.strip()
                break
        except Exception:  # pylint: disable=broad-except
            name = ''
    return name


def extract_acts(site):
    """
    @brief: Extract acts content to csv file
    @param site: First site in search result
    @note: Requires webkit_server (Unix only)
    """
    # Start webkit server and session
    if 'linux' in sys.platform:
        dryscrape.start_xvfb()
    sess = dryscrape.Session()
    # Load site
    sess.visit(site)

    csv_exists = os.path.exists(settings.CSV_PATH)
    with open(settings.CSV_PATH, 'a', encoding='utf8') as output_file:
        csv_writer = csv.writer(output_file, delimiter=';', quoting=csv.QUOTE_ALL)
        if not csv_exists:
            csv_writer.writerow(settings.HEADERS)

        i = 1
        prev_progress = ''
        # Iterate while "Next" button is enabled
        while True:
            try:
                progress = sess.wait_for(lambda: sess.at_css('.text.result-counter')).text()
                if prev_progress == progress:
                    continue

                row = [i]
                elements = sess.wait_for(lambda: sess.css('.docValue'))
                # Iterate through all fields except last one (34 - 1 = 33)
                for element in elements[:33]:
                    text = element.text().strip()
                    row.append(text if text != 'Не заполнено' else '')

                frame = sess.eval_script("$('.field-iframe').contents().find('body').html();")
                try:
                    tree = html.fromstring(frame)
                    elements = tree.xpath('//p')
                except Exception:  # pylint: disable=broad-except
                    elements = []

                row.append(find_name(elements))

                csv_writer.writerow(row)
                prev_progress = progress
                print(i)
                i += 1

                button = sess.wait_for(lambda: sess.at_css('.card-paginator .to-right-red'))
                if 'yui-button-disabled' in button['class']:
                    break
                button.children()[0].click()
            except dryscrape.mixins.WaitTimeoutError:
                sess.exec_script('location.reload();')
            except Exception:  # pylint: disable=broad-except
                continue


def main():
    """
    @brief: Main function
    """
    for _, site in settings.FIRST_ACT.items():
        extract_acts(site)


if __name__ == '__main__':
    main()
