class Patient:


    def __init__(self, phn, name, birth_date, phone, email, adress):
       self.phn = phn
       self.name = name
       self.birth_date = birth_date
       self.phone = phone
       self.email = email
       self.adress = adress
 
    
    def __eq__(self, other):
       #checks if equal
       if (other == None):
           return False
       if (self.phone != other.phone):
           return False
       if (self.phn != other.phn):
           return False
       if (self.name != other.name):
           return False
       if (self.birth_date != other.birth_date):
           return False
       if (self.adress != other.adress):
           return False
       if (self.email != other.email):
           return False
       return True

    def __repr__(self):
        return f"{self.phone}, {self.phn}, {self.name}"
    
    def create_patient(phn, name, birth_date, phone, email, adress):
        return Patient(phn, name, birth_date, phone, email, adress)
    
    def get_phn(self):
        return self.phn
    
    def get_name(self):
        return self.name

    def get_birth_date(self):
        return self.birth_date

    def get_phone(self):
        return self.phone

    def get_email(self):
        return self.email

    def get_adress(self):
        return self.adress
    
    def set_phn(self, phn):
        self.phn = phn
        return self.phn
    
    def set_name(self, name):
        self.name = name
        return self.name

    def set_birth_date(self, birth_date):
        self.birth_date = birth_date
        return self.birth_date

    def set_phone(self, phone):
        self.phone = phone
        return self.phone

    def set_email(self, email):
        self.email = email
        return self.email

    def set_adress(self, adress):
        self.adress = adress
        return self.adress