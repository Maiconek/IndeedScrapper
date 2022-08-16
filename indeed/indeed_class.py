from selenium import webdriver
from selenium.webdriver.common.by import By
from indeed.constants import PATH
import os
import json
import csv
import pandas as pd


class Indeed(webdriver.Chrome):
    def __init__(self, driver_path="C:\Program Files (x86)", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Indeed, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(PATH)

    def get_rid_off_cookies_bar(self):
        cookie = self.find_element(
            By.ID, "onetrust-accept-btn-handler"
        )

        cookie.click()

    def input_job_type(self, job_type):
        job_element = self.find_element(
            By.NAME, "q"
        )

        job_element.send_keys(job_type)

    def input_location(self, location):
        location_element = self.find_element(
            By.NAME, "l"
        )

        location_element.send_keys(location)

    def click_search(self):
        search_element = self.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )

        search_element.click()

    def pull_jobs(self):
        jobs_results_list = self.find_element(
            By.CLASS_NAME, "jobsearch-ResultsList"
        )

        jobs_cards = jobs_results_list.find_elements(
            By.CLASS_NAME, "cardOutline"
        )

        jobs_list = []
        jobs_dict = {'jobs' : []}

        for job in jobs_cards:

            job_name = job.find_element(
                By.CLASS_NAME, "jcs-JobTitle"
            ).find_element(
                By.TAG_NAME, 'span'
            ).get_attribute('innerHTML').strip()

            job_company = job.find_element(
                By.CLASS_NAME, "companyName"
            ).get_attribute('innerHTML').strip()

            if job_company.startswith("<a"):
               job_company = job.find_element(
                   By.CLASS_NAME, "turnstileLink"
               ).get_attribute('innerHTML').strip()

            job_location = job.find_element(
                By.CLASS_NAME, "companyLocation"
            ).get_attribute('innerHTML').strip()


            jobs_list.append([job_name, job_company, job_location])

            jobs_dict['jobs'].append({"title" : job_name, "company": job_company, "location" : job_location})

        return jobs_dict

    def save_to_json(self):
        data = self.pull_jobs()

        with open("data.json", "w") as outfile:
            json.dump(data, outfile, indent=2)

    def save_to_csv(self):
        fieldnames = ["title", "company", "location"]
        data = self.pull_jobs()
        keys = data['jobs']

        with open("jobs.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()

            writer.writerows(keys)

    def print_as_dataframe(self):
        data = self.pull_jobs()
        results = pd.DataFrame(data['jobs'])
        print(results)