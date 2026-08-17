# Tag vocabulary — template

Upload this as your agent's knowledge source, once you've replaced the examples with
your own tags. Keep it in sync with `allowed_tags` and `allowed_types` in the
workflow's SETTINGS node — the agent generates from this document, the workflow
validates against those settings, and if the two disagree, valid tags get thrown away.

---

## Disposition — exactly one on every ticket

| Tag | Means |
|---|---|
| `action-required` | A human must read this and do something. |
| `no-action-required` | Safe to close unread. Nobody owes anyone a response. |

When uncertain, `action-required`. A real customer filed as noise is the expensive
mistake; an over-flagged newsletter costs someone two seconds.

## Topic tags — zero or more

### Noise

| Tag | Means |
|---|---|
| `third_party_notification` | A vendor's system notifying you — status pages, receipts, payout notices. |
| `newsletter` | A recurring marketing broadcast someone subscribed to. |
| `auto_reply` | Out-of-office and autoresponder mail. |
| `spam` | Backlink, guest-post, link-exchange and SEO promotion offers. |
| `bounce` | Delivery failure notices. |
| `vendor_outreach` | An unsolicited pitch from a company selling you something. |
| `internal_alert` | Your own automation alerting you — monitoring, cron failures. |

### Real work

Replace these with your own. The examples below are a starting point.

| Tag | Means |
|---|---|
| `bug_report` | A customer says something is broken. |
| `account_issue` | Login, access, seats, permissions. |
| `billing_issue` | Money between you and your customer — charges, invoices, refunds, plans. |
| `api_issue` | Problems using your API. |
| `integration_issue` | Problems connecting your product to something else. |
| `feature_request` | Wants something you don't do yet. |

## Boundaries that get confused

Spell these out for whichever of your tags overlap. The ones that reliably need it:

- **`newsletter` vs `vendor_outreach`** — a newsletter is a recurring broadcast someone subscribed to. A one-off cold pitch is `vendor_outreach`.
- **`billing_issue` vs `third_party_notification`** — `billing_issue` is money between you and your customer. A vendor's invoice to you, or a payout notice, is a third-party notification.
- **`internal_alert` vs customer-reported problems** — your own monitoring firing is `internal_alert` only. Don't add `bug_report` or `api_issue`; those are reserved for something a customer reported.

## Ticket Types

List your Freshdesk Types exactly as Freshdesk spells them, with one line of meaning
each, then the precedence order for the ones that overlap.

| Type | Means |
|---|---|
| `Question` | How to do something that already works. |
| `Problem/Bug reporting` | Something is broken. |
| `Feature Request` | Wants something you don't do yet. |
| `Billing` | Charges, invoices, refunds, plans, cancellations — between you and your customer. |
| `Sales Inquiry` | Pre-purchase interest. |
| `Newsletter` | A marketing broadcast. |
| `Other` | Nothing else fits, including machine-generated mail. |

**Precedence.** Billing beats Question and Problem/Bug when money between you and the
customer is the subject. Problem/Bug beats Question when they claim something is
broken. Sales Inquiry beats Question before purchase. Feature Request beats
Problem/Bug when the thing works as designed.

**Type must agree with disposition.** A `no-action-required` ticket can only be a
noise Type — `Other` or `Newsletter` in this list. If a business Type feels right on
a ticket you've called noise, the disposition is probably wrong.

## Worked examples

Add ten to twenty real tickets from your own queue with the answer for each. This is
the part that makes the difference on edge cases — the agent reads them when the rules
alone don't settle it.

| Subject | Disposition | Tags | Type |
|---|---|---|---|
| "Refund me please" | action-required | `billing_issue` | Billing |
| "STOP Minimizing Your AI Spend" (marketing blast) | no-action-required | `newsletter` | Newsletter |
| "Partnership Proposal" (cold SDK pitch) | no-action-required | `vendor_outreach` | Other |
| Payment processor "money request" notice | no-action-required | `third_party_notification` | Other |
| "Website widget unauthorized on iPad" | action-required | `bug_report` | Problem/Bug reporting |
