from clinic.patient import Patient
from clinic.patient_record import PatientRecord
from clinic.note import Note
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException
from clinic.dao.patient_dao import PatientDAO
from clinic.dao.patient_dao_json import *
import json
import hashlib

class Controller():
	''' controller class that receives the system's operations '''

	def __init__(self, autosave):
		''' construct a controller class '''
		
		self.autosave = autosave
		self.patientDAOJSON = PatientDAOJSON(autosave)
		self.username = None
		self.password = None
		self.logged = False
		self.users = {"user" : "123456", "ali" : "@G00dPassw0rd"}
		if self.autosave:
			self.users = self.patientDAOJSON.load_users()
		#self.patients = {}
		self.current_patient = None
		
	def login(self, username, password):
		''' user logs in the system '''

		if self.logged:
			raise DuplicateLoginException
			return False
		if self.autosave:
			if username in self.users:
				if self.get_password_hash(password) == self.users[username]:
					self.username = username
					self.password = password
					self.logged = True

					return True

		if username in self.users:
			if password == self.users[username]:
				self.username = username
				self.password = password
				self.logged = True
				
				return True
			else:
				raise InvalidLoginException
				return False
		else:
			raise InvalidLoginException
			return False

	def logout(self):
		''' user logs out from the system '''
		if not self.logged:
			raise InvalidLogoutException
			return False
		else:
			self.username = None
			self.password = None
			self.logged = False
			self.current_patient = None
			return True
		
	def get_password_hash(self, password):
		encoded_password = password.encode('utf-8')     # Convert the password to bytes
		hash_object = hashlib.sha256(encoded_password)      # Choose a hashing algorithm (e.g., SHA-256)
		hex_dig = hash_object.hexdigest()       # Get the hexadecimal digest of the hashed password
		return hex_dig

	def search_patient(self, phn):
		''' user searches a patient '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException
			return None

		return self.patientDAOJSON.search_patient(phn)

	def create_patient(self, phn, name, birth_date, phone, email, address):
		''' user creates a patient '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException
			return None

		# patient already exists, do not create them
		if self.patientDAOJSON.search_patient(phn):
			raise IllegalOperationException
			return None

		# finally, create a new patient
		patient = Patient(phn, name, birth_date, phone, email, address, self.autosave)
		
		#self.patientDAOJSON.create_patient(patient)
		return self.patientDAOJSON.create_patient(patient)
		

	def retrieve_patients(self, name):
		''' user retrieves the patients that satisfy a search criterion '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException
			return None

		
		return self.patientDAOJSON.retrieve_patients(name)

	def update_patient(self, original_phn, phn, name, birth_date, phone, email, address):
		''' user updates a patient '''
		# must be logged in to do operation
		
		if not self.logged:
			raise IllegalAccessException
			return False

		# first, search the patient by key
		patient = self.patientDAOJSON.search_patient(original_phn)

		# patient does not exist, cannot update
		if not patient:
			raise IllegalOperationException
			return False
		
		

		# patient is current patient, cannot update
		if self.current_patient:
			if patient == self.current_patient:
				raise IllegalOperationException
				return False
			
		

		# create updated_patient
		updated_patient = Patient(phn, name, birth_date, phone, email, address, self.autosave)


		return self.patientDAOJSON.update_patient(original_phn, updated_patient)

		
			
	def delete_patient(self, phn):
		''' user deletes a patient '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException
			return False

		# first, search the patient by key
		patient = self.patientDAOJSON.search_patient(phn)

		# patient does not exist, cannot delete
		if not patient:
			raise IllegalOperationException
			return False

		# patient is current patient, cannot delete
		if self.current_patient:
			if patient == self.current_patient:
				raise IllegalOperationException
				return False

		# patient exists, delete patient
		return self.patientDAOJSON.delete_patient(phn)
		

	def list_patients(self):
		''' user lists all patients '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException
			return None


		return self.patientDAOJSON.list_patients()

	def set_current_patient(self, phn):
		''' user sets the current patient '''

		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException
			return False
		

		# first, search the patient by key
		patient = self.patientDAOJSON.search_patient(phn)

		# patient does not exist
		if not patient:
			raise IllegalOperationException
			return False

		# patient exists, set them to be the current patient
		self.current_patient = patient


	def get_current_patient(self):
		''' get the current patient '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException
			return None

		# return current patient
		return self.current_patient

	def unset_current_patient(self):
		''' unset the current patient '''

		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException
			return None

		# unset current patient
		self.current_patient = None
		return None


	def search_note(self, code):
		''' user searches a note from the current patient's record '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException
			return None

		# there must be a valid current patient
		if not self.current_patient:
			raise NoCurrentPatientException
			return None

		# search a new note with the given code and return it 
		return self.current_patient.search_note(code)

	def create_note(self, text):
		''' user creates a note in the current patient's record '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException
			return None

		# there must be a valid current patient
		if not self.current_patient:
			raise NoCurrentPatientException
			return None

		# create a new note and return it
		return self.current_patient.create_note(text)

	def retrieve_notes(self, search_string):
		''' user retrieves the notes from the current patient's record
			that satisfy a search string '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException
			return None

		# there must be a valid current patient
		if not self.current_patient:
			raise NoCurrentPatientException
			return None

		# return the found notes
		return self.current_patient.retrieve_notes(search_string)

	def update_note(self, code, new_text):
		''' user updates a note from the current patient's record '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException
			return None

		# there must be a valid current patient
		if not self.current_patient:
			raise NoCurrentPatientException
			return None

		# update note
		return self.current_patient.update_note(code, new_text)

	def delete_note(self, code):
		''' user deletes a note from the current patient's record '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException
			return None

		# there must be a valid current patient
		if not self.current_patient:
			raise NoCurrentPatientException
			return None

		# delete note
		return self.current_patient.delete_note(code)

	def list_notes(self):
		''' user lists all notes from the current patient's record '''
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException
			return None

		# there must be a valid current patient
		if not self.current_patient:
			raise NoCurrentPatientException
			return None

		return self.current_patient.list_notes()