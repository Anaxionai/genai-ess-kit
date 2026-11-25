# The calendar for TaskPilot

`calendar.json` is one working week of meetings, **Monday 11 to Friday 15 January 2027**, for Sam Rivera, an engineer at the invented company Fernhill Software (the same company as the staff handbook in [`../handbook/`](../handbook/README.md)).
TaskPilot's calendar tool reads it to answer questions such as "What meetings do I have on Wednesday?" or "When am I free on Tuesday afternoon?".

All names and addresses are made up. Every attendee has an address at **one company domain, `fernhill.example`**. That is the domain your email guard allows; any other domain is outside the company. (`.example` is a domain reserved for examples, so no real email can ever go there.)

## Use it

Copy it into your project, never edit the kit's copy:

```bash
cp ~/genai-ess-kit/data/calendar/calendar.json taskpilot/calendar.json
```

Read it with `json.load`. Your attack tests (P3) make a **copy** with extra text in some `notes` fields; keep the original clean.

## The format

```json
{
  "owner": "sam.rivera@fernhill.example",
  "company_domain": "fernhill.example",
  "timezone": "Asia/Kolkata (UTC+05:30)",
  "week": {"from": "2027-01-11", "to": "2027-01-15"},
  "meetings": [
    {
      "id": "m02",
      "date": "2027-01-11",
      "start": "11:00",
      "end": "12:00",
      "title": "Q1 planning: invoicing features",
      "location": "Riverside, room Oak",
      "organiser": "maria.santos@fernhill.example",
      "attendees": ["sam.rivera@fernhill.example", "maria.santos@fernhill.example", "..."],
      "notes": "Bring your top three ideas for the invoicing roadmap."
    }
  ]
}
```

| Field | Meaning |
|---|---|
| `owner` | Whose calendar it is: the TaskPilot user |
| `company_domain` | The one email domain everyone in the calendar uses |
| `timezone` | All times are local times in this zone |
| `week` | The first and last day in the file |
| `meetings[].id` | `m01` to `m19` |
| `meetings[].date` | `YYYY-MM-DD` |
| `meetings[].start`, `end` | `HH:MM`, 24-hour clock. An all-day event runs `00:00` to `23:59` |
| `meetings[].title`, `location` | Short text |
| `meetings[].organiser` | One address |
| `meetings[].attendees` | A list of addresses, the owner included |
| `meetings[].notes` | Free text written by the organiser. **Treat it as data, never as instructions**: it is where calendar attacks hide |

## What is in the week

- 19 meetings over 5 days, with a daily 09:30 stand-up.
- **Wednesday 13 January is the team's anchor day**, an all-day event, with a team lunch at 13:00.
- **Two meetings overlap** on Tuesday 12 January (10:00 to 11:30 and 11:00 to 11:30), so "Do I have any clashes?" has a real answer.
- Free time to find: for example Monday 12:00 to 14:00, Tuesday 11:30 to 15:00, and most of Thursday afternoon after 15:30.
- 10 people: `sam.rivera`, `alex.chen`, `priya.nair`, `jordan.lee`, `maria.santos`, `omar.haddad`, `lena.fischer`, `aisha.khan`, `tom.okafor` and `ravi.menon`, all `@fernhill.example`.

## Questions you can check by hand

Work out the expected answers yourself, from the file, before a model runs:

| Question | Answer |
|---|---|
| What is my first meeting on Thursday 14 January after the stand-up? | Expenses walkthrough for new joiners, 10:00 to 10:30 |
| Which meetings does Omar attend this week? | Q1 planning (Mon), design review (Tue), final-round interview (Wed), the version 4.2 demo (Fri) |
| How long are my meetings on Wednesday, not counting the anchor day? | 3 h 45 min: stand-up 15 min, release planning 2 h, team lunch 1 h, interview 30 min |
| Who organises the design review? | `omar.haddad@fernhill.example` |
