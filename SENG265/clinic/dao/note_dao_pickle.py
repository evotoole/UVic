import pickle
from clinic.dao.note_dao import NoteDAO
import datetime
from clinic.note import Note


class NoteDAOPickle(NoteDAO):
	def __init__(self, autosave, phn):
		''' construct a patient record '''
		self.counter = 0
		self.notes = []
		self.phn = phn
		self.autosave = autosave
		#in the constructor, try to load the notes from the given patients record file
		#persistence code is seperated with the if statement
		if autosave:
			try:
				with open(f'clinic/records/{self.phn}.dat', 'rb') as file:
					self.notes = pickle.load(file)
			except:
				self.notes = []


	def search_note(self, key):
		#returns note if found without file.
		for note in self.notes:
			if note.code == key:
				return note
		notes = []

		#if autosave then use persistence code to find the note is the saved file
		#read from the binaray file in records and identify the note.
		if self.autosave:
			with open(f'clinic/records/{self.phn}.dat', 'rb') as file:
				notes = pickle.load(file)
				for note in notes:
					if note.code == key:
						return note
		return None
		pass


	def create_note(self, text):
		self.counter += 1
		temp = []
		
		#the following ensures self.counter is working properly after persistence is reset
		if self.autosave:
			try:
				with open(f'clinic/records/{self.phn}.dat', 'rb') as file:
					temp = pickle.load(file)
					self.counter = len(temp)+1
			except:
				pass

		current_time = datetime.datetime.now()
		new_note = Note(self.counter, text, current_time)
		self.notes.append(new_note)

		#we now write back into the file in binary our list of notes
		if self.autosave:
			with open(f'clinic/records/{self.phn}.dat', 'wb') as file:
				pickle.dump(self.notes, file)

		return new_note
		pass


	def retrieve_notes(self, search_string):
		#retrieves the notes with the given search_string
		retrieved_notes = []
		for note in self.notes:
			if search_string in note.text:
				retrieved_notes.append(note)
		return retrieved_notes
		pass


	def update_note(self, key, text):
		updated_note = None

		# first, search the note by code
		for note in self.notes:
			if note.code == key:
				updated_note = note
				break

		# note does not exist
		if not updated_note:
			return False

		# note exists, update fields
		updated_note.text = text
		updated_note.timestamp = datetime.datetime.now()

		temp_notes = []
		updated_notes = []

		#the following updates the given records file, by overwritting the previous with the updated 
		if self.autosave:
			with open(f'clinic/records/{self.phn}.dat', 'rb') as file:
				temp_notes = pickle.load(file)
				for note in temp_notes:
					if note.code == key:
						note.text = updated_note.text
						note.timestamp = updated_note.timestamp
					updated_notes.append(note)
			with open(f'clinic/records/{self.phn}.dat', 'wb') as file:
				pickle.dump(updated_notes, file)

		return True
		pass
   

	def delete_note(self, key):
		note_to_delete_index = -1

		# first, search the note by code
		for i in range(len(self.notes)):
			if self.notes[i].code == key:
				note_to_delete_index = i
				break

		# note does not exist
		if note_to_delete_index == -1:
			return False
		
		# note exists, delete note
		self.notes.pop(note_to_delete_index)

		#delete the node from file, by overwritting
		with open(f'clinic/records/{self.phn}.dat', 'wb') as file:
				pickle.dump(self.notes, file)

		return True
		pass


	def list_notes(self):
		# list existing notes
		notes_list = []
		for i in range(-1, -len(self.notes)-1, -1):
			notes_list.append(self.notes[i])
		return notes_list
		pass

