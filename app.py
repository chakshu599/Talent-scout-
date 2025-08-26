import os, json, re, time
import streamlit as st
import requests

from typing import List, Dict
from prompt_templates import SYSTEM_GREETING, qgen_prompt, validate_field_prompt, SUMMARY_PROMPT
from question_generator import QuestionGenerator
from data_handler import Candidate, END_KEYWORDS
from config import OPENAI_API_KEY, MODEL_NAME, PROJECT_NAME

st.set_page_config(page_title="TalentScout — AI Hiring Assistant", page_icon="🎯", layout="wide")
st.title("TalentScout — AI Hiring Assistant")

# Sidebar
with st.sidebar:
    st.header("Progress")
    if "stage" not in st.session_state:
        st.session_state.stage = "greet"
    st.write(f"Stage: {st.session_state.stage}")
    st.caption("Type any of: quit/exit/stop/end/goodbye to conclude.")

# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = []
if "candidate" not in st.session_state:
    st.session_state.candidate = {
        "name": "", "email": "", "phone": "", "experience_years": 0.0,
        "positions": [], "location": "", "tech_stack": [], "answers": {}
    }
if "questions" not in st.session_state:
    st.session_state.questions = {}
if "q_cursor" not in st.session_state:
    st.session_state.q_cursor = {"tech": None, "idx": 0}
if "tech_order" not in st.session_state:
    st.session_state.tech_order = []

def say(role, text):
    with st.chat_message(role):
        st.write(text)
    st.session_state.messages.append({"role": role, "content": text})

# Greeting
if st.session_state.stage == "greet":
    say("assistant", "Hi! I’m TalentScout. I’ll collect basic info and then ask a few technical questions based on the declared tech stack. This takes about 10 minutes.")
    st.session_state.stage = "name"

# Render history
for m in st.session_state.messages[:-1]:
    pass  # already rendered above

def end_if_keyword(text: str) -> bool:
    token = text.strip().lower()
    if token in END_KEYWORDS:
        say("assistant", "Thanks for your time. The conversation is now concluded. Next steps: A recruiter will review and contact if there’s a match.")
        st.session_state.stage = "end"
        return True
    return False

def call_openai(prompt: str, system: str = "") -> str:
    # Simple REST call placeholder; integrate your OpenAI SDK if preferred
    # This stub purposefully avoids sending requests in this template.
    # Replace with actual API call in production.
    return ""

def validate_field(field_name: str, value: str) -> Dict:
    # Local lightweight validators as fallback
    if field_name == "email":
        ok = re.match(r"^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$", value) is not None
        return {"valid": ok, "reason": "" if ok else "Invalid email format", "normalized": value.strip()}
    if field_name == "phone":
        digits = re.sub(r"\\D", "", value)
        ok = len(digits) >= 6
        return {"valid": ok, "reason": "" if ok else "Phone too short", "normalized": value.strip()}
    if field_name == "experience_years":
        try:
            years = float(value)
            ok = years >= 0 and years < 60
            return {"valid": ok, "reason": "" if ok else "Unreasonable years", "normalized": years}
        except:
            return {"valid": False, "reason": "Not a number", "normalized": 0.0}
    if field_name in {"name","location"}:
        ok = 2 <= len(value.strip()) <= 120
        return {"valid": ok, "reason": "" if ok else "Length out of range", "normalized": value.strip()}
    if field_name == "positions":
        items = [s.strip() for s in value.split(",") if s.strip()]
        ok = len(items) > 0
        return {"valid": ok, "reason": "" if ok else "Provide at least one position", "normalized": items}
    if field_name == "tech_stack":
        items = [s.strip() for s in value.split(",") if s.strip()]
        ok = len(items) > 0
        return {"valid": ok, "reason": "" if ok else "Provide at least one technology", "normalized": items}
    return {"valid": True, "reason": "", "normalized": value}

def next_question():
    # Determine current tech and index
    if not st.session_state.tech_order:
        st.session_state.tech_order = list(st.session_state.questions.keys())
    if not st.session_state.tech_order:
        return None, None
    tech = st.session_state.q_cursor["tech"]
    idx = st.session_state.q_cursor["idx"]
    if tech is None:
        tech = st.session_state.tech_order
        idx = 0
    q_list = st.session_state.questions.get(tech, [])
    if idx >= len(q_list):
        # move to next tech
        tpos = st.session_state.tech_order.index(tech)
        if tpos + 1 < len(st.session_state.tech_order):
            tech = st.session_state.tech_order[tpos + 1]
            idx = 0
        else:
            return None, None
        q_list = st.session_state.questions.get(tech, [])
    st.session_state.q_cursor = {"tech": tech, "idx": idx}
    return tech, q_list[idx]["q"]

def advance_cursor():
    tech = st.session_state.q_cursor["tech"]
    idx = st.session_state.q_cursor["idx"] + 1
    st.session_state.q_cursor = {"tech": tech, "idx": idx}

# Main input
user_text = st.chat_input("Type your response...")
if user_text:
    say("user", user_text)
    if end_if_keyword(user_text):
        pass
    elif st.session_state.stage == "name":
        v = validate_field("name", user_text)
        if v["valid"]:
            st.session_state.candidate["name"] = v["normalized"]
            say("assistant", "Thanks. Please share your email address.")
            st.session_state.stage = "email"
        else:
            say("assistant", f"That doesn’t look right ({v['reason']}). What is your full name?")
    elif st.session_state.stage == "email":
        v = validate_field("email", user_text)
        if v["valid"]:
            st.session_state.candidate["email"] = v["normalized"]
            say("assistant", "Got it. Phone number?")
            st.session_state.stage = "phone"
        else:
            say("assistant", "The email format seems off. Please re-enter your email.")
    elif st.session_state.stage == "phone":
        v = validate_field("phone", user_text)
        if v["valid"]:
            st.session_state.candidate["phone"] = v["normalized"]
            say("assistant", "How many years of professional experience?")
            st.session_state.stage = "experience_years"
        else:
            say("assistant", "That phone number seems short. Please provide a valid number (you may include country code).")
    elif st.session_state.stage == "experience_years":
        v = validate_field("experience_years", user_text)
        if v["valid"]:
            st.session_state.candidate["experience_years"] = v["normalized"]
            say("assistant", "Which position(s) are you targeting? (comma-separated)")
            st.session_state.stage = "positions"
        else:
            say("assistant", "Please enter years as a number (e.g., 3.5).")
    elif st.session_state.stage == "positions":
        v = validate_field("positions", user_text)
        if v["valid"]:
            st.session_state.candidate["positions"] = v["normalized"]
            say("assistant", "What is your current location?")
            st.session_state.stage = "location"
        else:
            say("assistant", "Please provide at least one position (comma-separated).")
    elif st.session_state.stage == "location":
        v = validate_field("location", user_text)
        if v["valid"]:
            st.session_state.candidate["location"] = v["normalized"]
            say("assistant", "List your tech stack (comma-separated: languages, frameworks, tools).")
            st.session_state.stage = "tech_stack"
        else:
            say("assistant", "Please provide a valid location.")
    elif st.session_state.stage == "tech_stack":
        v = validate_field("tech_stack", user_text)
        if v["valid"]:
            st.session_state.candidate["tech_stack"] = v["normalized"]
            techs = st.session_state.candidate["tech_stack"]
            # Generate questions via static bank for template (safe)
            qg = QuestionGenerator()
            # placeholder LLM output structure
            llm_out = {t.title(): [{"q": q["q"]} for q in qg.from_bank(t.title(), 4)] for t in techs}
            st.session_state.questions = qg.merge_bank_and_llm(llm_out)
            st.session_state.candidate["answers"] = {t: [] for t in st.session_state.questions.keys()}
            st.session_state.stage = "questions"
            say("assistant", "Thanks. I’ll now ask a few short technical questions per technology.")
            tech, q = next_question()
            if tech and q:
                say("assistant", f"[{tech}] {q}")
            else:
                st.session_state.stage = "summary"
        else:
            say("assistant", "Please provide at least one technology (comma-separated).")
    elif st.session_state.stage == "questions":
        # Record answer for current question
        tech = st.session_state.q_cursor["tech"]
        if tech:
            st.session_state.candidate["answers"].setdefault(tech, []).append(user_text)
            advance_cursor()
            tech2, q2 = next_question()
            if tech2 and q2:
                say("assistant", f"[{tech2}] {q2}")
            else:
                st.session_state.stage = "summary"
                say("assistant", "Thanks for answering. Preparing a short summary...")
    elif st.session_state.stage == "summary":
        c = st.session_state.candidate
        bullets = [
            f"- Experience: {c['experience_years']} yrs; Target roles: {', '.join(c['positions'])}",
            f"- Location: {c['location']}",
            f"- Tech stack: {', '.join(c['tech_stack'])}",
            f"- Answers recorded for: {', '.join([t for t in c['answers'] if c['answers'][t]])}",
            "- Next steps: A recruiter will review and follow up if there’s a match."
        ]
        say("assistant", "\n".join(bullets))
        st.session_state.stage = "end"
    elif st.session_state.stage == "end":
        say("assistant", "Conversation already concluded. Type 'restart' to begin again.")