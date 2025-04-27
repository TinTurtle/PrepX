import streamlit as st
from google import genai
from google.genai import types
import datetime
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Predefined options for tech interviews
DISCIPLINE_OPTIONS = [
    "Operating Systems", "Computer Networks", "Cloud Computing",
    "Software Development", "Database Management", "Data Structures & Algorithms",
    "System Design", "Security", "DevOps", "Programming Languages"
]

SYSTEM_OPTIONS = [
    "Process Management", "Memory Management", "File Systems",
    "Networking Protocols", "Cloud Architecture", "Software Development Lifecycle",
    "Database Design", "Algorithm Design", "System Architecture", "Security Protocols"
]

COMPETENCY_OPTIONS = [
    "Problem Solving", "Technical Knowledge", "Debugging",
    "System Design", "Code Optimization", "Security Best Practices"
]

EXAMPLE_ITEMS = """
<example#1> In the context of operating systems, which of the following scheduling algorithms is most likely to result in starvation? 
(A) Round Robin 
(B) First-Come, First-Served 
(C) Shortest Job Next 
(D) Priority Scheduling 
(E) Multilevel Queue Scheduling 
Correct Answer: D </example1>

<example#2> A network administrator is troubleshooting a connectivity issue between two subnets. The administrator notices that the default gateway on one of the subnets is incorrectly configured. 
Which of the following tools would be most appropriate to diagnose this issue? 
(A) Ping 
(B) Traceroute 
(C) Netstat 
(D) Nslookup 
(E) Wireshark 
Correct Answer: B </example#2>

<example#3> A developer is designing a distributed system that requires high availability and fault tolerance. 
Which of the following database systems is most suitable for this requirement? 
(A) MySQL 
(B) MongoDB 
(C) Cassandra 
(D) SQLite 
(E) PostgreSQL 
Correct Answer: C </example#3>
"""

class GeminiModel:
    def __init__(self, api_key, model_name="gemini-2.0-flash"):
        if not api_key:
            raise ValueError("API key cannot be empty")
        self.api_key = api_key
        self.model_name = model_name
        self.client = genai.Client(api_key=self.api_key)

    def generate_response(self, system_prompt, user_prompt):
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=f"{system_prompt}\n\n{user_prompt}"
            )
            return response.text
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return f"Error: {str(e)}"

class MCQDevelopmentSystem:
    def __init__(self, api_key):
        self.api_key = api_key;
        self.history = []

    def call_ai_model(self, system_prompt, user_prompt, max_attempts=5, delay_seconds=2):
        for attempt in range(max_attempts):
            try:
                model = GeminiModel(self.api_key) #moved gemini model creation here.
                response = model.generate_response(system_prompt, user_prompt)
                return response
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_attempts - 1:
                    time.sleep(delay_seconds)
        return f"Error: Unable to get response after {max_attempts} attempts"

    def add_to_history(self, role, content, version):
        entry = {
            "timestamp": str(datetime.datetime.now()),
            "role": role,
            "content": content,
            "version": version
        }
        self.history.append(entry)
        return self.history

    def get_history_as_text(self):
        return "\n".join(
            f"[{entry['timestamp']}] {entry['role']} (Version {entry['version']}):\n{entry['content']}\n"
            for entry in self.history
        ) if self.history else "No history available."

def process_mcq(api_key, disciplines, systems, competencies, keywords, num_questions=5):
    try:
        mcq_system = MCQDevelopmentSystem(api_key)

        user_prompt = (
            f"Generate {num_questions} high-quality MCQ items for tech interviews. "
            f"Study these example items carefully:\n{EXAMPLE_ITEMS}\n\n"
            f"Disciplines: {', '.join(disciplines)}\n"
            f"Systems: {', '.join(systems)}\n"
            f"Competencies: {', '.join(competencies)}\n"
            f"Keywords: {keywords}\n\n"
            f"Format each question as a separate item, using 'Question #' instead of 'Item #'. "
            f"Place each answer option (A, B, C, D, E) on a new line, without parentheses around the option letters. "
            f"For example: A. Option text. "
            f"Include the question, answer options, and the Correct Answer."
        )

        questions = mcq_system.call_ai_model(
            "You are an experienced technical interviewer. Create high-quality MCQ items for tech interviews.",
            user_prompt
        )
        mcq_system.add_to_history("MCQ Questions", questions, 1)

        return mcq_system.history 
    except Exception as e:
        print(f"Error in process_mcq: {str(e)}")
        return [{"error": str(e)}]

def main():
    st.title("PrepX🐢")
    disciplines = st.multiselect("Disciplines", DISCIPLINE_OPTIONS)
    systems = st.multiselect("Systems", SYSTEM_OPTIONS)
    competencies = st.multiselect("Competencies", COMPETENCY_OPTIONS)
    keywords = st.text_input("Keywords")
    num_questions = st.number_input("Number of Questions", min_value=1, value=5)

    if st.button("Generate MCQs"):
        with st.spinner("Generating MCQs..."):
            history = process_mcq(os.environ.get("GEMINI_API_KEY"), disciplines, systems, competencies, keywords, num_questions)

            if history and "content" in history[0]:
                generated_text = history[0]["content"]
                questions = generated_text.split("\n\n")

                st.subheader("Generated MCQs")
                for question in questions:
                    lines = question.split("\n")
                    for line in lines:
                        line = line.replace("(A)", "A.").replace("(B)", "B.").replace("(C)", "C.").replace("(D)", "D.").replace("(E)", "E.")
                        st.write(line)
            else:
                st.error("Error generating MCQs. Please check the logs.")

if __name__ == "__main__":
    main()