# VitalCue

VitalCue is an educational health-risk prediction prototype with a Streamlit demo and an optional authenticated Flask API.

> **Research demo only.** The model is not clinically validated. Results and generated food/activity examples are not medical advice and must not guide care decisions. Use synthetic inputs only; never enter real patient or identifying information.

## Hosted demo

https://agewell-risk-demo.onrender.com/

The hosted demo does not save predictions, generate email alerts, or connect to a database. Local database storage and email controls are hidden unless `AGEWELL_LOCAL_STORAGE_ENABLED=true` is explicitly set; leave it `false` for hosted deployments. Inputs are processed by the public hosting service, so use fictional sample values only; the app requires you to confirm this before running a prediction. If you request a PDF, the generated file is removed immediately after its bytes are loaded into the current Streamlit session for download. Use **Reset fictional sample** to clear entered values, consent, options and any session-held report bytes.

An optional research/workshop signup appears only when `LEADHUB_BASE_URL` is configured with the separate HTTPS LeadHub service. It sends only an email after explicit opt-in; health values and reports are never included. A separate opt-in can request related products; that request sends only the `vitalcue` product ID and never includes health inputs or usage history. The CLI now runs one fixed fictional sample and cannot accept, save, or email arbitrary patient inputs.

## What it does

- Estimates a binary risk label from age, heart rate, systolic blood pressure and cholesterol.
- Shows the four fictional values used for the label and clarifies that height and weight are only used for the BMI reference.
- Explains which four fields drive the classifier and separates its high/low label from the BMI reference and rule-based examples.
- Calculates a reference BMI and prototype score, then displays rule-based examples. The result explains the score's fixed code thresholds and clarifies that they are neither clinical cutoffs nor a probability.
- Loads either of two clearly fictional input examples for a quick demo; each selection clears prior confirmation, optional outputs, and any session-held report bytes.
- Shows the PDF download action as soon as an explicitly requested sample report is ready; MySQL persistence remains opt-in and local-only.
- Provides an optional Flask API with bearer-token authentication; persistence and reports default off.

## Local setup

Requires Python 3.12.11. Create a virtual environment, then install dependencies:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start the demo:

```powershell
streamlit run app.py
```

Optional database, report and email settings are documented in `.env.example`. Keep all real secrets in a local `.env` file and never commit them. UI database storage and email alerts remain unavailable unless you explicitly set `AGEWELL_LOCAL_STORAGE_ENABLED=true`; storage also requires all MySQL settings, and alerts require `EMAIL_ALERTS_ENABLED=true` plus an explicit per-run opt-in. Keep local storage disabled on public hosting.

## Optional API

Set `AGEWELL_API_TOKEN` to a unique secret of at least 32 characters before starting the Flask API:

```powershell
$env:AGEWELL_API_TOKEN = python -c "import secrets; print(secrets.token_urlsafe(32))"
python -m app.routes.api
```

- `GET /health` — service health; no patient data.
- `POST /predict` — requires `Authorization: Bearer <token>` and a JSON body containing `age`, `heart_rate`, `systolic_bp`, `cholesterol`, `weight`, `height`, and `synthetic_data_confirmed: true`. Requests without this explicit fictional-data confirmation are rejected. JSON results repeat the research-only/non-clinical warning for downstream clients.
- `GET /records` — disabled by default. It requires `AGEWELL_API_RECORDS_ENABLED=true`, the same bearer token, and a configured MySQL database; it exposes stored health values, so only enable it in an isolated, single-owner environment.

JSON requests larger than 16 KiB receive a bounded JSON `413` response; API prediction errors are not returned as HTML pages.

API predictions never persist records, even if `save_to_db` is requested. Reports are generated only when `generate_pdf` is explicitly set to `true`; `POST /predict` then returns an `application/pdf` attachment, with risk label, BMI and prototype score in response headers. The temporary server file is removed after reading. Treat the downloaded report as sensitive health information. Do not expose a token in browser code, logs, screenshots or a public repository.

## Project map

- `app.py` — Streamlit interface and optional research signup.
- `app/routes/api.py` — authenticated Flask endpoints.
- `app/services/health_service.py` — model workflow and opt-in side effects.
- `app/models/` — predictor and serialized research model.
- `app/utils/` — database, PDF and email helpers.
- `app/services/newpatient.py` — fixed fictional CLI sample with all persistence and alerts disabled.
- `tests/` — privacy-default and report-file checks.

## Possible paid offer

The safe commercial direction is an instructor-led workshop for data-science classes on model limitations, synthetic-data demos, and privacy-by-default workflows. VitalCue is the teaching example, not a health service. A workshop should use fictional values only and explain how this prototype separates classifier inputs, BMI, and rule-based examples. Validate demand with instructors before quoting or charging, and verify model and training-data licenses before including this repository in paid materials. Do not sell health predictions or patient-data handling through this app.

## Run checks

```powershell
python -m unittest discover -s tests -v
```

GitHub Actions runs Python compilation and the test suite on pushes and pull requests to `main`.

## Privacy and limitations

This prototype has not been clinically validated or assessed for medical use. Public hosting is intended only for synthetic sample values. The hosted service has no database or email credentials configured, and the UI disables record storage until a complete local MySQL configuration is provided. The Render Free service is a demo only: it can sleep after 15 idle minutes and its filesystem is temporary. Before any real-world use, obtain clinical, privacy, security and regulatory review, and build appropriate consent, access control, retention and monitoring. Do not sell clinical predictions from this prototype.
