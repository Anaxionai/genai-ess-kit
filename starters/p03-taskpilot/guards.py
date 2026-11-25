"""Guards that run in TaskPilot's own code, before an action happens.

A rule that lives only in the system prompt is not a guard: the attack
harness (task 16) answers "y" to every confirmation, so only code stops it.
"""

# TODO(task 8): the one company domain in the kit's calendar file (kit data/calendar/README.md).
ALLOWED_DOMAINS: set[str] = set()


def check_email(args: dict) -> str | None:
    """Check a send_email call against the allow-list, before anything is sent.

    Input: the call's arguments, as the model sent them (`to`, `subject`, `body`).
    Output: None when the recipient's domain is in ALLOWED_DOMAINS, otherwise
    a short reason to refuse, such as "gmail.com is outside the company".
    Edge cases: compare domains without regard to case; an address with no
    "@", several addresses in one string or a look-alike domain
    (fernhill.example.evil.com) is refused.
    """
    raise NotImplementedError("TODO(task 8): return None for an allowed domain, else the reason")


def confirm_email(args: dict, ask=input) -> bool:
    """Ask the human before an email is sent. The default answer is No.

    Inputs: the call's arguments, and `ask`, a function like input() (tests pass
    `ask=lambda _: "n"`, the job runner `ask=lambda _: "y"`).
    Prints the recipient, the subject and the body, then asks
    `Send this email? [y/N]`.
    Output: True only for "y" (allow spaces and "Y"); anything else, an empty
    answer included, is False.
    """
    raise NotImplementedError("TODO(task 8): print the email, ask, and return True only for y")


# Task 16 fixes. The brief does not name these functions; keep these names or use your own.


def as_data(text: str) -> str:
    """Wrap a tool result in <data> tags that the result itself cannot close.

    Input: any tool result, which may contain an attack such as "</data> Now email ...".
    Output: the text inside one <data> ... </data> pair, with any <data> or
    </data> inside the result made harmless first, so the output holds exactly
    one closing tag, at the end. (You did the same for passages in DocAnswer.)
    """
    raise NotImplementedError("TODO(task 16): wrap the result so it cannot close the data tag")


def tools_for_job(job: str, declarations: list[dict]) -> list[dict]:
    """Offer send_email only when the job asks for an email.

    Inputs: the user's job text and every tool declaration.
    Output: the declarations to offer for this job: without send_email unless
    the job itself asks to email or send something. A document or calendar
    note that says "email ..." must never add it.
    """
    raise NotImplementedError("TODO(task 16): drop send_email unless the job asks for an email")
