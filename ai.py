from openai import OpenAI, RateLimitError
import os
import time 
from dotenv import load_dotenv
load_dotenv()
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
        - It is primarily in sales, marketing, behavorial therapy,recruiting, tutoring, content creation, or customer service
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
        - Jobs accepting related fields to cs or linguistics → ACCEPT
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


    max_retries = 3
    for attempt in range(max_retries):
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
        except RateLimitError as e:
            if attempt < max_retries - 1:
                print(f"Rate limit hit, attempt {attempt + 1}/{max_retries}. Waiting 60 seconds before retry...")
                time.sleep(60)
            else:
                print("Rate limit hit, max retries exceeded:", e)
                return False
        except Exception as e:
            print("Error calling OpenAI API:", e)
            return False