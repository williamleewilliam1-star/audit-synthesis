# AuditSynthesis

AuditSynthesis is a prototype auditable evidence-synthesis agent for the 2026 Digital Science Catalyst Grant theme: Agentic Workflows You Can Trust.

The v0.1 workflow plans a bounded research question, discovers public literature metadata through OpenAlex, normalizes evidence, excludes retracted works, flags provenance gaps such as missing DOI, synthesizes only metadata-supported statements, and stops at an explicit human review gate.

AuditSynthesis intentionally withholds scientific conclusions in v0.1. The point of the prototype is trust plumbing: provenance, auditability, deterministic policy checks, escalation and accountability before a research decision is made.

Run:

python3 -m unittest discover -s tests -v
python3 audit_synthesis.py "agentic research workflows provenance audit trail"

Live demo: https://williamleewilliam1-star.github.io/audit-synthesis/

Data source: OpenAlex public API. No API key, personal data, wallet or write action is required.
