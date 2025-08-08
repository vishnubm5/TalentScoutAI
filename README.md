#TalentScout — AI Hiring Assistant
Streamlit · LLM-based resume parser · Interview question generator

A lightweight hiring assistant that performs an initial technical screen by parsing a candidate’s resume (PDF) and generating 10 tailored interview questions based on the candidate’s declared tech stack. Built for local use with a simple Streamlit UI and modular code for prompt-engineering experiments.

**🚀 Demo (what it does)**
Upload a text-based PDF resume.

The app extracts skills/projects (heuristic + LLM fallback) and generates 10 realistic, human-style technical questions that reference the candidate’s listed technologies and projects.

Q&A flow runs in a single-page Streamlit UI and stores answers in session state for the demo.

Note: This repo uses a local LLM client (e.g., Ollama) by default. Swap in your preferred LLM provider or SDK as needed.

**✨ Features**
PDF text extraction using PyPDF2 with conservative heuristics for SKILLS and PROJECTS sections.

LLM fallback parser that returns a strict JSON object: skills, education, projects, experience_years when heuristics are insufficient.

LLM-driven question generator that produces 10 targeted interview questions referencing actual skills/projects found in the resume.

Streamlit UI for resume upload, sequential question presentation, and inline answer collection.

Simple context handler to detect conversation-ending keywords and exit gracefully.

**🧰 Tech stack**
Python 3.9+

Streamlit

PyPDF2

ollama (or your preferred LLM SDK)

