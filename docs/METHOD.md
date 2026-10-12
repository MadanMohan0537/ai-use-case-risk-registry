# Method and limitations

ControlLedger uses deterministic rules to assign an illustrative `limited`, `elevated`, or `high` tier. Explanation text is generated from the matched rules; no language model decides the classification. Each stored record retains its rule version. Controls are mapped to tiers and evidence has explicit issue and expiry dates.

The P1 experiment starts with a low-autonomy FAQ assistant and seeds four scope changes: full automation, biometric data, a child audience, and benefits eligibility. The predeclared test requires every material change to reopen at least one relevant control while a version-only update must not trigger review.

Important limitations:

- The tier labels and mappings are an educational synthesis, not legal advice or a determination under the EU AI Act, NIST AI RMF, or any jurisdiction.
- Real deployments require counsel and governance owners to validate definitions, applicability, and controls.
- Structured intake can be wrong or incomplete; the MVP does not independently verify disclosures.
- Evidence presence and freshness do not prove effectiveness.
- No authentication, authorization, file upload, malware scanning, or cryptographic audit log is implemented.
- The sample systems and evidence are synthetic.
