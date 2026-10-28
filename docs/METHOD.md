# Method and limitations

ControlLedger uses deterministic rules to assign an illustrative `limited`, `elevated`, or `high` tier. Explanation text is generated from the matched rules; no language model decides the classification. Each stored record retains its rule version. Controls are mapped to tiers and evidence has explicit issue and expiry dates.

The P1 experiment starts with a low-autonomy FAQ assistant and seeds four scope changes: full automation, biometric data, a child audience, and benefits eligibility. The predeclared test requires every material change to reopen at least one relevant control while a version-only update must not trigger review.

The P2 experiment models shared evidence as immutable artifact versions and system-control dependencies as separately reviewable applicability claims. Five applicable claims initially reuse two artifacts, avoiding three duplicate submissions. Adding logging version 2 makes three version-1 links `superseded`; advancing the review date past the incident-plan expiry marks two more links `expired`. The predeclared acceptance test requires all five seeded stale dependencies to be found.

Important limitations:

- The tier labels and mappings are an educational synthesis, not legal advice or a determination under the EU AI Act, NIST AI RMF, or any jurisdiction.
- Real deployments require counsel and governance owners to validate definitions, applicability, and controls.
- Structured intake can be wrong or incomplete; the MVP does not independently verify disclosures.
- Evidence presence and freshness do not prove effectiveness.
- Shared evidence does not prove that a platform control operates correctly for every dependent system; applicability requires a system-specific rationale and remains a governance decision.
- Links are intentionally pinned to evidence versions. A newer version invalidates the prior claim until it is reviewed and relinked; automatic migration would hide scope changes.
- No authentication, authorization, file upload, malware scanning, or cryptographic audit log is implemented.
- The sample systems and evidence are synthetic.

