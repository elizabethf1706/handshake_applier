from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def save_handshake_jobs():

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument(r"--user-data-dir=C:\selenium-profile")
    options.add_argument("--profile-directory=Default")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 10)
    time.sleep(2)
    # open handshake search
    driver.execute_script("window.location.href='https://app.joinhandshake.com/job-search?page=1&per_page=25'")    
    time.sleep(3)
    print("\nLog into Handshake in the browser.")
    input("Once you are logged in and on the job search page, press ENTER here...")

    # scroll so all jobs load
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    job_cards = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div[data-hook*='job-result-card']")
    )
)

    print("Jobs found:", len(job_cards))

    # for i in range(len(job_cards)):

    #     try:
    #         # refresh list because DOM changes after clicking
    #         job_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-hook*='job-result-card']")
    #         job = job_cards[i]

    #         # scroll into view
    #         driver.execute_script("arguments[0].scrollIntoView();", job)
    #         time.sleep(1)

    #         # click the job card
    #         job.click()
    #         print("Opened job", i+1)

    #         time.sleep(3)

    #         # look for apply button text
    #         apply_buttons = driver.find_elements(By.XPATH, "//button//span[contains(text(),'Apply')]")

    #         if apply_buttons:

    #             action_text = apply_buttons[0].text.strip().lower()

    #             print("Action:", action_text)

    #             if "externally" in action_text:
    #                 print("Skipping external apply")

    #             else:
    #                 save_button = driver.find_element(By.XPATH, "//button[.//span[text()='Save']]")
    #                 save_button.click()
    #                 print("Saved job")

    #         time.sleep(2)

    #     except Exception as e:
    #         print("Error with job", i+1, e)

if __name__ == "__main__":
    save_handshake_jobs()