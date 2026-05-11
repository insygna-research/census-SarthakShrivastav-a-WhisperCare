from __future__ import annotations

from app.models.intake import IntakeSession
from app.models.patient import Patient


def patient_to_fhir(patient: Patient) -> dict:
    return {
        "resourceType": "Patient",
        "id": patient.id,
        "name": [{"text": patient.full_name}],
        "telecom": [{"system": "phone", "value": patient.phone}],
        "gender": patient.gender,
        "address": [{"state": patient.state, "country": "IN"}],
        "identifier": _patient_identifiers(patient),
    }


def intake_to_questionnaire_response(intake: IntakeSession) -> dict:
    return {
        "resourceType": "QuestionnaireResponse",
        "id": intake.id,
        "status": "completed" if intake.status == "completed" else "in-progress",
        "subject": {"reference": f"Patient/{intake.patient_id}"} if intake.patient_id else None,
        "item": [
            {"linkId": key, "answer": [{"valueString": value}]}
            for key, value in intake.raw_answers.items()
        ],
    }


def build_patient_bundle(patient: Patient, intakes: list[IntakeSession]) -> dict:
    entries = [{"resource": patient_to_fhir(patient)}]
    entries.extend({"resource": intake_to_questionnaire_response(item)} for item in intakes)
    return {"resourceType": "Bundle", "type": "collection", "entry": entries}


def _patient_identifiers(patient: Patient) -> list[dict]:
    identifiers = []
    if patient.abha_address:
        identifiers.append({"system": "https://abdm.gov.in/abha-address", "value": patient.abha_address})
    if patient.abha_number:
        identifiers.append({"system": "https://abdm.gov.in/abha-number", "value": patient.abha_number})
    return identifiers

