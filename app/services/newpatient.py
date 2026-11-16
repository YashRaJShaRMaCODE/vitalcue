"""Run one fictional VitalCue sample without saving, reporting, or emailing."""
from app.services.health_service import process_patient


def main():
    print("Research demo only · fictional sample values · not a medical tool")
    result = process_patient(
        65, 80, 120, 180, 65, 1.7,
        save_to_db=False,
        generate_pdf=False,
        send_alert=False,
    )
    print(f"Sample label: {result.risk_label} · BMI reference: {result.bmi}")
    print("No values were saved, emailed, or added to a report.")


if __name__ == "__main__":
    main()
