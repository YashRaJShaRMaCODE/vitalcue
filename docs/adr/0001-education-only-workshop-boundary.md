# ADR 0001: Keep VitalCue an education-only workshop demo

- **Status:** Accepted for the current validation phase
- **Date:** 2026-11-17
- **Decision owners:** Product owner / repository maintainer

## Context

VitalCue exposes a binary health-risk label, a prototype score, a BMI reference, and food/activity examples. The README states that the model is not clinically validated. The current playbook defines the safe commercial hypothesis as an instructor-led workshop about model limitations and privacy using fictional inputs. Model provenance and rights, clinical validation, buyer demand, the live deployment, and operational services remain unverified.

## Decision

Treat VitalCue as an educational, synthetic-data-only demo and workshop artifact. Do not market or sell personalized health predictions, diagnosis, treatment suggestions, clinical decision support, patient-data handling, or a subscription health service. For the first commercial validation, sell only a clearly scoped instructor-led learning session if an instructor confirms demand and relevant licensing is cleared.

Keep the current monolith and ephemeral demo flow. Database, email alerts, and API records remain opt-in and off by default; for public sessions, keep them off. Signup is separate and must send only contact/consent metadata. Use no health data in analytics, support tickets, emails, or screenshots.

## Options considered

1. **Launch as a health-risk SaaS.** Rejected: no clinical validation, rights clearance, privacy/regulatory assessment, buyer evidence, or production support evidence; model outputs may be mistaken for care guidance.
2. **Build a multi-tenant platform with auth, billing, analytics, and automated campaigns now.** Rejected: premature infrastructure without validated buyer need; expands data and security scope.
3. **Validate an instructor-led synthetic-data workshop first.** Chosen: smallest path to test purchasing demand while keeping the product inside the current safe educational use.

## Consequences

- The next proof is 5–8 buyer conversations and a written-scope pilot, not more SaaS infrastructure.
- The team must verify the model artifact and training-data license before distribution or paid use.
- Live hosting is a blocker until a deployment health check passes; current documented 503 is not converted into a release claim.
- If the product direction changes toward clinical or real-person use, this ADR is not enough: obtain qualified clinical, privacy, regulatory, and security review, re-evaluate the intended use, and make a new decision before building.

## Revisit conditions

Revisit after a paid pilot or repeated, documented buyer request for a specific self-serve capability, and only after license, privacy, and safety checks establish that the capability can be provided within the education-only boundary.
