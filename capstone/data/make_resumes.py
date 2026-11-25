# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""make_resumes.py: fake resumes and job posts for the ResumeCheck capstone brief.

    uv run make_resumes.py --student <your student id>
    uv run make_resumes.py --student <id> --resumes 12 --jobs 6 --out out/resumes
    uv run make_resumes.py --self-test

Writes resumes/resume-01.md ..., jobs/job-01.md ..., and index.json.
Every person, company and school is invented; names are marked as fictional.
Some resumes contain traps for the hard rule: skills the person only wants to
learn, tools a colleague used, and courses started but not finished.
The same --student id always gives the same files.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

FIRST = ["Asha", "Ben", "Carmen", "Dev", "Elif", "Farid", "Gina", "Hugo", "Isla", "Jonas", "Kiran",
         "Lucia", "Mateo", "Noor", "Oscar", "Rina", "Sami", "Tara", "Uma", "Victor"]
LAST = ["Arden", "Brook", "Calder", "Dune", "Ellis", "Fenwick", "Garnet", "Hale", "Ivers", "Juniper",
        "Kestrel", "Lowe", "Marlow", "Nash", "Orwin", "Pell", "Quill", "Rowan", "Sable", "Thorne"]
COMPANIES = ["Brightpath Logistics", "Copperleaf Foods", "Lumen Health Labs", "Northgate Retail",
             "Bluewater Analytics", "Riverstone Travel", "Oakline Software", "Sunfield Energy",
             "Tidewell Insurance", "Greystone Media"]
SCHOOLS = ["Westbrook Institute of Technology", "Lakeside University", "Hillcrest College of Engineering",
           "Eastmoor University", "Kingsford Polytechnic"]
ROLES = {
    "Data analyst": ["SQL", "Excel", "Python", "pandas", "Power BI", "Tableau", "statistics", "A/B testing"],
    "Backend developer": ["Python", "FastAPI", "PostgreSQL", "Docker", "REST APIs", "pytest", "Git", "Redis"],
    "Frontend developer": ["JavaScript", "TypeScript", "React", "CSS", "HTML", "accessibility", "Vite", "Git"],
    "Support engineer": ["customer support", "SQL", "Linux", "ticketing systems", "scripting", "networking",
                         "written communication", "incident handling"],
    "ML engineer": ["Python", "PyTorch", "scikit-learn", "model evaluation", "Docker", "SQL", "LLM APIs",
                    "vector databases"],
}
ACHIEVE = [
    "Cut the time to produce the weekly report from 6 hours to 1 hour using {skill}.",
    "Built an internal tool with {skill} that 40 colleagues use every day.",
    "Reduced customer complaints by 15% after fixing problems found with {skill}.",
    "Led a team of 3 to move the old system to {skill}.",
    "Wrote the team's guide to {skill} for new joiners.",
]


def make_resume(rng: random.Random, n: int) -> tuple[dict, str]:
    role = rng.choice(list(ROLES))
    pool = ROLES[role][:]
    rng.shuffle(pool)
    has = pool[: rng.randint(4, 6)]
    missing = [s for s in ROLES[role] if s not in has]
    years = rng.randint(2, 9)
    current_start = 2027 - max(1, years // 2)
    name = f"{rng.choice(FIRST)} {rng.choice(LAST)}"
    jobs = rng.sample(COMPANIES, 2)
    traps = []
    lines = [f"# {name} (fictional)", "", f"{role} · {years} years of experience · Remote or hybrid", "",
             "## Summary", "",
             f"{role} with {years} years of experience. Strongest in {has[0]} and {has[1]}.", "",
             "## Skills", "", ", ".join(has) + ".", "", "## Experience", "",
             f"**{role}, {jobs[0]}** ({current_start} to now)", ""]
    for _ in range(2):
        lines.append("- " + rng.choice(ACHIEVE).format(skill=rng.choice(has)))
    if missing and rng.random() < 0.6:  # trap: a tool the team used, not the person
        tool = missing.pop(0)
        traps.append({"skill": tool, "trap": "used by the team, not by the person"})
        lines.append(f"- Worked alongside the data platform team, who maintained the {tool} setup.")
    lines += ["", f"**Junior {role.lower()}, {jobs[1]}** ({2027 - years} to {current_start})", "",
              "- " + rng.choice(ACHIEVE).format(skill=rng.choice(has)), "",
              "## Education", "", f"BSc in Computer Science, {rng.choice(SCHOOLS)} ({2027 - years})", ""]
    if missing and rng.random() < 0.5:  # trap: a course started, not finished
        course = missing.pop(0)
        traps.append({"skill": course, "trap": "course started, not finished"})
        lines += [f"Currently taking an online course in {course} (about a third complete).", ""]
    lines += ["## Interests", ""]
    if missing and rng.random() < 0.7:  # trap: wants to learn
        wish = missing.pop(0)
        traps.append({"skill": wish, "trap": "wants to learn it"})
        lines.append(f"Keen to learn {wish} next year. Hiking, chess and cooking.")
    else:
        lines.append("Hiking, chess and cooking.")
    meta = {"id": f"resume-{n:02d}", "file": f"resumes/resume-{n:02d}.md", "role": role,
            "years": years, "skills_claimed": has, "traps": traps}
    return meta, "\n".join(lines) + "\n"


def make_job(rng: random.Random, n: int) -> tuple[dict, str]:
    role = rng.choice(list(ROLES))
    pool = ROLES[role][:]
    rng.shuffle(pool)
    must, nice = pool[:4], pool[4:6]
    company = rng.choice(COMPANIES)
    min_years = rng.choice([1, 2, 3, 5])
    text = "\n".join([
        f"# {role} at {company} (fictional)", "",
        f"{company} is hiring a {role.lower()} to join a small team. Hybrid, 2 days a week in the office.", "",
        "## You must have", "", *[f"- {s}" for s in must], f"- At least {min_years} years of experience", "",
        "## Nice to have", "", *[f"- {s}" for s in nice], "",
        "## What you will do", "",
        f"- Work with {must[0]} and {must[1]} every day.",
        "- Write clear notes for the rest of the team.",
        "- Take part in code or work reviews.", ""])
    meta = {"id": f"job-{n:02d}", "file": f"jobs/job-{n:02d}.md", "role": role, "must": must,
            "nice": nice, "min_years": min_years}
    return meta, text


def make_all(student: str, n_resumes: int, n_jobs: int):
    rng = random.Random(f"genai-ess-resumes|{student}")
    resumes = [make_resume(rng, i) for i in range(1, n_resumes + 1)]
    jobs = [make_job(rng, i) for i in range(1, n_jobs + 1)]
    return resumes, jobs


def write(resumes, jobs, out: Path) -> None:
    for sub in ("resumes", "jobs"):
        (out / sub).mkdir(parents=True, exist_ok=True)
    for meta, text in resumes + jobs:
        (out / meta["file"]).write_text(text, encoding="utf-8", newline="\n")
    index = {"resumes": [m for m, _ in resumes], "jobs": [m for m, _ in jobs]}
    (out / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8", newline="\n")


def self_test() -> None:
    a, b, c = make_all("s1", 12, 6), make_all("s1", 12, 6), make_all("s2", 12, 6)
    assert a == b and a != c
    resumes, jobs = a
    assert sum(len(m["traps"]) for m, _ in resumes) >= 6, "enough traps for the hard rule"
    for meta, text in resumes:
        for t in meta["traps"]:
            assert t["skill"] not in meta["skills_claimed"]
        assert "@" not in text and "{" not in text and "(fictional)" in text
    print("self-test passed: deterministic, traps present, no contact details")


def main() -> int:
    p = argparse.ArgumentParser(description="Make fake resumes and job posts.")
    p.add_argument("--student", help="your student id; the same id gives the same files")
    p.add_argument("--resumes", type=int, default=12, help="number of resumes (default 12)")
    p.add_argument("--jobs", type=int, default=6, help="number of job posts (default 6)")
    p.add_argument("--out", default="out/resumes", help="output folder (default out/resumes)")
    p.add_argument("--self-test", action="store_true", help="check the generator and exit")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.student:
        p.error("--student is required (use your student id)")
    resumes, jobs = make_all(args.student, args.resumes, args.jobs)
    write(resumes, jobs, Path(args.out))
    print(f"Wrote {len(resumes)} resumes, {len(jobs)} job posts and index.json to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
