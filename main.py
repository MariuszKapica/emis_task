from fhir.resources.bundle import Bundle
from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.careplan import CarePlan
from fhir.resources.careteam import CareTeam
from fhir.resources.claim import Claim
from fhir.resources.condition import Condition
from fhir.resources.device import Device
from fhir.resources.diagnosticreport import DiagnosticReport
from fhir.resources.documentreference import DocumentReference
from fhir.resources.encounter import Encounter
from fhir.resources.explanationofbenefit import ExplanationOfBenefit
from fhir.resources.imagingstudy import ImagingStudy
from fhir.resources.immunization import Immunization
from fhir.resources.medication import Medication
from fhir.resources.medicationadministration import MedicationAdministration
from fhir.resources.medicationrequest import MedicationRequest
from fhir.resources.observation import Observation
from fhir.resources.patient import Patient
from fhir.resources.procedure import Procedure
from fhir.resources.provenance import Provenance
from fhir.resources.supplydelivery import SupplyDelivery
import pandas as pd
import os

MAIN_PATH = os.getcwd()
DATA_PATH = os.path.join(MAIN_PATH, 'data')
os.chdir(DATA_PATH)
resources_types = {'AllergyIntolerance' : AllergyIntolerance,
                   'CarePlan': CarePlan,
                   'CareTeam': CareTeam,
                   'Claim': Claim,
                   'Condition': Condition,
                   'Device': Device,
                   'DiagnosticReport': DiagnosticReport,
                   'DocumentReference': DocumentReference,
                   'Encounter': Encounter,
                   'ExplanationOfBenefit': ExplanationOfBenefit,
                   'ImagingStudy': ImagingStudy,
                   'Immunization': Immunization,
                   'Medication': Medication,
                   'MedicationAdministration': MedicationAdministration,
                   'MedicationRequest': MedicationRequest,
                   'Observation': Observation,
                   'Patient': Patient,
                   'Procedure': Procedure,
                   'Provenance': Provenance,
                   'SupplyDelivery': SupplyDelivery}

def main():
    print(os.listdir(DATA_PATH))
    files_list = os.listdir(DATA_PATH)
    patients_list = []
    for file in files_list:
        try:
            bundle_obj = Bundle.parse_file(file)
            for entry in bundle_obj.entry:
                if entry.resource.resource_type == 'Patient':
                    patient = Patient.parse_obj(entry.resource)
                    print(patient.dict().keys())
                    patients_list.append(patient)
            print(len(patients_list))
        except Exception as e:
            print("No Entries. Exception: ", e)


if __name__ == '__main__':
    main()
