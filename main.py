from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
import time
import random
from ai import ai_evaluate_job

# 263 pages for internships
# link for just paid internships: https://ucla.joinhandshake.com/job-search/10812441?jobType=3&pay%5BsalaryType%5D=1&per_page=25&page=1
# link for just jobs https://ucla.joinhandshake.com/job-search/10799122?jobType=9&per_page=25&page=1
 


def setup_driver():
    """Set up and return Chrome driver with options."""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument(r"--user-data-dir=C:\selenium-profile")
    options.add_argument("--profile-directory=Default")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    wait = WebDriverWait(driver, 12)
    return driver, wait

def check_login(driver):
    """Check if login is required and wait for user to log in."""
    try:
        login_indicator = driver.find_element(By.XPATH, "//input[@type='email'] | //button[contains(text(),'Log in')] | //a[contains(text(),'Sign in')]")
        print("Login required. Please log in manually in the browser window.")
        input("Press Enter after logging in to continue...")
    except Exception:
        pass  # Assume logged in

def load_page(driver, page):
    """Load a specific page of job search results."""
    driver.execute_script(f"window.location.href='https://ucla.joinhandshake.com/job-search/10799122?jobType=9&per_page=25&page={page}'")
    time.sleep(random.uniform(1, 3))

def get_job_cards(driver, wait):
    """Scroll to load all jobs and return job cards."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div[data-hook*='job-result-card']")
    ))
    job_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-hook*='job-result-card']")
    print("Jobs found:", len(job_cards))
    return job_cards

def click_job_card(driver, job):
    """Click on a job card to open the job details."""
    driver.execute_script("arguments[0].scrollIntoView();", job)
    time.sleep(random.uniform(1, 3))

    try:
        # Find the clickable anchor link inside the job card
        job_link = job.find_element(By.XPATH, ".//a[@role='button']")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", job_link)
        time.sleep(0.5)
        job_link.click()
    except:
        # Fallback: use JavaScript to click the job card
        driver.execute_script("arguments[0].click();", job)

def expand_description(driver):
    """Click the 'More' button to expand job description."""
    try:
        # Click the "More" button using the view-more-button class
        # Retry up to 3 times in case of stale element
        max_retries = 3
        for attempt in range(max_retries):
            try:
                more_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(@class, 'view-more-button') and contains(text(), 'More')]")
                    )
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", more_button)
                time.sleep(0.5)
                print("Found 'More' button, attempting click...")

                # Use JavaScript click to avoid Selenium click issues
                driver.execute_script("arguments[0].click();", more_button)

                # Wait for the content to expand (Less button appears)
                time.sleep(1)
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[contains(@class, 'view-more-button') and contains(text(), 'Less')]")
                    )
                )
                print("More button clicked successfully")
                return True  # Success
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"Could not find/click more button after {max_retries} attempts: {e}")
                    return False
                else:
                    print(f"Attempt {attempt + 1} failed, retrying...")
                    time.sleep(1)  # Wait before retry
    except Exception as expand_e:
        print(f"Could not find/click more button: {expand_e}")
        return False

def extract_job_details(driver):
    """Extract job title and description from the page."""
    title = ""
    description = ""

    try:
        title_el = driver.find_element(By.XPATH, "//h1 | //h2[@data-hook='job-title'] | //div[contains(@class, 'job-title')]//h1")
        title = title_el.text.strip()
    except Exception:
        pass

    try:
        # Find the "Less" button and get the description from its immediate parent
        less_button = driver.find_element(By.XPATH, "//button[contains(@class, 'view-more-button') and contains(text(), 'Less')]")
        # Get the immediate parent container which has the description text right above
        description_container = less_button.find_element(By.XPATH, "./parent::div")
        # Extract all text from this container
        full_text = description_container.text.strip()
        # Remove "Less" from the end
        if "Less" in full_text:
            description = full_text.replace("Less", "").strip()
        else:
            description = full_text
    except Exception:
        # Fallback to original selectors if Less button not found
        try:
            desc_el = driver.find_element(By.XPATH, "//div[@data-hook='job-description'] | //div[contains(@class, 'job-description')] | //div[contains(@class, 'description')]")
            description = desc_el.text.strip()
        except Exception:
            pass

    return title, description

def save_job_if_worth(driver, title, description):
    """Evaluate job with AI and save if worth it."""
    print(f"Job title: {title}")
    print(f"Job description: {description}")

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

def process_single_job(driver, job, wait, job_index):
    """Process a single job: click, expand, extract, evaluate, save."""
    try:
        click_job_card(driver, job)
        print("Opened job", job_index + 1)

        expand_description(driver)
        title, description = extract_job_details(driver)
        save_job_if_worth(driver, title, description)

        time.sleep(random.uniform(1, 3))

    except Exception as e:
        print("Error with job", job_index + 1, e)

def save_handshake_jobs():
    """Main function to scrape and save Handshake jobs."""
    driver, wait = setup_driver()
    job_limit = 1000
    page = 1

    try:
        while page < job_limit:
            load_page(driver, page)
            check_login(driver)
            job_cards = get_job_cards(driver, wait)

            for i in range(len(job_cards)):
                # Refresh job cards list because DOM changes after clicking
                job_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-hook*='job-result-card']")
                job = job_cards[i]
                process_single_job(driver, job, wait, i)

            print(f"page {page} has been scanned")
            page += 1

        print("\nFinished scanning all pages.")
    finally:
        driver.quit()
if __name__ == "__main__":
    save_handshake_jobs()