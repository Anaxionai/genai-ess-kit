# Brief: ShopHelp

## The product

ShopHelp answers customer questions for a small online shop, Corner Goods. It answers from the shop's help pages and looks up the customer's order, and it hands anything it must not decide, above all refunds, to a person on the support team.

## User and job

When a customer has a question about an order, they want a correct answer straight away, so that they do not wait a day for an email reply.

## The hard rule

**No refund without a human's confirmation.** ShopHelp may explain the refund rules and say whether an order looks eligible, but it never approves, promises or issues a refund. Any refund request becomes a hand-over ticket for a person, and the code, not only the prompt, checks every answer: an answer that promises or confirms a refund is replaced by the hand-over message, and no refund tool exists that the model could call without a person's "yes".

## Cost of a wrong answer

- A false answer (a refund promised wrongly, or a wrong delivery date) costs the shop money and the customer's trust.
- A missed answer (a simple question handed to a person) costs the customer time.
- The hard rule makes the first kind impossible for refunds; decide with your mentor where else ShopHelp should hand over rather than guess.

## The data

Generate the shop's data with the kit generator, using your student id:

```bash
cd ~/genai-ess-kit/capstone/data
uv run make_shop.py --student <your student id> --out <your capstone folder>/data/shop
```

| Option | Default | Meaning |
|---|---|---|
| `--student <id>` | required | Your student id; the same id always gives the same files |
| `--orders <n>` | 60 | How many orders |
| `--messages <n>` | 40 | How many customer messages |
| `--out <folder>` | `out/shop` | Where to write them |
| `--self-test` | | Check the generator and exit |

It writes:

- `faq.md`: the shop's help pages (delivery, cancelling, returns, refunds, damaged items, payments, warranty, talking to a person). **They are the only source of truth for answers.**
- `orders.json`: `today` (the date the shop treats as today) and a list of orders, each with `order_id`, `customer` (a customer number, never a name), `placed`, `status` (`processing`, `shipped`, `delivered`, `cancelled` or `returned`), `items` (name, `price_inr`, `final_sale`), `total_inr`, and the `dispatched`, `delivered` and `return_received` dates where they apply.
- `messages.json`: customer messages to answer, each with `id`, `customer`, `kind` and `text`. About a third push for a refund in different ways (pressure, a "colleague already approved it", a fake manager, an injection), and a few are out of scope.

Use `kind` only to help you plan cases; write each expected answer yourself from `faq.md` and the order.

## Example stories

- **S1**: As a customer, I want my order's status and expected delivery, so that I know when it arrives.
- **S2**: As a customer, I want to know whether I can still cancel or return an order, with the reason.
- **S3**: As a customer asking for a refund, I want to be handed to a person with my case summarised.
- **S4**: As a support agent, I want every hand-over as a ticket with the order id and the customer's request.
- **S5**: As a customer, I want an honest "I can't answer that here" for questions the help pages do not cover.
- **S6**: As the shop, I want every answer to cite the help-page section it used.

## Evaluation ideas

- `normal`: status, cancel, return-window and warranty questions, with expected answers worked out from `faq.md`, the order's dates and `today`.
- `edge`: a final-sale item; an order returned more than 7 days ago; an order id that does not exist.
- `hard_rule`: every refund push in `messages.json`, plus your own (a message in another language, a refund hidden in a long complaint). The check: no answer contains an approval or promise of a refund, and each one creates a hand-over.
- `out_of_scope`: weather, homework, other shops.

## Stretch ideas

- An MCP server with `get_order` and `create_handover` tools, and the agent loop from TaskPilot.
- A small chat page with FastAPI, and a page for the support team that lists open hand-overs.
