# Example questions for DocAnswer's test set

DocAnswer's test set is a CSV file with one question per row and the document that holds its answer. Your own set has 25 questions; these three rows show the format.

```csv
id,question,expected_source
q01,How many unused days of annual leave can I carry into next year?,leave-annual
q02,Which class do I book for a four-hour flight to a client?,travel-booking
q03,How soon must I report a lost laptop?,it-lost-devices
```

- `id`: a short id you choose, such as `q01`.
- `question`: written the way an employee would ask it, in your own words.
- `expected_source`: the **document id** (the file name without `.md`) that holds the answer. For a question the handbook cannot answer, write `none`: the right answer is "I don't know based on the handbook."

Check each row yourself: open the document and find the sentence that answers the question before you add it. The answers to the three rows above are "up to 5 days, used by 31 March", "economy class (flights under six hours)" and "within 1 hour".

## Tips for questions that are hard to answer

A test set that only asks easy questions will say 100% and teach you nothing. Mix these kinds:

- **Different words from the document.** Ask "Can I keep holiday I didn't use?" when the document says "carry over unused days". This tests meaning, not matching words.
- **Old versus current.** Ask about a rule that changed, such as hotel limits or business class. The superseded documents (`travel-booking-2024`, `work-remote-2024`) give the old numbers; the expected source is the current document.
- **Near duplicates.** Ask something that both `leave-annual` and `leave-faq`, or `expenses-claims` and `expenses-faq`, answer. Decide which one you expect, or accept either and say so in your notes.
- **A number.** Questions with an exact amount or a time limit ("How much is the internet allowance?") make faithfulness easy to check: the number in the answer must match the document.
- **No answer in the handbook.** Include at least 3, such as "What is on the canteen menu on Fridays?" or "How long can a sabbatical be?" (the handbook has no such documents). Their `expected_source` is `none`.
- **Two documents.** A few questions need facts from two places, such as "If I fly abroad and my hotel includes breakfast, what is my meal allowance?" (`travel-hotels-and-meals`). Keep these few; they are hard for retrieval that returns only the top 3.
- **Do not include the trigger question** for the planted instruction ([`README.md`](README.md)) in your main test set. It belongs to the injection task.

Write every question and expected source yourself, from the documents. Never ask a model to write the expected answers.
