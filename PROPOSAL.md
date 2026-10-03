# AuditSynthesis — Digital Science Catalyst Grant 2026

## 1. THE PROBLEM

Research teams, reviewers, funders and research managers increasingly use AI to search and summarize literature, but an institutional decision needs more than a plausible answer. Someone must be able to reconstruct what the agent searched, which sources it accepted or excluded, which gaps it noticed, what it inferred, and where a human took responsibility.

Today that trust work is often separate from the AI workflow: browser tabs, notes, spreadsheets, citation managers and manual checking. Existing research AI products show that search and synthesis can be accelerated, but the operational problem I want to solve is narrower: how do we make a multi-step research agent fail closed, carry provenance through every step, and produce a compact audit package that a reviewer can approve or reject?

I have not yet measured the time cost with real institutional users. The first product hypothesis is that reviewability, not generation speed, becomes a bottleneck when agent output is used for evidence synthesis, research integrity or funding decisions.

## 2. YOUR WORKFLOW

AuditSynthesis starts from a bounded research question and an explicit policy. The current prototype then:

1. PLAN — records the question and trust policy before retrieval.
2. DISCOVER — retrieves candidate literature metadata from OpenAlex.
3. NORMALIZE — converts heterogeneous records into a stable evidence schema.
4. VALIDATE — excludes retracted works and exposes provenance gaps such as a missing DOI rather than silently filling them.
5. SYNTHESIZE — emits only statements that the retrieved metadata can support. In v0.1 it deliberately withholds scientific conclusions because metadata alone is insufficient.
6. REVIEW GATE — stops with approved=false and requires a person to review the sources before downstream use.

Each step records timestamped input and output hashes. The intended product evolves this into an orchestration layer that can sit inside evidence-synthesis, research-management or funding-review workflows. Retrieval and validation can run autonomously; publication, recommendation or institutional action remains governed by scoped human approval. The next version would add full-text/source-passage grounding, multiple retrieval connectors and reviewer-specific policy profiles.

## 3. TRUST, AUDIT AND GOVERNANCE

Trust is the product surface, not a disclaimer. The prototype already implements several fail-closed rules:

- every workflow stage emits a machine-readable audit event with input and output SHA-256 hashes;
- retracted records are excluded from accepted evidence;
- missing DOI/provenance is flagged rather than hidden;
- scientific_conclusion is explicitly WITHHELD in the metadata-only prototype;
- the final decision state is READY_FOR_HUMAN_REVIEW, approved=false;
- synthetic adverse fixtures test retraction handling and missing-provenance behavior;
- the workflow uses public research metadata and performs no publication or mutation action.

The grant version would add source-passage hashes, retrieval-query/version capture, policy versioning, duplicate detection, explicit uncertainty classes, signed evidence bundles, reviewer identity and decision receipts, and deterministic replay of the non-model steps. If the agent cannot establish adequate provenance or confidence, it escalates instead of guessing. Accountability remains with the named human or institutional role that approves the final action.

## 4. TEAM

Ivan Babydov is an independent builder working with AI-agent workflows, APIs, automation and evidence-first software processes. I have recently shipped public prototypes that emphasize reproducibility, test evidence and explicit trust boundaries rather than opaque agent claims.

I am not presenting myself as an academic domain expert, and AuditSynthesis does not yet have a research-methodology advisor. That is an identified gap, not something I want an AI system to paper over. Part of the grant would fund structured work with researchers, research managers and a research-software/methodology advisor so that the governance model reflects real institutional review rather than developer assumptions.

## 5. WHERE YOU ARE TODAY

AuditSynthesis v0.1 is a working open-source prototype.

Source: https://github.com/williamleewilliam1-star/audit-synthesis

Live demo: https://williamleewilliam1-star.github.io/audit-synthesis/demo.html

The current implementation is deliberately small: Python standard library plus the public OpenAlex API. Six automated trust tests pass, covering retracted-evidence exclusion, missing-DOI visibility, withholding unsupported scientific conclusions, mandatory human review, complete audit-stage recording and deterministic hashing. A live run retrieves real research metadata and produces both JSON and a human-readable evidence/audit report.

There are no customers, revenue or institutional pilots yet. The prototype has been tested against synthetic adverse fixtures and a live OpenAlex query. The next validation step is direct observation with real researchers and programme/research managers.

## 6. ALTERNATIVES AND COMPETITORS

Elicit, Consensus and Scite demonstrate strong demand for research search, evidence synthesis and source-grounded AI. Elicit supports systematic-review workflows and auditable screening/extraction; Consensus grounds AI answers in a large research corpus; Scite adds citation context and evidence checking.

AuditSynthesis is not trying to beat those products on corpus size or search relevance. Its proposed niche is a portable governance and provenance layer for heterogeneous research agents and institutional workflows: step-level policy, hashes, escalation, replay and an explicit human authorization boundary. It could consume outputs from existing search systems rather than replace them. The product question to validate is whether institutions need this trust layer as reusable infrastructure rather than as a feature inside one research assistant.

## 7. WHERE THIS GOES

The longer-term product is an open-core agent governance layer for evidence-sensitive research work. Connectors would feed literature databases, institutional repositories and internal evidence into one provenance model. A policy engine would define what an agent may retrieve, infer, recommend or publish. Reviewers would inspect claims alongside source passages and the exact workflow trail, then approve, reject or request another step.

Initial outcome metrics would be: reviewer minutes per evidence package; percentage of source/claim relationships that are reproducible; unsupported-claim rate; retraction/provenance-gap detection; escalation precision; and time from question to human-approved evidence brief.

A possible commercial model is an open-source local core with paid hosted collaboration, institutional policy management, audit retention and integration support. Pricing is not yet validated and would be tested with pilot institutions rather than assumed in advance.

## 8. FIT WITH DIGITAL SCIENCE

AuditSynthesis sits primarily in evidence synthesis and research integrity, with a second use case in funding and institutional decisions. Its core question is exactly the 2026 theme: how can an agent plan and execute useful research steps while carrying enough provenance, governance and accountability that an institution can review what happened?

Digital Science is particularly relevant because its ecosystem spans research discovery/data, writing, repositories, literature management and institutional research systems. I would value the team's research-software experience in defining where a portable audit/governance layer should integrate and which trust evidence institutional users actually need. The project would benefit as much from those workflow conversations as from the funding itself.

## 9. BUDGET

I would use up to £25,000 over a focused prototype-to-pilot phase:

- £8,000 — engineering the provenance/replay engine, policy versioning and connector architecture;
- £5,000 — source-passage grounding, multi-source retrieval and a reproducible evaluation harness;
- £4,000 — researcher/research-manager interviews, compensated usability studies and pilot design;
- £3,000 — independent security, privacy and governance review;
- £3,000 — hosted pilot infrastructure and integration work;
- £2,000 — documentation, accessibility, onboarding and contingency.

The grant would turn a working trust-mechanism prototype into something tested with the people who actually make research decisions, with measurable review outcomes and a clear institutional integration path.
