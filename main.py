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
import datetime

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

    # List the files names
    files_list = os.listdir(DATA_PATH)

    # Create a placeholder for the dataframes columns names
    resources_columns = {}
    for resource_type in resources_types.keys():
        resources_columns[resource_type] = []

    # Loop that collects column names from each resource
    for file in files_list:
        bundle_obj = Bundle.parse_file(file)
        for entry in bundle_obj.entry:
            for resource_type in resources_types.keys():
                if entry.resource.resource_type == resource_type:
                    resource = resources_types[resource_type].parse_obj(entry.resource)
                    for column_name in resource.dict().keys():
                        resources_columns[resource_type].append(column_name)

    # Create set of column names for each resource used
    for resource_type in resources_columns.keys():
        resources_columns[resource_type] = sorted(list(set(resources_columns[resource_type])))

    # Create dataframe for each resource type
    tables = {}
    for resource_type in resources_types.keys():
        tables[resource_type] = pd.DataFrame(columns=resources_columns[resource_type])

    # Adding data to the tables
    for file in files_list:
        try:
            bundle_obj = Bundle.parse_file(file)
            for entry in bundle_obj.entry:
                for resource_type in resources_types.keys():
                    if entry.resource.resource_type == resource_type:
                        resource = resources_types[resource_type].parse_obj(entry.resource)

                        # Get the values from resource in the right order
                        values_list = []
                        for column_name in resources_columns[resource_type]:
                            try:
                                values_list.append(resource.dict()[column_name])
                            except Exception as e:
                                print("No found attribute: ", e)
                                values_list.append(None)

                        # Convert the datetime object and bool and None to str
                        for index in range(0 ,len(values_list)) :
                            try:
                                if type(values_list[index]) == datetime.datetime or type(values_list[index]) == datetime.date:
                                    values_list[index] = str(values_list[index])#f'{value.year}-{value.month}-{value.day}'
                                if type(values_list[index]) == bool:
                                    if values_list[index] is True:
                                        values_list[index] = 'True'
                                    if values_list[index] is False:
                                        values_list[index] = 'False'
                                if type(values_list[index]) == type(None):
                                    values_list[index] = ''
                            except Exception as e:
                                print("Exception: ", e)

                        new_df = pd.DataFrame(values_list, columns=resources_columns[resource_type])
                        concated_df = pd.concat([tables[resource_type], new_df], axis=1)
                        print(concated_df.head())
        except Exception as e:
            print("Exception: ", e)


if __name__ == '__main__':
    main()
