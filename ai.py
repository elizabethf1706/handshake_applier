from openai import OpenAI, RateLimitError
import os
import time 
from dotenv import load_dotenv
load_dotenv()
resume = """Recent UCLA graduate with 1 year of software development experience, located in southern California, working full time
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
Python, JavaScript, HTML, CSS, React, Node.js, Flask, Streamlit, MongoDB, REST APIs, Git, GitHub, VS Code,
technical skills:Terraform, WordPress, LLMs, Generative AI, NLP, RAG, OpenAI, Groq, Google Sheets, Tableau, AI/ML, Selenium,
Monday.com, Webscraping, AWS
"""
def ai_evaluate_job(title, description):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=api_key)
    prompt = f"""
    You must follow this EXACT decision process:
        You are given a job title and description from a job board. please read the prompt fully before making a decision

        Your task: Decide whether the job or internship is worth saving for the user. User is open to any field besides the ones listed in the hard rejects.
        - Ignore ALL requirements when considering rejection, unless it specifically states a hard requirement in which you must have at least 2 years of experience in a work role, in which case apply the hard reject rule about work experience.
        Respond with ONLY:
        - "yes" if the job should be saved
        - "no: <clear reason from HARD RULES ONLY>"
STEP 1: Check HARD REJECTION rules ONLY
- Reject ONLY if:
  1. The job is PRIMARILY a sales, marketing, customer service, or retail role.  
  2. The job EXPLICITLY requires 2+ years of work experience (must be clearly stated, do NOT assume)
  3. The job EXPLICITLY requires a degree the user does NOT have, and does not specify that unrelated majors or similar majors can apply (NOT engineering, CS, Lingustics, Information Systems/Technology, or related)
  4. The job REQUIRES bilingual ability
  5. The job REQUIRES a PhD, JD, MD, or Paralegal certification. 
  6. The job only wants or specifies a specific year in school that the user is not a part of such as freshman, sophmore, junior and senior, AND does not say that "recent graduates", "current students enrolled in a masters or 4 year institution" or "masters students" can also apply
        - If it says a specific year but also says recent graduates or masters students can apply, do NOT reject.
        - If it says currently enrolled student, masters student, enrolled in a 4 year institution, or recent gradute, user falls into that role and should not reject.


IMPORTANT:
- Do NOT infer or assume requirements
- Do NOT treat "preferred" as required
- Do NOT assume a Bachelor's degree = experience requirement

STEP 2: If NONE of the above apply → ACCEPT

STEP 3: Ignore the following when deciding:
- Skills (languages, tools, frameworks)
- Years of experience UNLESS explicitly stated as required
- Industry (tech vs non-tech)
- Tasks like customer interaction IF the role is technical or white-collar or relevant to user. For example, IT support is fine to accept.

STEP 4: Special clarification rules:
- IT, Software Dev, Engineering, Analyst, or Technical roles are ALWAYS acceptable even if they include support or customer interaction
- If the role is ambiguous → default to YES


        NOTES
        --------
        - DO NOT reject based off the field the position it is in, only reject if the position is not somethng we would likely qualify for. For example a software developer in the film field we should NOT REJECT for.
        - Do not reject based off of specific skills, tools, or experiences except if it speciically states we require 2+ years in a language or tooling.  
        For example, If the role is in software engineering but requires Java and the user doesnt have it, dont reject. But if role is sofware engineering and calls for 2+ years of java, reject.
        When considering degrees an example of what to accept for is "Currently pursuing a Bachelor’s or Master’s degree in Computer Science, Information Systems, Engineering, or a related field."
        (do not reject if it is for "students and recent graduates", "must be enrolled in a 4 year institution", or "enrolled students")
        (if role is labeled in a tech field or position such as IT support, or Application Engineering or white collar job and has some sales, support tasks do not reject).
        - If you feel the role suits the users resume very well and does not fit specific experience requirements or tooling, override to accept anyways.

        ------------------------
        USER PROFILE
        ------------------------
        - Recently Completed Bachelor's in Computer Science and Linguistics (UCLA) Dec 2025, Current masters student in Electrical Engineering-and Computer Science
        - 1 year of software development experience
       -        users resume: {resume}
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