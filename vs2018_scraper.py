#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from time import sleep

# Set up Chrome webdriver
chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920x1080')
# Path to your chromedriver here
driver = webdriver.Chrome(executable_path= \
                    "/usr/bin/chromedriver",
                    options=chrome_options)

logging.basicConfig(filename="vs2018_scrape.log", level=logging.INFO, \
                    format="%(asctime)s:%(levelname)s:%(message)s")

driver.get("http://eciresults.nic.in/ConstituencywiseS2653.htm?")

# Build and store lists of states and constituencies
states = []
states_menu = Select(driver.find_element_by_id("ddlState"))
states_options = driver.find_elements_by_xpath \
    ("//select[@id='ddlState']//option[@value!='Select State']")
for option in states_options:
    states.append(option.text)

constituencies = {}

for state in states:
    driver.get("http://eciresults.nic.in/ConstituencywiseS2653.htm?")
    states_menu = Select(driver.find_element_by_id("ddlState"))
    states_menu.select_by_visible_text(state)
    sleep(2)

    const_menu = Select(driver.find_element_by_id("ddlAC"))
    const_options = driver.find_elements_by_xpath \
        ("//select[@id='ddlAC']//option")

    consts = []
    for const in const_options[1:]:
        consts.append(const.get_attribute("value"))

    constituencies[state] = consts

print(constituencies)

# Initialize list of results
results = []

# Iterate through the drop-down menus and scrape results
const_count = 0

for state in constituencies.keys():
    driver.get("http://eciresults.nic.in/ConstituencywiseS2653.htm?")
    states_menu = Select(driver.find_element_by_id("ddlState"))
    states_menu.select_by_visible_text(state)
    print("Now scraping :", state)
    sleep(2)

    try:
        for const in constituencies[state]:
            const_menu = Select(driver.find_element_by_id("ddlAC"))
            for attempt in range(3):
                    try:
                        const_menu.select_by_value(const)
                    except TimeoutException:
                        logging.exception(f"{state} {const} timed out")
                        sleep(5)
                        continue
                    break

            # Parse results table
            results_table = driver.find_elements_by_xpath \
                ("//div[@id='div1']//tr")

            const_name = results_table[0].find_element_by_tag_name('td').text

            # Append constituency id & name, candidate name, party, votes
            for row in results_table[3:-1]:
                data_row=[]
                data_row.append(state)
                data_row.append(const)
                data_row.append(const_name)
                results_data = row.find_elements_by_tag_name('td')
                for item in results_data[0:3]:
                    data_row.append(item.text)
                results.append(data_row)

            logging.info(f"Scraped {state} {const_name}")
            print(f"Scraped {state} {const_name}")
            const_count += 1
            sleep(1)

    except TimeoutException as e:
        logging.exception(f"{state} {const_name} timed out")
        print(f"{state} {const_name} timed out. Sleeping 10 seconds")
        sleep(10)
        continue

    except:
        logging.exception(f"Exception at {state} {const_name}")
        sleep(2)
        continue

    logging.info(f"Finished {state}")
    print("Finished ", state)

print("Scraped " + str(const_count) +"  constituencies")

# Assemble Pandas dataframe
cresults=pd.DataFrame(results, columns=["state", "const_id", \
                                        "const_name", "candidate", "party", \
                                        "votes"])

# Write results to disk
filename = input("Results ready to save. Save as: ")
cresults.to_csv(str(filename) + '.csv', na_rep='.')
print('Results written to disk')
