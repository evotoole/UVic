import json
from clinic.dao.patient_dao import PatientDAO
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.patient import Patient


class PatientEncoder(json.JSONEncoder):
	def default(self, obj):
		#converts our patient into dictionary format so it can properly be encoded in JSON
		if isinstance(obj, Patient):
			return {"__type__": "Patient", "phn": obj.phn, \
		   	"name": obj.name, "birth_date": obj.birth_date, \
			"phone": obj.phone, "email": obj.email, "address": obj.address, "autosave":obj.autosave}
		return super().default(obj)
