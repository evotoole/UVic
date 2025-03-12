import datetime
from clinic.note import Note
from clinic.dao.note_dao import NoteDAO
import pickle
from clinic.dao.note_dao_pickle import NoteDAOPickle
#from dao.note_dao import NoteDAO

class PatientRecord():
	''' class that represents a patient's medical record '''

	def __init__(self, autosave, phn):
		''' construct a patient record '''
		self.noteDAO = NoteDAOPickle(autosave, phn)
		self.autosave = autosave

	def search_note(self, code):
		''' search a note in the patient's record '''
		return self.noteDAO.search_note(code)

	def create_note(self, text):
		''' create a note in the patient's record '''
		return self.noteDAO.create_note(text)

	def retrieve_notes(self, search_string):
		''' retrieve notes in the patient's record that satisfy a search string '''
		# retrieve existing notes
		return self.noteDAO.retrieve_notes(search_string)

	def update_note(self, code, new_text):
		''' update a note from the patient's record '''
		return self.noteDAO.update_note(code, new_text)

	def delete_note(self, code):
		''' delete a note from the patient's record '''
		return self.noteDAO.delete_note(code)

	def list_notes(self):
		''' list all notes from the patient's record from the 
			more recently added to the least recently added'''
		return self.noteDAO.list_notes()

