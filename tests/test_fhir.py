from app.models.patient import Patient
from app.services.fhir_service import patient_to_fhir


def test_patient_to_fhir():
    patient = Patient(
        id="p1",
        phone="9999999999",
        full_name="Test Patient",
        preferred_language="en-IN",
        emergency_contact={},
    )
    resource = patient_to_fhir(patient)
    assert resource["resourceType"] == "Patient"
    assert resource["address"][0]["country"] == "IN"

