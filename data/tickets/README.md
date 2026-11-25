# Support tickets for TicketSort

`make_tickets.py` makes **200 synthetic support tickets** for an online shop, each with its true labels: a category from a fixed list of 8, an urgency (low, medium or high) and a reference one-line summary.
TicketSort (P1) asks a model to label every ticket, then scores the model against these true labels.

Every ticket is made up. There are no names, email addresses, phone numbers or street addresses in them, so you may send them to a free-tier model.

## Make your tickets

In Git Bash:

```bash
cd ~/genai-ess-kit/data/tickets
uv run make_tickets.py --student <your student id> --out ~/<your course repository>/ticketsort/data/tickets.csv
```

It prints the count per category and per urgency. **The same student id always gives the same 200 tickets**, so your mentor can make your exact file again. Another student's id gives different products, order numbers, wording and counts.

- `--count 20` makes a smaller file for quick tests (about 1 in 10 is still ambiguous).
- `--self-test` checks the generator and exits.
- `sample.csv` is 20 tickets from the id `sample`, to look at before you run anything.

The generator uses only Python's standard library.

## The columns

The first five columns are the ones TicketSort uses: the ticket's **id**, its **text**, and the three **true labels**.

| Column | What it holds |
|---|---|
| `id` | The ticket id, `T0001` to `T0200`. Join your predictions to the true labels by this id, never by row order |
| `text` | The ticket as the customer wrote it. Email and web-form tickets start with `Subject: <subject> \|` and then the message; chat tickets are the message only, often in lower case. Some have typing mistakes, as real tickets do |
| `category` | **True category**: one of the 8 categories below |
| `urgency` | **True urgency**: `low`, `medium` or `high` |
| `summary` | **Reference summary**: one sentence, written to the rules below |
| `channel` | `email`, `web_form` or `chat` |
| `created_at` | When the ticket arrived, `YYYY-MM-DD HH:MM`, during one week in November 2026 |
| `order_id` | The order number if the ticket mentions one, otherwise empty |
| `alt_category` | For ambiguous tickets only: the second category a careful person could defend. Empty for the rest |

**Send the model only `text`.** The `category`, `urgency`, `summary` and `alt_category` columns are the answers: a prompt that contains them is cheating, and your evaluation would mean nothing. Never edit the file by hand; make it again with the command above if you need a fresh copy.

## The 8 categories

| Category | Use it when the customer… |
|---|---|
| `delivery` | asks where an order is: late, lost, tracking not moving, marked delivered but not received, part of the order missing in transit |
| `damaged_or_wrong` | received an item that is damaged, broken, unsafe, the wrong item, colour or size, or missing a part |
| `return` | wants to send back or swap an item that is not damaged (does not fit, changed their mind), or has a problem with a return pickup |
| `refund` | asks about money back: when it comes, how much, a refund that has not arrived |
| `payment` | has a problem paying or was charged wrongly: declined card, charged twice, paid with no order, discount code |
| `account` | has a problem with their account: sign-in, password reset, a possible break-in, changing the email, deleting the account, saved cards |
| `order_change` | wants to change or cancel an order that has not shipped yet, or move its delivery |
| `product_question` | asks about a product: size, fit, use, care, stock, warranty, compatibility |

### The labelling guide (how the true labels were chosen)

When a ticket touches two categories, the true label follows these rules, in this order:

1. **Money taken wrongly** (charged twice, charged for a cancelled order) is `payment`, even if they ask for the money back.
2. **Damaged, wrong or incomplete items** are `damaged_or_wrong`, even if the customer only asks to send the item back.
3. **An order that has not arrived** is `delivery`, unless the customer asks for their money back instead, which is `refund`.
4. **Changing an order or its delivery date** before it arrives is `order_change`.
5. **"I don't want it"** for an item that is fine is `return`, even if they say "money back".
6. **A question about whether something is normal or compatible** is `product_question`, until the customer says it is faulty.

About **1 ticket in 10 is ambiguous**: the text alone does not settle the category, and `alt_category` names the other reading. That is deliberate. Real tickets are like this, and it means 100% accuracy is very hard. When you study your confusion matrix, look at the ambiguous tickets separately.

## Urgency

Urgency is about **impact on the customer, not tone of voice**. A few low-urgency tickets are written in capitals with "URGENT!!!"; they are still low.

| Urgency | When |
|---|---|
| `high` | Money taken wrongly; a possible account break-in; a safety problem (sparks, burning smell, overheating); an order needed within two days; a cancellation for an order that ships today |
| `medium` | Something has gone wrong and needs action, but nothing is at risk today: a late or missing parcel, a damaged or wrong item, a refund overdue or short, a declined card, a sign-in problem, a missed return pickup, a change or cancellation before dispatch |
| `low` | Questions and requests with no harm yet: product questions, returns of unwanted items, refund timing still inside the normal window, tracking that has not updated but is not late, account changes, discount codes, adding or swapping an item in an order that is still processing |

## The reference summary

Each summary is one sentence of at most 120 characters that says **what happened and what the customer wants**, using only facts from the ticket (an order number only if the ticket gives one). Your model's summaries will be worded differently. P1 checks them with a written rubric, not by exact match.

## Example rows

From `sample.csv`:

| id | channel | text (shortened) | category | urgency | alt_category |
|---|---|---|---|---|---|
| T0001 | email | Subject: Return request \| I'd like to return the pair of trainers from order 420144. It is unused… | `return` | `low` | |
| T0003 | chat | The new blneder got very hot and the plug melted a little… | `damaged_or_wrong` | `high` | |
| T0004 | web_form | Subject: Discount code not working \| Hello, The code from your newsletter didn't apply to my phone charger… | `payment` | `low` | |
