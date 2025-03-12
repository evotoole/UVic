import json
from clinic.dao.patient_dao import PatientDAO
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.patient import Patient



class PatientDecoder(json.JSONDecoder):
	def __init__(self, *args, **kwargs):
		super().__init__(object_hook=self.object_hook, *args, **kwargs)
	def object_hook(self, dct):
		#returns our patient given its JSON representation
		if '__type__' in dct and dct['__type__'] == 'Patient':
			return Patient(dct['phn'], dct['name'], dct['birth_date'],\
				dct['phone'], dct['email'], dct['address'], dct['autosave'])
		return dct