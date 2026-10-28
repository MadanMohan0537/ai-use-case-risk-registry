# Evidence-driven backlog

| Priority | Feature | User problem and behavior | Dependencies | Success test | Risks and tradeoffs | Status |
|---|---|---|---|---|---|---|
| P1 | Scope-change reclassification | A low-risk system quietly becomes consequential. Diff purpose, users, autonomy, impact, domain, and data; reopen linked controls. | Versioned intake, control mapping | Reopen controls for all four seeded material changes with zero misses; ignore version-only bump | Illustrative rules require jurisdictional validation | Shipped |
| P2 | Control reuse with expiry | Teams duplicate platform evidence. Link shared, versioned evidence and invalidate dependents on expiry/change. | Dependency graph, applicability decision | Reduce duplicate submissions and find all seeded stale dependencies | Shared evidence may not apply locally; current MVP requires manual relinking after changes | Shipped |
| P2 | Reviewer disagreement queue | Product and governance owners disagree on scope fields. Preserve both views and require resolution. | Reviewer identity, immutable revisions | Measure resolution time and downstream tier changes | Adds process burden | Planned |
| P2 | Rule migration rehearsal | Framework mappings change. Replay saved systems under candidate rules and show tier/control transitions. | Versioned rules, replay corpus | Detect every seeded transition before promotion | Historical inventory may omit new patterns | Planned |
| P2 | Evidence quality rubric | A file can be current but irrelevant. Score provenance, scope, recency, and reviewer sign-off. | Typed artifacts, review labels | Reject seeded irrelevant evidence with bounded false review | Rubrics can become checkbox theater | Planned |
| P3 | Attestation sampling | Teams may under-report autonomy or impact. Select risk-weighted records for independent audit. | Audit outcomes, sampling policy | Higher material-misstatement yield than random sampling | Can create adversarial reporting behavior | Planned |
| P3 | Public inventory projection | Public-sector users need transparency without sensitive internals. Export approved fields with redaction review. | Field-level disclosure policy | Seeded secrets never appear; required public fields remain | Redaction may hide accountability context | Planned |
| P3 | Framework crosswalk provenance | NIST and legal obligations are not interchangeable. Store source, interpretation, and applicability per mapping. | Source registry, legal review | Reviewer can trace every control mapping to a versioned source | Maintenance cost and jurisdiction drift | Planned |
| P4 | Governance workload forecast | Evidence renewals cluster and overwhelm reviewers. Forecast expiries and simulate capacity. | Renewal history, queue model | Reduce missed renewals under frozen scenario | Forecasts inherit poor historical data | Planned |

## Further rigorous additions

| Priority | Feature | User problem and behavior | Dependencies | Success test | Risks and tradeoffs | Status |
|---|---|---|---|---|---|---|
| P2 | Dependency renewal queue | Evidence owners need to know which systems will lose coverage before expiry. Rank renewals by lead time, risk tier, and dependent count. | Shared dependency graph, ownership, renewal SLA | Every seeded near-expiry high-tier dependency enters the queue before its lead-time deadline | Large shared artifacts can dominate the queue; cap and explain priority | Planned |
| P2 | Applicability drift review | A system scope change can make previously reusable evidence inapplicable. Re-run applicability review when material intake fields change. | P1 scope diff, shared links, reviewer decisions | Detect all seeded scope changes that invalidate shared evidence with a bounded false-review rate | Conservative triggers increase governance workload | Planned |
| P2 | Evidence lineage signatures | Reviewers cannot distinguish an artifact update from silent replacement. Store content digests and predecessor links. | Immutable artifact storage, digest policy | Any seeded byte change produces a new version and invalidates pinned claims | Digests prove change, not quality or authorship | Planned |

Next slice: reviewer disagreement queue, because structured intake and applicability judgments currently have only one asserted view.

