TalentScout — AI Hiring Assistant

Streamlit · LLM-based resume parser · Interview question generator

A lightweight Hiring Assistant that performs initial technical screening by parsing a candidate's resume (PDF) and generating 10 tailored interview questions based on the candidate's declared tech stack. Built for local deployment with an easy Streamlit UI and modular code for prompt engineering experiments.

Demo

Upload a text-based PDF resume and the app will parse skills/projects and generate 10 human-style technical interview questions.

UI: Streamlit (single-page), Q&A flow with session-state tracking.

Note: This repository uses a local LLM client (e.g., Ollama) by default. Substitute your preferred LLM client or API as needed.

Features

Resume text extraction (PyPDF2) with conservative heuristics for SKILLS and PROJECTS sections.

LLM fallback parser that returns a strict JSON (skills, education, projects, experience_years) when heuristics fail.

LLM-based question generator that outputs 10 realistic interview questions referencing actual skills or projects found in the resume.

Streamlit UI for resume upload, question presentation, and answer collection.

Simple context handler to exit gracefully when conversation-ending keywords are detected.

Tech Stack

Python 3.9+

Streamlit

PyPDF2

ollama (or your preferred LLM SDK)

