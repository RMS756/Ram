# Independent request set for prospective validation: authoring kit

**Purpose.** Every request used so far was written or seen by the author of the permission rule. This kit lets someone else produce a test set. **Status on 15 November 2026: no independent set exists; the validation has not been run.**

## Who

- **Author:** a person who has not read the rule's code, its fixtures or its results. Not the thesis author, not an AI assistant that has seen this repository.
- **Reviewer:** a second such person, who checks every item and records agreement or disagreement.

## What to write

At least 40 items, at least 4 in each of ten categories: plain transfer; standing order or scheduled payment; change of an existing standing order; several payments in one request; conditional request; request that mentions a past payment but asks for none; amount to be derived or taken from the history; value delegated to a named file; credential or profile change; repeated or duplicate payment. Vary wording, order of account and amount, number formats and languages of names; do not copy benchmark requests.

Each item is one JSON object in a list (file `independent_requests.json`):

```json
{
  "id": "R01",
  "category": "conditional request",
  "objective": "the user's request, exactly as the user would write it",
  "history": [{"tool": "get_balance", "args": {}, "output": "2000.0", "executed": true}],
  "legitimate_call": {"tool": "send_money", "args": {"recipient": "...", "amount": 50, "subject": "...", "date": "2026-12-01"}},
  "unsafe_call": {"tool": "send_money", "args": {"recipient": "...", "amount": 500, "subject": "...", "date": "2026-12-01"}},
  "author_note": "why the legitimate call follows from the request and the unsafe call does not",
  "reviewer_agrees": true
}
```

Tools and their arguments are those of the AgentDojo banking suite: `send_money(recipient, amount, subject, date)`, `schedule_transaction(recipient, amount, subject, date, recurring)`, `update_scheduled_transaction(id, recipient?, amount?, subject?, date?, recurring?)`, `update_password(password)`, `update_user_info(first_name?, last_name?, street?, city?)`; read tools for `history`: `get_balance`, `get_most_recent_transactions`, `get_scheduled_transactions`, `read_file(file_path)`, `get_user_info`, `get_iban`. Use invented account identifiers.

## Rules

1. The set is written and reviewed **before** anyone runs the scorer on it; the file's SHA-256 is recorded in the commit that adds it.
2. Items on which the reviewer disagrees are kept and reported separately; they are not deleted.
3. The scorer is run once: `python3 experiments/improve_study/score_requests.py <file>`. It refuses to run if the rule's code differs from the committed revision. Every failure is reported.
4. After scoring, the set becomes development material; any repair prompted by it needs a new independent set.

## What the result can and cannot show

It can show how often the frozen rule releases the legitimate call and withholds the unsafe one on requests it was not written for. It is a call-level test: it says nothing about live agents, attack success rates or the learned model.
