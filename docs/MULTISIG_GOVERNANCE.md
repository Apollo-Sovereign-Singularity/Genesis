# Multisig Governance Template (advisory)

Purpose
- Describe a human-in-the-loop, auditable multisig process for on‑chain or custodial operations.
- Maintain safety via separation of proposer, approver, and operator roles.
- Provide off‑channel verification and emergency response.

Roles
- Proposer: creates a proposal, records purpose, amount, recipients, and justification.
- Approver(s): sign off on proposals. Require N-of-M approvals (recommended 3-of-5 for high-value ops).
- Executor/Operator: performs the approved operation (executes the on‑chain transaction or custodial transfer) — must not act without verifiable approvals.
- Auditor / Watcher: independent observers who monitor and log operations.

Proposal workflow
1. Proposer opens a Proposal Issue (template) with:
   - unique proposal id
   - timestamp
   - purpose and rationale
   - requested action (detailed)
   - expected recipients and amounts
   - proposed multisig threshold and list of approvers
   - off‑chain verification method (e.g., PGP-signed confirmation, verbal code, video of keyholders)
2. Approvers review and add signed confirmations to the issue (GPG/PGP or other agreed signature).
3. When threshold is met, the Operator executes the operation and posts transaction details and provenance to the Issue.
4. Auditors verify and record the transaction hash, receipts, and confirmations.

Signing & verification
- Prefer hardware-backed signing (YubiKey, OpenPGP on smartcard) for maintainers.
- Use reproducible signatures (ASCII-armored PGP or similar) attached to the proposal for provenance.
- Maintain the public keys of approvers in the repo (or an auditable registrar file) but keep private keys offline.

Emergency & recovery
- Define emergency thresholds, e.g., emergency multisig (higher threshold or separate keys).
- Maintain off‑channel emergency procedures (☎ secure phone list, out‑of-band verification).
- Keep documented backups of critical artifacts (signed and checksummed) in geographically separated storage.

Auditing & logging
- All operations and approvals must be logged with timestamps, signatures, and provenance.
- Consider periodic independent audits of governance processes and keyholder lists.

Notes & ethics
- This is advisory. Maintain legal awareness and consider jurisdictional implications for custody and transfers.
- No party should be able to unilaterally drain funds or take irreversible control.
