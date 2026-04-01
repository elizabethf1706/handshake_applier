from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import random
from openai import OpenAI

# 263 pages for internships
# link for just paid internships: https://ucla.joinhandshake.com/job-search/10812441?jobType=3&pay%5BsalaryType%5D=1&per_page=25&page=1
# link for just jobs https://ucla.joinhandshake.com/job-search/10799122?jobType=9&per_page=25&page=1
 
def ai_evaluate_job(title, description):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=api_key)
    prompt = f"""
        You are given a job title and description from a job board.

        Your task: Decide whether the job or internship is worth saving for the user.

        Respond with ONLY one word:
        - "yes" if the job should be saved
        - "no" if it should NOT be saved

        ------------------------
        USER PROFILE
        ------------------------
        - Bachelor's in Computer Science and Linguistics (UCLA)
        - Currently pursuing a Master's in Computer Science
        - 1 year of software development experience
        - Skills: Python, JavaScript, AI, LLMs, agents

        ------------------------
        TARGET ROLES (GOOD FIT)
        ------------------------
        Save jobs or internships related to:
        - Software engineering
        - AI / Machine Learning
        - Data science / data engineering
        - Product management
        - UX / UI
        - Technical project/program management
        - General tech or engineering roles
        - Analyst Roles

        ------------------------
        HARD REJECTION RULES (IF ANY MATCH → ANSWER "no")
        ------------------------
        Reject the job if:
        - It is primarily in sales, marketing, recruiting, or customer service
        - It requires bilingual ability
        - It requires 2+ years of experience (EXCEPTION: ranges like "0–4 years" are OK)
        - It requires:
        - Law school
        - Paralegal certification
        - Medical degree
        - it requires a completed Master's or PhD
        - It requires a degree ONLY in unrelated fields (e.g., nursing, social work, education, business) AND does not say other fields are accepted
        - It is ONLY for currently enrolled undergraduate students

        ------------------------
        ACCEPTANCE CONDITIONS
        ------------------------
        - Jobs open to graduate students → ACCEPT
        - Jobs requiring "in school" or "recent graduate" → ACCEPT
        - Jobs accepting related fields → ACCEPT
        - Internships and entry-level roles → STRONGLY PREFERRED

        ------------------------
        FINAL INSTRUCTION
        ------------------------
        Evaluate strictly using the rules above.
        If ANY rejection rule applies → answer "no".
        Otherwise → answer "yes".

        ------------------------
        INPUT
        ------------------------
        Title: {title}
        Description: {description}
        """


    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You help the user decide whether a job listing is worth saving."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=20,
        )

        answer = response.choices[0].message.content.strip().lower()
        print(f"AI response: {answer}")

        return answer.startswith("yes")
    except Exception as e:
        print("Error calling OpenAI API:", e)
        return False

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

                # gather job title and description
                title = ""
                description = ""
                try:
                    title_el = driver.find_element(By.XPATH, "//h1 | //h2[@data-hook='job-title'] | //div[contains(@class, 'job-title')]//h1")
                    title = title_el.text.strip()
                except Exception:
                    pass

                try:
                    desc_el = driver.find_element(By.XPATH, "//div[@data-hook='job-description'] | //div[contains(@class, 'job-description')] | //div[contains(@class, 'description')]")
                    description = desc_el.text.strip()
                except Exception:
                    pass

                print(f"Job title: {title}")
                print(f"Job desc length: {len(description)}")

                # send to AI to determine whether to save
                worth_saving = ai_evaluate_job(title, description)

                if worth_saving:
                    try:
                        save_button = driver.find_element(By.XPATH, "//button[.//span[text()='Save']]")
                        save_button.click()
                        print("Saved job based on AI evaluation")
                    except Exception as save_e:
                        print("Could not click Save button:", save_e)
                else:
                    print("AI says not worth saving")

                time.sleep(random.uniform(3, 5))

            except Exception as e:
                print("Error with job", i+1, e)
        print(f"page {page} has been scanned")
        page += 1
    print("\nFinished scanning all pages.")  # ADDED
if __name__ == "__main__":
    save_handshake_jobs()