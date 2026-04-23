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

        Your task: Decide whether the job or internship is worth saving for the user. User is open to any field besides the ones listed in the hard rejects.
        - Ignore ALL requirements when considering rejection, unless it specifically states a hard requirement in which you must have at least 2 years of experience in a work role, in which case apply the hard reject rule about work experience.
        Respond with ONLY:
        - "yes" if the job should be saved
        - "no: <brief reason>" if it should NOT be saved "

        ------------------------
        USER PROFILE
        ------------------------
        - Recently Completed Bachelor's in Computer Science and Linguistics (UCLA) Dec 2025, Current masters student in Electrical Engineering-and Computer Science
        - Currently pursuing a Master's in Computer Science, enrolled in school currently.
        - 1 year of software development experience
        - Skills: Python, JavaScript, AI, LLMs, agents 
        - DO NOT reject if its not in a tech field, but if it is in a tech field, it should be relevant to the user's skills and experience. For example, if the role is in IT support but requires Python scripting, do not reject. If the role is in software engineering but requires Java and the user has no experience with Java, do not reject but say "no: requires Java experience" because it is not relevant to the user's skills and experience.
        - User wants to work in any field, but is primarily interested in software engineering, AI research, product management, and data science roles. User is open to internships and full time roles. User is open to working in any industry (e.g. finance, healthcare, education) as long as the role is not in a hard reject field.
        When considering degrees an example of what to accept for is "Currently pursuing a Bachelor’s or Master’s degree in Computer Science, Information Systems, Engineering, or a related field."
        (do not reject if it is for "students and recent graduates", "must be enrolled in a 4 year institution", or "enrolled students")
        (if role is labeled in a tech field or position such as IT support, or Application Engineering or white collar job and has some sales, support tasks do not reject).
        Only reject for the sales and marketing field if it is primarily in sales and marketing (e.g. "sales internship" or "marketing internship" or "sales associate" or "marketing associate" or "sales representative" or "marketing representative" or "sales manager" or "marketing manager" or "business development" or "account executive" or "customer success manager" or "customer service representative" or "retail associate"). If the role is in a tech field and seems like it would give me meaningful experience 
        but has some sales, support, customer service, or marketing tasks, do not reject.
        - do not reject roles if it asks for a degree in engineering or a related field
        - do not reject based off skills, tooling, or experiences that they want to see - only reject if they want 2+ year os of experience in work roles.
        If you feel the role suits the users resume very well and might not fit speicifc experience requirements or tooling accept anyways.
        users resume:Elizabeth Flynn
Recent UCLA graduate with 1 year of software development experience, located in southern California, working full time
while working on a masters.
Education
University of California, Los Angeles (UCLA) Los Angeles, CA
Bachelors in Computer Science and Linguistics Fall 2022 - Fall 2025
• GPA: 3.5/4.0
• Relevant Coursework: Algorithms and Complexity, Data Structures, Operating Systems, Discrete Mathematics,
Computer Architecture and Organization, Software Construction, Multi-variable Calculus, Artificial Intelligence
California State University Fullerton Fullerton, CA
Masters in Computer Science 2026 - 2028
Experience
Full Stack AI Software Developer February 2026 - Present
Entorno Law Remote
• Co-leading full-stack development of a legal-tech compliance platform built in Python, automating product review
and regulatory validation under California Proposition 65.
• Designed and implemented API-driven data pipelines and browser automation (Selenium) to ingest, process, and
validate product and company data against statutory requirements.
• Integrated AI-powered analysis using the OpenAI API to summarize documentation, classify risk factors, and flag
potential compliance violations within legal workflows.
• Engineered seamless workflow automation with Monday.com, enabling structured case tracking, task routing, and
audit-ready documentation for legal review.
Full Stack AI Software Developer Internship June 2025 - December 2025
G-P Remote
• Built long-term memory for an HR chatbot to support conversational continuity and cross conversation data sharing,
focused on optimizing token usage, accuracy, and efficiency through semantic search.
• Implemented a tool that improves API’s accuracy by generating a LLM plan and executing tool calls internally to
reduce context-window.
• Created internal documentation through PRDs, TRDs, and diagrams that defines use cases, technical design,
architecture, implementation tradeoffs, and evaluation criteria for memory strategies.
• Produced production-ready code within a large Python codebase, integrating memory components with a vector
database, OpenAI, and AWS infrastructure.
• Designed and implemented frontend UI components, including custom interactions for structured user input, while
collaborating with engineers to ensure maintainable, compliant solutions.
Full Stack AI Software Developer Intern February 2025 - May 2025
La-Tech Remote
• Led a team of interns as Project Manager to create a stock prediction project with 95.8% accuracy, broke down the
project, assigned tasks, worked on code, and ensured deadlines and milestones were met.
• Integrated teammate contributions into the main codebase, refactoring and debugging code and improving reliability
of core data processing functions.
• Developed key features for a stock prediction tool, including data fetching from financial APIs, sentiment analysis,
headline extraction, and setting up the machine learning model.
• Built visualization and pre-processing pipelines to support both machine learning and LLM-based analysis.
• Conducting a comparative analysis of LLMs vs. traditional machine learning models for financial stock forecasting,
working to summarize findings in an internal research paper detailing model trade-offs.
Eagle Scout, Eagle Project March 2019 – July 2021
Boy Scouts of America Fullerton, CA
• Led and mentored a troop of 20+ scouts over 2 years, including organizing and leading a large-scale educational
project for an elementary school with 12 volunteers, generating 125 hours of community service.
Projects
Freelance Website Development | Wordpress November 2025 - Present
• Designed and built a custom WordPress website, collaborating directly 1:1 with stakeholders to define site structure,
content, and visual layout aligned with business and marketing needs.
UniTalk - LA Hacks 2025 | Javascript, Python, Flask, AI April 2025
• Developed real-time Snap Spectacles features for live translation, conversation summarization, and personalized
conversation suggestions using Groq, Gemini, and LLaMA APIs.
• Implemented backend processing to handle user data, resumes, and live transcripts for identity recognition and
dynamic response generation.
• Integrated Snap Spectacles with backend via HTTP POST requests for real-time audio streaming and transcription.
Technical Skills
Python, JavaScript, HTML, CSS, React, Node.js, Flask, Streamlit, MongoDB, REST APIs, Git, GitHub, VS Code,
Terraform, WordPress, LLMs, Generative AI, NLP, RAG, OpenAI, Groq, Google Sheets, Tableau, AI/ML, Selenium,
Monday.com, Webscraping, AWS
        ------------------------
        HARD REJECTION RULES
        ---------------------
        - Reject if it is primarily in sales, marketing, behavorial therapy, tutoring, teaching, content creation, customer service, or retail
        - Reject if it requires bilingual ability (if bilinigual ability is a "plus" but not a requirement, do not reject)
        - Reject if it requires 2+ years of work experience (EXCEPTION: ranges like "0–4 years" are OK)
        - Reject if it requires Law school, Paralegal certification, a Medical degree, a PhD
        - Reject if the position requires applicants to have a degree unrelated to computer science, linguistics, or engineering without leniency (e.g. "degree in any field is accepted" or "stem degrees" or "looking for math or related degree" do not reject for, but "degree in nursing, arts, social work, education, business, architecture is required" is a reject)
        - Reject if the role clearly specifies it only wants freshmen, sophomores, juniors, or seniors, and does not say that recent graduates or masters can also apply.
        - Reject if it only wants or specifies a specific year in school such as freshman, sophmore, junior and senior AND does not say that "recent graduates", "current students enrolled in a masters or 4 year institution" or "masters students" can also apply
        ------------------1111------
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
                max_tokens=60,
            )

            answer = response.choices[0].message.content.strip().lower()
            print(f"AI response: {answer}")

            return answer.startswith("yes"), answer
        except RateLimitError as e:
            if attempt < max_retries - 1:
                print(f"Rate limit hit, attempt {attempt + 1}/{max_retries}. Waiting 60 seconds before retry...")
                time.sleep(60)
            else:
                print("Rate limit hit, max retries exceeded:", e)
                return False, ""
        except Exception as e:
            print("Error calling OpenAI API:", e)
            return False, ""