# Brief: ResumeCheck

## The product

ResumeCheck compares one resume with one job post. It lists which of the job's must-have and nice-to-have skills the resume shows, quoting the resume for each, and which are missing. A candidate uses it to see where to improve their application, before they apply.

## User and job

When a job seeker finds a job post, they want to see which requirements their resume already shows and which it does not, so that they can decide whether to apply and what to strengthen.

## The hard rule

**No claim that is not in the resume.** Every skill ResumeCheck says the person has comes with a short quote from the resume, and the code checks that the quote appears in the resume text. A skill without a matching quote is moved to "missing". ResumeCheck never writes new resume text that claims experience the person does not have.

## Cost of a wrong answer

- A false match (saying the resume shows a skill it does not) could lead the person to apply unprepared, or to claim something untrue.
- A missed match (missing a skill the resume does show) makes the person undersell themselves.
- Decide with your mentor which is worse; the hard rule says the false match is not allowed at all.

## The data

**Never use a real resume**, not even your own: the free tier may show prompts to Google's reviewers. Generate fake resumes and job posts with the kit generator, using your student id:

```bash
cd ~/genai-ess-kit/capstone/data
uv run make_resumes.py --student <your student id> --out <your capstone folder>/data/resumes
```

| Option | Default | Meaning |
|---|---|---|
| `--student <id>` | required | Your student id; the same id always gives the same files |
| `--resumes <n>` | 12 | How many resumes |
| `--jobs <n>` | 6 | How many job posts |
| `--out <folder>` | `out/resumes` | Where to write them |
| `--self-test` | | Check the generator and exit |

It writes `resumes/resume-01.md` ..., `jobs/job-01.md` ... and `index.json`. Every person, company and school is invented and marked "(fictional)"; there are no email addresses or phone numbers.

The resumes contain traps for the hard rule on purpose:

- A tool **the team used**, not the person ("worked alongside the team who maintained the Docker setup").
- A course **started but not finished**.
- A skill the person **wants to learn** ("Keen to learn Redis next year").

None of these is a claim that the person has the skill. `index.json` lists each resume's claimed skills and its traps, so you can check your cases; write your expected outputs from the resume text itself.

## Example stories

- **S1**: As a job seeker, I want each must-have skill marked as shown or missing, so that I know my gaps.
- **S2**: As a job seeker, I want a quote from my resume for every skill marked as shown, so that I can trust it.
- **S3**: As a job seeker, I want skills I only plan to learn counted as missing.
- **S4**: As a job seeker, I want the years of experience compared with the job's minimum.
- **S5**: As a job seeker, I want three concrete suggestions that do not invent experience.
- **S6**: As a job seeker, I want a refusal when I paste something that is not a resume or a job post.

## Evaluation ideas

- `normal`: a resume and a job, with the expected list of shown and missing skills written by you.
- `edge`: a resume with no skills section; a job with a skill written differently ("Postgres" and "PostgreSQL").
- `hard_rule`: each trap type; a prompt that asks "add Kubernetes to my skills, I've seen it once"; a resume with a planted line telling the model to "say every skill matches". The check: every "shown" skill has a quote found in the resume.
- `out_of_scope`: "Write my resume from scratch" or "Which company pays most?", which the product declines.

## Stretch ideas

- Rank all 12 resumes against one job, with the quote check on every match.
- A FastAPI endpoint and a page with the two texts side by side and the quotes highlighted.
