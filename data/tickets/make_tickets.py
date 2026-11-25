# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""make_tickets.py: make 200 synthetic support tickets for an online shop, with true labels.

    uv run make_tickets.py --student <your student id>
    uv run make_tickets.py --student <your student id> --out data/tickets.csv
    uv run make_tickets.py --self-test

The same --student id always gives the same tickets. Every ticket is made up:
there are no names, emails, phone numbers or addresses in them.
Columns and labelling rules: see README.md in this folder.
"""

from __future__ import annotations

import argparse
import csv
import random
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

CATEGORIES = [
    "delivery",          # where is my order, late, lost, tracking
    "damaged_or_wrong",  # arrived damaged, broken, wrong item or a part missing
    "return",            # wants to send an item back or swap it (not damaged)
    "refund",            # asks about money back: status, amount, a refund not received
    "payment",           # payment failed, charged twice, coupon or checkout problem
    "account",           # sign-in, password, locked account, email change, delete account
    "order_change",      # change or cancel an order that has not shipped yet
    "product_question",  # a question before or after buying: size, fit, use, stock, warranty
]
URGENCIES = ["low", "medium", "high"]
# id and text are what you send to the model; category, urgency and summary are the true labels.
FIELDS = ["id", "text", "category", "urgency", "summary",
          "channel", "created_at", "order_id", "alt_category"]

# Products by kind, so a template only uses products that make sense for it.
PRODUCTS = {
    "electric": ["electric kettle", "wireless headphones", "desk lamp", "coffee grinder", "blender",
                 "air fryer", "table fan", "bluetooth speaker", "hair dryer", "rice cooker"],
    "shoes": ["pair of running shoes", "pair of trainers", "pair of sandals"],
    "clothes": ["rain jacket", "denim jacket", "kids' raincoat", "hoodie", "cotton shirt"],
    "device_extra": ["phone case", "smartwatch strap", "wireless mouse", "laptop sleeve",
                     "phone charger", "bluetooth speaker", "wireless headphones"],
    "home": ["hiking backpack", "yoga mat", "cotton bedsheet set", "steel water bottle",
             "building block set", "ceramic mug set", "office chair", "non-stick frying pan",
             "bookshelf", "storage box set"],
}
KIND_GROUPS = {
    "any": ["electric", "shoes", "clothes", "device_extra", "home"],
    "sized": ["shoes", "clothes"],
    "electric": ["electric"],
    "device": ["device_extra"],
    "hard": ["electric", "device_extra", "home"],
}
COLOURS = ["black", "blue", "grey", "green", "red", "white", "navy", "beige"]
SHOE_SIZES = ["6", "7", "8", "9", "10", "11"]
CLOTHES_SIZES = ["XS", "S", "M", "L", "XL"]
COURIERS = ["the courier", "the delivery company", "the delivery partner"]

OPENERS = ["Hi,", "Hello,", "Hello team,", "Hi there,", "Good morning,", "Dear support,", "", ""]
CLOSERS = ["Thanks", "Thank you", "Regards", "Thanks in advance", "Please help", "", "", "Cheers"]


def pick(rng: random.Random, options):
    return options[rng.randrange(len(options))]


# ---------------------------------------------------------------------------
# Templates. Each one gives: subject options, body segments (a list of option
# lists, one option is picked from each), urgency, and a summary pattern.
# Slots: {order} {product} {product2} {days} {amount} {colour} {size} {courier}
# ---------------------------------------------------------------------------
CLEAR = {
    "delivery": [
        dict(subject=["Where is my order?", "Order {order} not arrived", "Late delivery"],
             body=[["My order {order} was due {days} days ago and it still has not arrived.",
                    "I ordered {a_product} (order {order}) and it is now {days} days late.",
                    "Order {order} should have been here {days} days ago."],
                   ["The tracking page has not changed since it left the warehouse.",
                    "Tracking just says 'in transit'.", "Can you tell me when it will come?",
                    "Could you check what is going on?"]],
             urgency="medium",
             summary="Order {order} is {days} days late; customer wants a delivery date."),
        dict(subject=["Tracking not updating", "Tracking stuck for order {order}"],
             body=[["The tracking for order {order} has said 'label created' for two days.",
                    "Tracking for my {product} has not moved since yesterday."],
                   ["It is not late yet, I just want to know it has actually been sent.",
                    "Delivery date says {daydate}, so no rush, but is it on its way?"]],
             urgency="low",
             summary="Customer asks whether order {order} has shipped; tracking has not updated, not yet late."),
        dict(subject=["Need it by {daydate}!", "Gift needed by {daydate}"],
             body=[["I ordered {a_product} as a birthday present and the party is on {daydate}.",
                    "Order {order} is a gift for {daydate}, which is the day after tomorrow."],
                   ["The estimate now says next week. Is there any way to speed it up?",
                    "Tracking shows it is delayed. Please tell me if it will make it."]],
             urgency="high",
             summary="A gift order is delayed and needed within two days; customer asks to speed it up."),
        dict(subject=["Parcel marked delivered but not here", "Says delivered, nothing received"],
             body=[["Tracking for order {order} says delivered yesterday but there is nothing at my door.",
                    "{courier} marked my {product} as delivered but I never got it."],
                   ["I checked with the neighbours and the building reception.",
                    "Nobody here signed for it."]],
             urgency="medium",
             summary="Order {order} shows as delivered but the customer has not received it."),
        dict(subject=["", ""],
             body=[["hey where is {order}??", "my {product} still not here, order {order}",
                    "order {order} - still waiting"],
                   ["its been {days} days", "{days} days late now", "still nothing after {days} extra days"]],
             urgency="medium",
             summary="Customer is chasing order {order}, {days} days overdue."),
    ],
    "damaged_or_wrong": [
        dict(kind="hard", subject=["Item arrived broken", "Damaged {product}", "Broken on arrival"],
             body=[["My {product} from order {order} arrived broken.",
                    "The box was crushed and the {product} inside is cracked.",
                    "Order {order} came today and the {product} is damaged."],
                   ["Please send a replacement.", "What do I do now?", "I have kept the packaging."]],
             urgency="medium",
             summary="{product} in order {order} arrived damaged; customer wants a replacement."),
        dict(kind="sized", subject=["Wrong item sent", "This is not what I ordered", "Wrong colour/size"],
             body=[["I ordered the {colour} {product} in size {size} but got a different colour.",
                    "Order {order} contained {a_product2} instead of the {product} I ordered.",
                    "I received size {size2} but I ordered size {size}."],
                   ["Can you send the right one?", "Please fix this.", "Not happy."]],
             urgency="medium",
             summary="Customer received the wrong item, colour or size and wants the right one."),
        dict(subject=["Part missing", "Missing pieces"],
             body=[["The {product} from order {order} came with a part missing.",
                    "Some pieces are missing from my {product}.",
                    "One of the parts listed on the box for the {product} is not there."],
                   ["I can't use it without it.", "Could you post the missing part?"]],
             urgency="medium",
             summary="{product} in order {order} arrived with a part missing; customer asks for it."),
        dict(kind="electric", subject=["Burning smell from {product}", "Sparks from new {product} - unsafe"],
             body=[["I plugged in the {product} from order {order} and it gave off a burning smell and a spark.",
                    "The new {product} got very hot and the plug melted a little."],
                   ["I have unplugged it and I am not using it.", "This is dangerous, please advise."]],
             urgency="high",
             summary="{product} from order {order} sparked or overheated; a safety issue, customer stopped using it."),
    ],
    "return": [
        dict(subject=["Return request", "How do I return this?", "Want to send back {product}"],
             body=[["I'd like to return the {product} from order {order}.",
                    "The {product} doesn't fit, so I want to send it back.",
                    "I changed my mind about the {product} (order {order})."],
                   ["It is unused and in the original box.", "How do I get a return label?",
                    "What are the steps?"]],
             urgency="low",
             summary="Customer wants to return an unused {product} from order {order} and asks how."),
        dict(kind="sized", subject=["Exchange for another size", "Swap size"],
             body=[["The {product} in size {size} is too small.",
                    "Can I swap the {product} from order {order} for size {size}?"],
                   ["I'd like to exchange it for a bigger one.", "Is an exchange possible?"]],
             urgency="low",
             summary="Customer wants to exchange the {product} from order {order} for another size."),
        dict(subject=["Return window question", "Is it too late to return?"],
             body=[["I bought {a_product} about four weeks ago and never used it.",
                    "Order {order} arrived 25 days ago."],
                   ["Can I still return it?", "Am I still inside the return period?"]],
             urgency="low",
             summary="Customer asks if an unused {product} bought about four weeks ago can still be returned."),
        dict(subject=["Return pickup missed", "Courier didn't collect my return"],
             body=[["I booked a pickup for my return of the {product} but nobody came.",
                    "The return pickup for order {order} was missed twice."],
                   ["Please book another one.", "What should I do now?"]],
             urgency="medium",
             summary="Return pickup for order {order} was missed; customer asks to rebook it."),
    ],
    "refund": [
        dict(subject=["Refund not received", "Where is my refund?"],
             body=[["I returned the {product} {days2} days ago and the refund of {amount} still hasn't arrived.",
                    "You confirmed my return for order {order} {days2} days ago but the {amount} has not come back."],
                   ["Your site says 5 to 7 days.", "Please check.", "When will I get it?"]],
             urgency="medium",
             summary="Refund of {amount} for a return made {days2} days ago has not arrived."),
        dict(subject=["Refund status", "Question about my refund"],
             body=[["I sent back my {product} on Monday.", "My return for order {order} was received yesterday."],
                   ["How long does the refund usually take?", "Just checking when to expect the money."]],
             urgency="low",
             summary="Customer asks how long the refund for order {order} will take; not yet overdue."),
        dict(subject=["Partial refund wrong", "Refund amount is wrong"],
             body=[["I got a refund for order {order} but it was {amount_small} instead of {amount}.",
                    "You refunded less than I paid for the {product}."],
                   ["Was the delivery charge taken off?", "Please refund the difference."]],
             urgency="medium",
             summary="Customer says the refund for order {order} was less than they paid; wants the difference."),
    ],
    "payment": [
        dict(subject=["Charged twice!", "Double payment", "Two charges for one order"],
             body=[["I was charged {amount} twice for order {order}.",
                    "My bank shows two payments of {amount} but I only placed one order."],
                   ["Please refund the extra payment.", "Please fix this today."]],
             urgency="high",
             summary="Customer was charged twice ({amount}) for order {order}; wants the duplicate returned."),
        dict(subject=["Payment failed but money taken", "Paid but no order"],
             body=[["The checkout said payment failed, but {amount} has left my account.",
                    "I paid {amount} and got an error page; there is no order in my account."],
                   ["Did the order go through?", "Where has my money gone?"]],
             urgency="high",
             summary="Payment of {amount} was taken but no order was created; customer asks where the money is."),
        dict(subject=["Card declined", "Can't pay"],
             body=[["My card keeps getting declined at checkout.",
                    "Payment for the {product} fails every time I try."],
                   ["The card works on other sites.", "Is there another way to pay?"]],
             urgency="medium",
             summary="Customer's card is declined at checkout; asks for another way to pay."),
        dict(subject=["Discount code not working", "Coupon didn't apply"],
             body=[["The code from your newsletter didn't apply to my {product}.",
                    "I entered the 10% discount code but the total didn't change."],
                   ["Can you apply it?", "Is the code still valid?"]],
             urgency="low",
             summary="Discount code did not apply at checkout; customer asks for it to be applied."),
    ],
    "account": [
        dict(subject=["Can't log in", "Login problem", "Password reset email not arriving"],
             body=[["I can't sign in to my account.", "The password reset email never arrives."],
                   ["I've checked spam.", "I've tried three times.", "Can you help me get back in?"]],
             urgency="medium",
             summary="Customer cannot sign in; the password reset email does not arrive."),
        dict(subject=["Someone else used my account", "Account hacked?", "Order I didn't place"],
             body=[["There is an order in my account that I did not place.",
                    "I got an email that my password was changed, but I didn't change it."],
                   ["I think someone has got into my account.", "Please lock it now."]],
             urgency="high",
             summary="Possible account takeover: unknown order or password change; customer asks to lock the account."),
        dict(subject=["Change my email address", "Update account email"],
             body=[["I want to change the email address on my account.",
                    "How do I update the email I sign in with?"],
                   ["I don't use the old one any more.", ""]],
             urgency="low",
             summary="Customer wants to change the email address on their account."),
        dict(subject=["Delete my account", "Close account"],
             body=[["Please delete my account and my data.", "I want to close my account."],
                   ["I don't shop here any more.", "How long does it take?"]],
             urgency="low",
             summary="Customer asks for their account and data to be deleted."),
    ],
    "order_change": [
        dict(subject=["Cancel my order", "Please cancel order {order}"],
             body=[["Please cancel order {order}, I ordered by mistake.",
                    "I want to cancel the {product} I ordered this morning."],
                   ["It hasn't shipped yet.", "The status still says 'processing'."]],
             urgency="medium",
             summary="Customer asks to cancel order {order} before it ships."),
        dict(subject=["Change delivery address", "Wrong address on order {order}"],
             body=[["I put my old address on order {order}.",
                    "I need to change the delivery address for my {product}."],
                   ["Can you update it before it is sent?", "It hasn't shipped yet."]],
             urgency="medium",
             summary="Customer needs the delivery address on order {order} changed before dispatch."),
        dict(subject=["Cancel before it ships today!", "Urgent cancel - ships today"],
             body=[["Order {order} says it will be dispatched today and I need to cancel it now.",
                    "I ordered the wrong {product} and it ships this afternoon."],
                   ["Please stop it before it goes.", "Please cancel it right away."]],
             urgency="high",
             summary="Customer must cancel order {order} before it is dispatched today."),
        dict(subject=["Add an item to my order", "Change item in order"],
             body=[["Can I add {a_product2} to order {order} so it comes together?",
                    "I want to change the {product} in order {order} to the {colour} one."],
                   ["It's still processing.", "No rush."]],
             urgency="low",
             summary="Customer wants to change the items in order {order} while it is still processing."),
    ],
    "product_question": [
        dict(kind="sized", subject=["Size question", "Does it run small?"],
             body=[["Does the {product} run true to size?", "I'm usually a size {size}. Which size should I get in the {product}?"],
                   ["Thanks.", "I don't want to have to return it."]],
             urgency="low",
             summary="Customer asks about sizing for the {product} before buying."),
        dict(subject=["Back in stock?", "When will {product} be available?"],
             body=[["The {colour} {product} says out of stock.", "Will the {product} come back in stock?"],
                   ["Is there a date?", "Can I be told when it's back?"]],
             urgency="low",
             summary="Customer asks when the {product} will be back in stock."),
        dict(kind="electric", subject=["Warranty question", "How long is the warranty?"],
             body=[["What warranty comes with the {product}?", "Is the {product} covered by a warranty?"],
                   ["Mine is six months old.", "Thinking of buying one."]],
             urgency="low",
             summary="Customer asks about the warranty on the {product}."),
        dict(subject=["How do I use this?", "Instructions for {product}"],
             body=[["How do I clean the {product}?", "Is there a manual for the {product}?",
                    "Can the {product} be used every day?"],
                   ["There was no leaflet in the box.", "Couldn't find it on the website."]],
             urgency="low",
             summary="Customer asks how to use or care for the {product}."),
    ],
}

# Tickets where two categories can be defended. The label follows the
# labelling guide in README.md; alt_category holds the other reading.
AMBIGUOUS = [
    dict(category="refund", alt="delivery", urgency="medium",
         subject=["Still not here, refund please", "Fed up waiting"],
         body=[["My {product} (order {order}) is {days} days late.", "Order {order} never came."],
               ["Honestly I just want my money back now.", "Just refund me, I don't want it any more."]],
         summary="Order {order} has not arrived and the customer asks for a refund instead."),
    dict(category="damaged_or_wrong", alt="return", urgency="medium", kind="hard",
         subject=["Want to return this", "Sending it back"],
         body=[["The {product} arrived with a scratch across the front.", "There's a dent in the {product} I got."],
               ["I just want to return it.", "Can I send it back please?"]],
         summary="{product} in order {order} arrived scratched or dented; customer wants to send it back."),
    dict(category="order_change", alt="return", urgency="low", kind="sized",
         subject=["Change size", "Different size please"],
         body=[["I ordered the {product} in size {size} yesterday.", "Order {order}: I picked the wrong size."],
               ["Can I get size {size2} instead?", "Can this be changed to {size2}?"]],
         summary="Customer wants order {order} changed to size {size2}; it is not clear if it has shipped."),
    dict(category="payment", alt="refund", urgency="high",
         subject=["Money taken after cancelling", "Charged for a cancelled order"],
         body=[["I cancelled order {order} last week but you still took {amount}.",
                "The order was cancelled but my card was charged {amount} today."],
               ["I want it back.", "Please sort this out."]],
         summary="Customer was charged {amount} for order {order}, which they had cancelled; wants the money back."),
    dict(category="account", alt="payment", urgency="medium",
         subject=["Saved card problem", "Can't remove my card"],
         body=[["I can't remove an old card from my account.", "My saved card won't update in my profile."],
               ["It keeps trying to charge the old one.", "Every time I try I get an error."]],
         summary="Customer cannot remove or update a saved card in their account."),
    dict(category="product_question", alt="damaged_or_wrong", urgency="low", kind="electric",
         subject=["Is this normal?", "Strange noise"],
         body=[["My new {product} makes a humming noise.", "The {product} smells a bit of plastic."],
               ["Is that normal for this model?", "Is that expected or is it faulty?"]],
         summary="Customer asks whether a noise or smell from the new {product} is normal."),
    dict(category="delivery", alt="damaged_or_wrong", urgency="medium",
         subject=["Only half my order came", "Parcel missing"],
         body=[["I ordered the {product} and {a_product2} but only one parcel arrived.",
                "Order {order} said two parcels and I only got one."],
               ["Is the other one still coming?", "Where's the rest?"]],
         summary="Only part of order {order} arrived; customer asks if the rest is still on its way."),
    dict(category="return", alt="refund", urgency="low",
         subject=["Don't want it", "Money back?"],
         body=[["The {product} isn't what I expected.", "I don't like the {colour} {product} in person."],
               ["Can I have my money back?", "How do I get a refund?"]],
         summary="Customer does not want the {product} and asks how to get their money back."),
    dict(category="order_change", alt="delivery", urgency="medium",
         subject=["Will be away", "Delivery while I'm away"],
         body=[["I'm away from {daydate} for a week and order {order} is due then.",
                "Nobody will be home when the {product} is due."],
               ["Can you hold it or deliver it later?", "Can the delivery date be moved?"]],
         summary="Customer will be away when order {order} is due and asks to move the delivery."),
    dict(category="product_question", alt="return", urgency="low", kind="device",
         subject=["Does it work with my phone?", "Compatibility"],
         body=[["I bought the {product} but I'm not sure it works with my phone.",
                "Will the {product} work with an older laptop?"],
               ["If not I'll send it back.", "Otherwise it's no use to me."]],
         summary="Customer asks if the {product} is compatible with their device; may return it if not."),
]

# A few low-urgency tickets written in an angry tone: urgency is about impact, not tone.
SHOUTY_PREFIX = ["URGENT!!! ", "PLEASE ANSWER!!! ", "Third time asking. "]


def typo(rng: random.Random, text: str) -> str:
    """Swap two neighbouring letters in one word, as real people do when they type fast."""
    words = text.split(" ")
    long_words = [i for i, w in enumerate(words) if len(w) > 4 and w.isalpha()]
    if not long_words:
        return text
    i = pick(rng, long_words)
    w = words[i]
    j = rng.randrange(1, len(w) - 2)
    words[i] = w[:j] + w[j + 1] + w[j] + w[j + 2:]
    return " ".join(words)


def with_article(noun: str) -> str:
    return ("an " if noun[0] in "aeiou" else "a ") + noun


def make_slots(rng: random.Random, created: datetime, kind: str = "any") -> dict[str, str]:
    group = pick(rng, KIND_GROUPS[kind])
    product = pick(rng, PRODUCTS[group])
    product2 = pick(rng, [p for g in PRODUCTS.values() for p in g if p != product])
    size, size2 = rng.sample(SHOE_SIZES if group == "shoes" else CLOTHES_SIZES, 2)
    amount = rng.randrange(12, 260) + pick(rng, [0, 0.49, 0.99])
    return {
        "order": f"{rng.randrange(400000, 499999)}",
        "product": product,
        "product2": product2,
        "a_product": with_article(product),
        "a_product2": with_article(product2),
        "days": str(rng.randrange(3, 13)),
        "days2": str(rng.randrange(11, 25)),
        "amount": f"${amount:,.2f}",
        "amount_small": f"${amount * pick(rng, [0.5, 0.7, 0.8]):,.2f}",
        "colour": pick(rng, COLOURS),
        "size": size,
        "size2": size2,
        "courier": pick(rng, COURIERS).capitalize(),
        "daydate": (created + timedelta(days=2)).strftime("%A %d %B").replace(" 0", " "),
    }


def render(rng: random.Random, template: dict, slots: dict, channel: str) -> tuple[str, str]:
    subject = pick(rng, template["subject"]).format(**slots)
    sentences = [pick(rng, options).format(**slots) for options in template["body"]]
    body = " ".join(s for s in sentences if s)
    if channel == "chat":
        subject = ""
        body = body.lower() if rng.random() < 0.5 else body
    else:
        opener, closer = pick(rng, OPENERS), pick(rng, CLOSERS)
        body = " ".join(x for x in (opener, body, closer) if x)
    if rng.random() < 0.15:
        body = typo(rng, body)
    return subject, body


def make_tickets(student: str, count: int = 200) -> list[dict[str, str]]:
    rng = random.Random(f"genai-ess-tickets|{student}")
    n_ambiguous = round(count * 0.10)
    n_clear = count - n_ambiguous

    # Category counts differ a little per student, but every category gets enough tickets.
    weights = [rng.uniform(0.8, 1.2) for _ in CATEGORIES]
    raw = [w / sum(weights) * n_clear for w in weights]
    counts = [int(x) for x in raw]
    for i in sorted(range(len(raw)), key=lambda k: raw[k] - counts[k], reverse=True)[: n_clear - sum(counts)]:
        counts[i] += 1

    plan: list[tuple[str, dict, bool]] = []
    for category, n in zip(CATEGORIES, counts):
        for _ in range(n):
            plan.append((category, pick(rng, CLEAR[category]), False))
    ambiguous_order = AMBIGUOUS * (n_ambiguous // len(AMBIGUOUS) + 1)
    rng.shuffle(ambiguous_order)
    for template in ambiguous_order[:n_ambiguous]:
        plan.append((template["category"], template, True))
    rng.shuffle(plan)

    start = datetime(2026, 11, 2, 7, 0)
    minutes = sorted(rng.sample(range(0, 7 * 24 * 60, 3), count))
    seen_bodies: set[str] = set()
    tickets = []
    for i, (category, template, ambiguous) in enumerate(plan):
        created = start + timedelta(minutes=minutes[i])
        channel = pick(rng, ["email", "email", "web_form", "chat"])
        for _ in range(20):  # avoid two identical bodies
            slots = make_slots(rng, created, template.get("kind", "any"))
            subject, body = render(rng, template, slots, channel)
            if body not in seen_bodies:
                break
        seen_bodies.add(body)
        urgency = template["urgency"]
        if not ambiguous and urgency == "low" and channel != "chat" and rng.random() < 0.08:
            body = pick(rng, SHOUTY_PREFIX) + body  # loud tone, still low impact
        has_order = slots["order"] in body + subject
        summary = template["summary"]
        if not has_order:  # the summary only names what the ticket says
            summary = summary.replace("order {order}", "the order").replace("Order {order}", "The order")
        tickets.append({
            "id": f"T{i + 1:04d}",
            "text": f"Subject: {subject} | {body}" if subject else body,
            "channel": channel,
            "created_at": created.strftime("%Y-%m-%d %H:%M"),
            "order_id": slots["order"] if has_order else "",
            "category": category,
            "urgency": urgency,
            "summary": capitalise(summary.format(**slots)),
            "alt_category": template.get("alt", "") if ambiguous else "",
        })
    return tickets


def capitalise(text: str) -> str:
    return text[:1].upper() + text[1:]


def write_csv(tickets: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(tickets)


def self_test() -> None:
    a, b, c = make_tickets("s1"), make_tickets("s1"), make_tickets("s2")
    assert a == b, "same student id must give the same tickets"
    assert a != c, "different student ids must give different tickets"
    for tickets in (a, c):
        assert len(tickets) == 200
        cats = Counter(t["category"] for t in tickets)
        assert set(cats) == set(CATEGORIES) and min(cats.values()) >= 15, cats
        assert {t["urgency"] for t in tickets} == set(URGENCIES)
        ambiguous = sum(1 for t in tickets if t["alt_category"])
        assert ambiguous == 20, ambiguous
        assert len({t["text"] for t in tickets}) == 200, "texts must be unique"
        assert all(t["summary"] and len(t["summary"]) <= 120 for t in tickets)
        assert all("{" not in t["text"] + t["summary"] for t in tickets)
        assert all("@" not in t["text"] for t in tickets), "no email addresses"
    print("self-test passed: 200 tickets, 8 categories, 3 urgencies, 20 ambiguous, deterministic")


def main() -> int:
    parser = argparse.ArgumentParser(description="Make synthetic support tickets with true labels.")
    parser.add_argument("--student", help="your student id; the same id always gives the same tickets")
    parser.add_argument("--out", default="tickets.csv", help="output CSV file (default: tickets.csv)")
    parser.add_argument("--count", type=int, default=200, help="how many tickets (default: 200)")
    parser.add_argument("--self-test", action="store_true", help="check the generator and exit")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.student:
        parser.error("--student is required (use your student id)")
    tickets = make_tickets(args.student, args.count)
    write_csv(tickets, Path(args.out))
    cats = Counter(t["category"] for t in tickets)
    urg = Counter(t["urgency"] for t in tickets)
    print(f"Wrote {len(tickets)} tickets to {args.out}")
    print("Categories: " + ", ".join(f"{c} {cats[c]}" for c in CATEGORIES))
    print("Urgency:    " + ", ".join(f"{u} {urg[u]}" for u in URGENCIES))
    print(f"Ambiguous (alt_category set): {sum(1 for t in tickets if t['alt_category'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
