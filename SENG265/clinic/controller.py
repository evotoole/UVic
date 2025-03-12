from .patient import Patient
from .patient import *
from .note import Note
from .note import *

class Controller:


    def __init__(self):
       self.logged = False
       self.pat = []
       self.retrieved = []
       self.current_pat = None
       self.cur_text_num = 0
       self.cur_note = None
       self.note_dic = {}
       self.note_list = []


    def login(self, name, password):
       if (((name == "user")and(password == "clinic2024")) and (self.logged == False)):
           self.logged = True
           return self.logged
       return False
      
    def logout(self):
       if (self.logged):
           self.logged = False
           return True
       return False
      
    def create_patient(self, phn, name, birth_date, phone, email, adress):
       #checks if the phn already is given, if not it creates a patient
       if (self.logged):
           for i in range(len(self.pat)):
                if (phn == self.pat[i].phn):
                    return
           self.patient = Patient.create_patient(phn, name, birth_date, phone, email, adress)
           self.pat.append(self.patient)
           return self.patient
       return
    
  
    def search_patient(self, phn):
       #searches through an array of patients
       for person in range(len(self.pat)):
           if self.pat[person].get_phn() == phn:
                return self.pat[person]
       return
   
    def retrieve_patients(self, name):
        #looks through a list of patients and if they have the name in there name they are returned in the list
        self.retrieved = []
        if (self.logged):
            for person in range(len(self.pat)):
                if ((name in self.pat[person].get_name()) and (self.pat[person].get_name() != None)):    
                    if not (self.pat[person] in self.retrieved):
                        self.retrieved.append(self.pat[person])
            return self.retrieved
        return
    
    def update_patient(self,prev_phn, phn, name, birth_date, phone, email, adress):
        #updates a patient correctly based on our given parameters (cycles through the list of people ensuring we can correctly update)
        if (self.logged):
            for person2 in range(len(self.pat)):
                if (phn == self.pat[person2].phn) and (phn != prev_phn):
                    return False
            for person in range(len(self.pat)):
                if prev_phn == self.pat[person].phn:
                    if self.pat[person] == self.current_pat:
                        return False
                    self.pat[person] = Patient(phn, name, birth_date, phone, email, adress)
                    return True
        return False
    
    def delete_patient(self, phn):
        #removes a patient from the list and shifts the array so that patients are properly positioned
        if (self.logged):
            for ind in range(len(self.pat)):
                if self.pat[ind].phn == phn:
                    if (self.current_pat != None):
                        if (self.pat[ind] == self.current_pat):
                            return False
                    for ind2 in range(ind+1,len(self.pat)):
                        self.pat[ind2-1] = self.pat[ind2]
                    self.pat.pop()
          
                    return True
        return False
        
    def list_patients(self):
        if self.logged:
            return self.pat
        return
        
    def get_current_patient(self):
        if self.logged:
            if self.current_pat:
                return self.current_pat
        return
        
    def set_current_patient(self, phn):
        if self.logged:
            for i in range(len(self.pat)):
                if phn == self.pat[i].phn:
                    self.current_pat = self.pat[i]
                    return True
        return False
    
    def unset_current_patient(self):
        if (self.logged):
            if (self.current_pat):
                self.current_pat = None
                return True
            
    def create_note(self, text):
        if self.logged:
            if self.current_pat:
                self.cur_text_num += 1
                self.cur_note = Note.create_note(self.cur_text_num, text)
                self.note_dic[self.cur_text_num] = self.cur_note
                return self.cur_note
            
    def search_note(self, code):
        if code in self.note_dic:
            return self.note_dic[code]
        return
    
    def retrieve_notes(self, text):
        #finds patients with the text parameter in there text and returns them
        self.note_list = []
        if self.logged and self.cur_note:
            for key in self.note_dic:
                if (text in self.note_dic[key].text) and not (self.note_dic[key] in self.note_list):
                    self.note_list.append(self.note_dic[key])
            return self.note_list
        return
    
    def update_note(self, code, text):
        if self.logged and self.current_pat:
            if code not in self.note_dic:
                return False
            self.note_dic[code] = text
            return True
    
    def delete_note(self, code):
        if self.logged and self.current_pat:
            if code in self.note_dic:
                del(self.note_dic[code])
                return True
        return False
    
    def list_notes(self):
        #returns a lsit of all the patients stored in the dictionary
        self.note_list = []
        temp_list = []
        if self.logged:
            for key in self.note_dic:
                temp_list.append(self.note_dic[key])
            for i in range(len(temp_list)-1, -1,-1):
                self.note_list.append(temp_list[i])
            if not (self.current_pat):
                return None
            print(self.note_list)
            return self.note_list