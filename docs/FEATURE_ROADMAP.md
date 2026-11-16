# VitalCue feature roadmap

This roadmap supports the workshop hypothesis in [market research](MARKET_RESEARCH.md), not a clinical product. All feature ideas use fictional, synthetic examples only. No upload of health records, free-text symptoms, individualized medical advice, clinical claims, patient analytics, or automated outreach is in scope.

Effort is a rough relative engineering estimate (S/M/L), not a delivery commitment. Impact is expected learning or instructor value, not measured revenue.

| # | Feature | User problem solved | Competitor gap / reason to consider | Impact | Effort |
|---:|---|---|---|---|---|
| 1 | Instructor workshop kit: run-of-show, setup, objectives, and facilitator notes | Instructor must assemble the session around the app | Broad course platforms provide catalogs; a small product can give one complete, ready-to-facilitate exercise | High | S |
| 2 | Model card and provenance panel | Learners cannot judge an output without knowing what data/model it represents | Generic notebook courses leave dataset/model provenance to the instructor; current provenance is a blocker and must be verified before making claims | High | M |
| 3 | Guided “what this output does not mean” lesson | A binary label can be mistaken for probability or personal diagnosis | Many coding sandboxes teach running models but not this particular safety boundary | High | S |
| 4 | Deterministic fictional scenario set with versioned definitions | Instructor needs repeatable examples across cohorts | Free notebooks require assembling and freezing exercise inputs/dependencies | High | S |
| 5 | Controlled-variable comparison activity | Learner needs to see that changing one field changes a model output, without interpreting it clinically | General courses cover exercises; a focused workshop can make model behavior and limitations the activity | High | M |
| 6 | Calibration and evaluation explainer using a separate toy model | Learner needs to distinguish accuracy, class labels, probabilities, and calibration | Avoid presenting unverified VitalCue model metrics as evidence; this feature must use a clearly separate toy example | High | M |
| 7 | Instructor-created lesson objective and rubric template | Instructor needs to assess reasoning, not simply the output label | Course libraries may require adapting a generic course to local outcomes | High | S |
| 8 | Printable learner worksheet and post-session reflection | Learners need a no-account way to discuss limitations and transfer learning | Self-guided platforms optimize in-platform progression; a workshop needs a portable classroom artifact | High | S |
| 9 | Local/offline workshop package with pinned dependencies | Unreliable classroom Wi-Fi or account access can derail a session | Hosted notebooks rely on account/network and may have changeable resource availability | High | M |
| 10 | Beginner glossary and step-by-step visual data flow | New learners need to follow the path from fictional inputs to label | Broad platforms can overwhelm beginners with large course catalogs or environment details | Medium | S |
| 11 | Accessible keyboard and screen-reader learner journey | Learners need to complete the activity with assistive technology | Some simulation reviews cite accessibility gaps; test against WCAG 2.2 AA rather than assume compliance | High | M |
| 12 | Language-ready facilitator materials | Mixed-language cohorts need clear instructions | Large platforms have broad catalogs but may not match the exact instructor's class language/context | Medium | M |
| 13 | Safe, anonymous workshop feedback card | Instructor needs to improve the session without collecting health data | Generic learning platforms collect broader learning signals; this can stay a short, non-sensitive local feedback loop | Medium | S |
| 14 | No-health-data session checklist and reset checklist | Instructor needs a reliable routine to avoid live personal data and clear the session | Most technical notebooks do not enforce this product-specific teaching protocol | High | S |
| 15 | Versioned facilitator release notes and compatibility checklist | Instructor needs to know what changed before a repeat session | Notebook environments and exercises may vary; one concise change log lowers repeat-session prep | Medium | S |

## Delivery order

1. Validate the buyer and teaching objective with interviews before implementing a full catalog or multi-tenant service.
2. Clear the rights/provenance gate and review current safety language.
3. Build the minimum paid-pilot kit first: items 1, 3, 4, 7, 8, 9, 11, and 14. Test the complete instructor-to-learner flow.
4. Add model transparency/evaluation items only when their evidence is supported by the model and training-data provenance.
5. Add cohort metrics, auth, billing, integrations, or email automation only after a buyer requests them and privacy/security review establishes a need. Current app stays no-account and no-data by default.

## Explicitly deferred

- Generative AI recommendations, care advice, or interpretation of an individual's inputs: unsafe and unnecessary for the validated teaching purpose.
- Clinical use, risk stratification of real people, EHR/data imports, patient accounts, and healthcare integrations: outside scope.
- SaaS billing, SSO, organization admin, and permanent learner analytics: not justified before pilot demand.
