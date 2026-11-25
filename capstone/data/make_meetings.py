# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""make_meetings.py: synthetic meeting transcripts for the MeetingNotes capstone brief.

    uv run make_meetings.py --student <your student id>
    uv run make_meetings.py --student <id> --count 12 --out out/meetings
    uv run make_meetings.py --self-test

Writes one transcript per meeting (meeting-01.txt, ...) and meetings.json, an index.
Every line of a transcript has a line id such as L014, so an action item can point
to the line it came from. Everyone and everything in them is made up.
The same --student id always gives the same files.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from datetime import date, timedelta
from pathlib import Path

PEOPLE = ["Alex", "Priya", "Jordan", "Maria", "Omar", "Lena", "Tom", "Aisha", "Ravi", "Sam",
          "Chen", "Nadia", "Leo", "Grace", "Kofi", "Ines"]
TOPICS = {
    "Website relaunch": ["the new home page", "the pricing page", "page speed", "the sign-up form",
                         "image sizes", "the launch email"],
    "Quarterly budget": ["the travel budget", "software licences", "the training budget",
                         "the hiring plan", "cloud costs", "the forecast sheet"],
    "Customer support review": ["response times", "the refund backlog", "the help articles",
                                "chat opening hours", "the satisfaction survey", "weekend cover"],
    "Mobile app release": ["the crash on older phones", "the store listing", "the beta testers",
                           "push notifications", "the release notes", "the login screen"],
    "Office move": ["the floor plan", "the moving company", "desk booking", "the network cabling",
                    "the kitchen", "parking spaces"],
    "Hiring sprint": ["the job advert", "the interview panel", "the work sample", "candidate feedback",
                      "the offer letters", "onboarding buddies"],
}
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

SMALL_TALK = [
    "Morning everyone, can you all hear me?", "Sorry I'm late, the last call ran over.",
    "Let's get started, we have thirty minutes.", "Is everyone here? I think we're missing one.",
    "Quick reminder that the notes go in the shared folder.", "Can someone share their screen?",
]
DISCUSS = [
    "I looked at {thing} yesterday and it's in better shape than I expected.",
    "The main problem with {thing} is that nobody owns it at the moment.",
    "We had three complaints about {thing} last week.",
    "I think {thing} can wait until next month.",
    "{thing} is mostly done, there are two small fixes left.",
    "The numbers for {thing} are up about ten percent on last quarter.",
    "Can we talk about {thing} for a minute? It keeps coming up.",
    "I agree, {thing} needs a decision today.",
]
# Real commitments: someone takes a task with an owner and (usually) a due day.
# Each template is a list of (speaker, text) turns.
ACTIONS = [
    [("who", "I'll {verb} {thing} by {day}.")],
    [("who", "Leave {thing} with me, I'll {verb} it before {day}.")],
    [("lead", "{who2}, can you {verb} {thing} by {day}?"), ("who2", "Yes, I'll do that.")],
    [("who", "Action for me: {verb} {thing}. I'll have it done by {day}.")],
    [("lead", "So {who2} owns {thing}, due {day}. Agreed?"), ("who2", "Agreed.")],
]
VERBS = ["update", "review", "write up", "check", "send round", "fix", "draft", "book", "test", "price"]
# Turns that sound like actions but are not: ideas, maybes, declined, already done.
DECOYS = [
    [("who", "Maybe someday we could {verb} {thing}, but not now.")],
    [("who", "It would be nice if somebody looked at {thing} at some point.")],
    [("who", "I was going to {verb} {thing}, but it was already done last week.")],
    [("who", "Should we {verb} {thing}?"), ("who2", "Let's not, it's not worth it this quarter.")],
    [("who", "Last time I said I'd {verb} {thing}. That's done now.")],
]
# An action handed from one person to another: only the second owner counts.
CANCEL = [("who", "Actually, scrap my action on {thing}, {who2} is doing it instead."),
          ("who2", "Yes, I'll take {thing}, by {day}.")]


def make_meeting(rng: random.Random, number: int, start: date) -> tuple[dict, list[str]]:
    title = rng.choice(list(TOPICS))
    things = TOPICS[title][:]
    rng.shuffle(things)
    people = rng.sample(PEOPLE, rng.randint(3, 6))
    lead = people[0]
    day_of_meeting = start + timedelta(days=rng.randrange(0, 5))
    lines: list[str] = []
    minute = 0

    def say(text: str) -> None:
        nonlocal minute
        minute += rng.randint(0, 2)
        lines.append(f"[{9 + minute // 60:02d}:{minute % 60:02d}] {text}")

    say(f"{lead}: {rng.choice(SMALL_TALK)}")
    say(f"{rng.choice(people[1:])}: {rng.choice(SMALL_TALK)}")
    n_actions = rng.randint(2, 5)
    n_decoys = rng.randint(1, 3)
    events = ["action"] * n_actions + ["decoy"] * n_decoys + ["talk"] * rng.randint(8, 18)
    if rng.random() < 0.4:
        events.append("cancel")
    rng.shuffle(events)
    for event in events:
        thing = things[rng.randrange(len(things))]
        who, who2 = rng.sample(people[1:], 2)
        slots = dict(who=who, who2=who2, lead=lead, thing=thing, verb=rng.choice(VERBS),
                     day=rng.choice(DAYS))
        if event == "talk":
            text = rng.choice(DISCUSS).format(**slots)
            say(f"{rng.choice(people)}: {text[0].upper()}{text[1:]}")
            continue
        turns = {"action": lambda: rng.choice(ACTIONS), "decoy": lambda: rng.choice(DECOYS),
                 "cancel": lambda: CANCEL}[event]()
        for speaker, text in turns:
            say(f"{slots[speaker]}: {text.format(**slots)}")
    say(f"{lead}: Thanks all, I'll put the notes in the shared folder.")
    numbered = [f"L{i:03d} {line}" for i, line in enumerate(lines, start=1)]
    meta = {"id": f"meeting-{number:02d}", "title": title, "date": day_of_meeting.isoformat(),
            "attendees": people, "lines": len(numbered), "file": f"meeting-{number:02d}.txt"}
    header = [f"# {title}", f"# Date: {day_of_meeting.isoformat()}", f"# Attendees: {', '.join(people)}", ""]
    return meta, header + numbered


def make_all(student: str, count: int) -> list[tuple[dict, list[str]]]:
    rng = random.Random(f"genai-ess-meetings|{student}")
    start = date(2027, 2, 1)  # a Monday
    return [make_meeting(rng, i, start + timedelta(weeks=(i - 1) // 3)) for i in range(1, count + 1)]


def write(meetings, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for meta, lines in meetings:
        (out / meta["file"]).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    index = [m for m, _ in meetings]
    (out / "meetings.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8", newline="\n")


def self_test() -> None:
    a, b, c = make_all("s1", 12), make_all("s1", 12), make_all("s2", 12)
    assert a == b and a != c
    for meta, lines in a:
        body = [l for l in lines if l.startswith("L")]
        assert body[0].startswith("L001 ") and len(body) == meta["lines"]
        assert all("{" not in l and "@" not in l for l in lines)
    print("self-test passed: deterministic, numbered lines, no unfilled slots")


def main() -> int:
    p = argparse.ArgumentParser(description="Make synthetic meeting transcripts.")
    p.add_argument("--student", help="your student id; the same id gives the same meetings")
    p.add_argument("--count", type=int, default=12, help="number of meetings (default 12)")
    p.add_argument("--out", default="out/meetings", help="output folder (default out/meetings)")
    p.add_argument("--self-test", action="store_true", help="check the generator and exit")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.student:
        p.error("--student is required (use your student id)")
    meetings = make_all(args.student, args.count)
    write(meetings, Path(args.out))
    print(f"Wrote {len(meetings)} transcripts and meetings.json to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
