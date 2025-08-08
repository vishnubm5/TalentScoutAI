
import re, json
from PyPDF2 import PdfReader
import ollama

def extract_text_from_pdf(uploaded_pdf) -> str:
    reader = PdfReader(uploaded_pdf)
    pages = [p.extract_text() or "" for p in reader.pages]
    return "\n".join(pages)

def _extract_section(raw: str, header: str) -> str:
    """Return text under `header` up until the next all‐caps line or blank line."""
    pattern = rf"{header}\s*(.+?)(?:\n[A-Z &]+:|\n\n|$)"
    match = re.search(pattern, raw, re.DOTALL)
    return match.group(1).strip() if match else ""

def parse_resume(uploaded_pdf) -> dict:
    raw_text = extract_text_from_pdf(uploaded_pdf)

    # 1) Try heuristic: SKILLS & INTERESTS
    skills_block = _extract_section(raw_text, "SKILLS & INTERESTS")
    if skills_block:
        # split on commas or newlines, strip out non-text
        skills = [s.strip() for s in re.split(r"[,\n]+", skills_block) if s.strip()]
    else:
        skills = []

    # 2) Try heuristic: PROJECTS
    proj_block = _extract_section(raw_text, "PROJECTS")
    if proj_block:
        # assume each bullet ("•") starts a new project
        projects = [p.strip(" •") for p in proj_block.split("•") if p.strip()]
    else:
        projects = []

    # 3) If heuristics found *something*, skip the LLM parse
    if skills and projects:
        return {
            "skills": skills,
            "education": [],           # you could apply a similar heuristic
            "projects": projects,
            "experience_years": None,   # or fill via LLM if you really need it
            "raw_text": raw_text
        }

    # 4) Otherwise fall back to your original LLM JSON parse
    prompt = (
        "You are a resume parser. Given the following resume text, extract:\n"
        "- skills (programming languages, frameworks, tools)\n"
        "- education (degree, institution, graduation year)\n"
        "- projects (name and brief description)\n"
        "- total years of professional experience\n"
        "Output a JSON object with keys: skills, education, projects, experience_years and nothing else.\n\n"
        f"Resume Text:\n{raw_text}"
    )
    resp = ollama.chat(
        model="mistral:7b",
        messages=[
            {"role":"system", "content":
               "You are a strict JSON resume parser. You will output exactly one JSON object "
               "with keys `skills`, `education`, `projects`, `experience_years` and nothing else."
            },
            {"role":"user", "content": prompt}
        ],
        options={"temperature":0.0}
    )

    try:
        profile = json.loads(resp["message"]["content"])
    except Exception:
        profile = {
            "skills": skills,
            "education": [],
            "projects": projects,
            "experience_years": None
        }

    profile["raw_text"] = raw_text
    return profile
