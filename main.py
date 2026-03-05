from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random 
# 263 pages for internships
# link for just paid internships: https://ucla.joinhandshake.com/job-search/10812441?jobType=3&pay%5BsalaryType%5D=1&per_page=25&page=1
# link for just jobs https://ucla.joinhandshake.com/job-search/10799122?jobType=9&per_page=25&page=1
def save_handshake_jobs():

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument(r"--user-data-dir=C:\selenium-profile")
    options.add_argument("--profile-directory=Default")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    internship_limit = 231
    job_limit = 1000
    wait = WebDriverWait(driver, 2)
    page = 1

    time.sleep(random.uniform(3, 6))
    while page < job_limit:
    # open handshake search
     # driver.execute_script(f"window.location.href='https://ucla.joinhandshake.com/job-search/10812441?jobType=3&pay%5BsalaryType%5D=1&per_page=25&page={}'") 
     # driver.execute_script(f"window.location.href='https://ucla.joinhandshake.com/job-search/10799122?jobType=9&per_page=25&page={}'")
     
        driver.execute_script(f"window.location.href='https://ucla.joinhandshake.com/job-search/10799122?jobType=9&per_page=25&page={page}'")
        time.sleep(random.uniform(3, 5))

        # scroll so all jobs load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div[data-hook*='job-result-card']")
        ))

        job_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-hook*='job-result-card']")

        print("Jobs found:", len(job_cards))

        for i in range(len(job_cards)):

            try:
                # refresh list because DOM changes after clicking
                job_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-hook*='job-result-card']")
                job = job_cards[i]

                # scroll into view
                driver.execute_script("arguments[0].scrollIntoView();", job)
                time.sleep(random.uniform(3, 10))

                # click the job card
                job.click()
                print("Opened job", i+1)

                time.sleep(random.uniform(3, 5))

                # look for apply button text
                apply_buttons = driver.find_elements(By.XPATH, "//button//span[contains(text(),'Apply')]")

                if apply_buttons:

                    action_text = apply_buttons[0].text.strip().lower()

                    print("Action:", action_text)

                    if "externally" in action_text:
                        print("Skipping external apply")

                    else:
                        save_button = driver.find_element(By.XPATH, "//button[.//span[text()='Save']]")
                        save_button.click()
                        print("Saved job")

                time.sleep(random.uniform(3, 5))

            except Exception as e:
                print("Error with job", i+1, e)
        print(f"page {page} has been scanned")
        page += 1
    print("\nFinished scanning all pages.")  # ADDED
if __name__ == "__main__":
    save_handshake_jobs()