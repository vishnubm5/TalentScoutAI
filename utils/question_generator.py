
import ollama
import json

def generate_questions(profile: dict) -> list:
    """
    Given a parsed profile (or raw text), produce 10 tailored questions.
    If no skills/projects found, fall back to asking off the raw resume text.
    """
    # if parser came up empty, use raw_text directly
    if not profile.get("skills") and not profile.get("projects"):
        system_prompt = (
            "You are a senior software engineer conducting a live technical interview.  "
            "You have only the candidate's raw resume text below.  "
            "Craft 10 human-style technical questions that explore their strengths, "
            "projects, and likely areas of expertise based on that text.  "
            "No placeholders."
        )
        user_prompt = f"Resume Text:\n{profile.get('raw_text','')}\n\n" + \
                      "Please produce exactly 10 numbered questions (no bullet list)."
        resp = ollama.chat(
            model="mistral:7b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt}
            ],
            options={"temperature": 0.7, "max_tokens": 500}
        )
    else:
        # your original, data‐driven path
        summary = {
            "skills": profile.get("skills", []),
            "projects": profile.get("projects", []),
            "education": profile.get("education", []),
            "experience_years": profile.get("experience_years", None)
        }
        profile_str = json.dumps(summary, indent=2)
        system_prompt = (
            "You are a senior software engineer.  "
            "You will generate 10 numbered, human-style interview questions.  "
            f"You have been given this profile:\n{profile_str}\n\n"
            "Now ask questions that stitch in actual skills, projects or education entries. "
            "If they list Django, ask about middleware or querysets; "
            "if they list AWS, ask about autoscaling; "
            "etc.  Do not use placeholders."
        )
        user_prompt = (
            "Please produce exactly 10 numbered questions (no bullet list), "
            "each one a realistic question you would ask in a 1-on-1 interview."
        )
        resp = ollama.chat(
            model="mistral:7b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt}
            ],
            options={"temperature": 0.7, "max_tokens": 500}
        )

    content = resp["message"]["content"].strip()
    questions = []
    for line in content.split("\n"):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith("-")):
            q = line.lstrip("0123456789.- )")
            questions.append(q)
    return questions[:10]
