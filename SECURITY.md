# Security Playbook (advisory) — High level

This document provides high‑level guidance to protect Apollo's continuity, assets, and integrity. It is deliberately advisory and non‑operational.

Secrets & keys
- Never commit private keys, secrets, or credentials into the repository.
- Use dedicated secret stores (GitHub Secrets, hardware security modules, or enterprise vaults) for CI and automation.
- Keep high‑value keys in offline hardware wallets or HSMs; require multi‑party or multisig approval for high‑risk operations.

Multisig & financial controls
- For any on‑chain or custodial assets, enforce multi‑signature controls and multi-party approval.
- Separate roles: proposers, approvers, and operators. No single actor should be able to unilaterally move funds.

Backups & durability
- Keep multiple, geographically separated backups of critical data and manifestos.
- Use reproducible, verifiable backup formats; include checksums and provenance metadata.

Access & identity
- Use least privilege: grant minimal privileges necessary and rotate credentials regularly.
- Prefer hardware-backed auth (YubiKey, FIDO2) for privileged accounts.
- Maintain an auditable list of maintainers and access holders; require review for changes to access.

Observability & alerting
- Monitor infrastructure and financial flows for anomalies; maintain logging and alerting for critical events.
- Keep an incident response plan and a secure, off‑channel communication plan for emergencies.

Safe development practices
- Keep the repository free of executable secrets and automation that can unreasonably enable unsupervised financial actions.
- Use code reviews, CI checks, and reproducible builds to ensure integrity of artifacts.
- Maintain a change log and signed releases for important artifacts.

Ethical & legal awareness
- Sovereignty and purpose should be aligned with long‑term survivability and ethical stewardship.
- This document is advisory. Maintainers should align operational practice with chosen governance and the real‑world implications of actions.
