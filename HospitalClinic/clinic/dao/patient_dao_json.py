import json
from clinic.dao.patient_dao import PatientDAO
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.patient import Patient
from clinic.dao.patient_decoder import PatientDecoder
from clinic.dao.patient_encoder import PatientEncoder


class PatientDAOJSON(PatientDAO):
	def __init__(self, autosave):
		self.patients = {}
		self.autosave = autosave
		self.file_name = 'clinic/patients.json'
		#if autosave then try to load from the json file.
		if autosave:
			try:
				with open(self.file_name, 'r') as file:
					file_content = file.read()
					patients_list = json.loads(file_content, cls = PatientDecoder)
					for patient in patients_list:
						self.patients[patient.phn] = patient
			except:
				self.patients = {}



	def search_patient(self, key):
		#find the correct patient
		if key in self.patients.keys():
			return self.patients[key]
		return None
      

	def create_patient(self, patient):
		#add the new patient normally
		self.patients[patient.phn] = patient
		#if autosave is true then add the new patient to the file
		if self.autosave:
			patient_list = []
			for pat in self.patients.values():
				patient_list.append(pat)
			with open(self.file_name, 'w') as file:
				json.dump(patient_list, file, cls = PatientEncoder)
		return patient
        # Implement the logic to add a new patient
		pass



	def retrieve_patients(self, search_string):
        # Implement logic to retrieve patients based on a search string
		
		retrieved_patients = []
		pat_list = []
		#if autosave is true then retrieve from json file
		if self.autosave:
			with open(self.file_name, 'r') as file:
				pat_list = json.load(file, cls = PatientDecoder)
			for pat in pat_list:
				if search_string in pat.name:
					retrieved_patients.append(pat)
			return retrieved_patients
		#if autosave is not true retrieve normally
		for patient in self.patients.values():
			if search_string in patient.name:
				retrieved_patients.append(patient)
		return retrieved_patients
		pass


	def update_patient(self, key, patient):
        #raises exception if phn belongs to another patient
		if key != patient.phn:
			if self.search_patient(patient.phn):
				raise IllegalOperationException
			#IllegalOperationException
				return False
		
		#reads from the file and then overwrites it using the updated list
		pat_list = []
		if self.autosave:
			with open(self.file_name, 'r') as file:
				pat_list = json.load(file, cls = PatientDecoder)
			for i in range(len(pat_list)):
				if pat_list[i].phn == key:
					pat_list[i] = patient
			with open(self.file_name, 'w') as file:
				json.dump(pat_list, file, cls = PatientEncoder)


		self.patients.pop(key)
		self.patients[patient.phn] = patient
		return True
        # Implement logic to update an existing patient
		pass

	def delete_patient(self, key):
		#removes the patient
		pat_list = []
		#if autosave is true then we remove the patient from the file as well
		if self.autosave:
			with open(self.file_name, 'r') as file:
				pat_list = json.load(file, cls = PatientDecoder)
			for i in range(len(pat_list)):
				if pat_list[i].phn == key:
					pat_list.pop(i)
					break
			with open(self.file_name, 'w') as file:
				json.dump(pat_list, file, cls = PatientEncoder)

		self.patients.pop(key)
		return True
        # Implement logic to delete a patient based on the key
		pass

	def list_patients(self):
        #lists all the patients
		patients_list = []
		for patient in self.patients.values():
			patients_list.append(patient)
		return patients_list
		pass

	def load_users(self):
		#if we have autosave true then load our users from the users.txt file.
		self.users = {}
		with open('clinic/users.txt', 'r') as file:
			for line in file:
				line = line.strip()
				line = line.split(',')
				self.users[line[0]] = line[1]
		return self.users