from unittest import TestCase
from unittest import main
from clinic.patient import *

class TestPatientClass(TestCase):
    
    def test_init(self):
        # Test Patient initialization
        patient = Patient("123456789", "John Doe", "1990-01-01", "555-1234", "john@example.com", "123 Main St")
        self.assertEqual(patient.phn, "123456789")
        self.assertEqual(patient.name, "John Doe")
        self.assertEqual(patient.birth_date, "1990-01-01")
        self.assertEqual(patient.phone, "555-1234")
        self.assertEqual(patient.email, "john@example.com")
        self.assertEqual(patient.adress, "123 Main St")

    def test_create_patient(self):
        # Test the create_patient method
        patient = Patient.create_patient("987654321", "Jane Doe", "1985-05-05", "555-5678", "jane@example.com", "456 Elm St")
        self.assertIsInstance(patient, Patient)
        self.assertEqual(patient.phn, "987654321")
        self.assertEqual(patient.name, "Jane Doe")
        self.assertEqual(patient.birth_date, "1985-05-05")
        self.assertEqual(patient.phone, "555-5678")
        self.assertEqual(patient.email, "jane@example.com")
        self.assertEqual(patient.adress, "456 Elm St")
    
    def test_eq(self):
        # Test equality comparison
        patient1 = Patient("123456789", "John Doe", "1990-01-01", "555-1234", "john@example.com", "123 Main St")
        patient2 = Patient("123456789", "John Doe", "1990-01-01", "555-1234", "john@example.com", "123 Main St")
        patient3 = Patient("987654321", "Jane Doe", "1985-05-05", "555-5678", "jane@example.com", "456 Elm St")
        
        self.assertTrue(patient1 == patient2)  # These should be equal
        self.assertFalse(patient1 == patient3)  # These should not be equal
        self.assertFalse(patient1 == None)  # Should return False when compared to None

    def test_repr(self):
        # Test the __repr__ method
        patient = Patient("123456789", "John Doe", "1990-01-01", "555-1234", "john@example.com", "123 Main St")
        self.assertEqual(repr(patient), "555-1234, 123456789, John Doe")
    
    def test_setters(self):
        # Test setters for updating patient info
        patient = Patient("123456789", "John Doe", "1990-01-01", "555-1234", "john@example.com", "123 Main St")
        
        # Update PHN
        updated_phn = patient.set_phn("987654321")
        self.assertEqual(updated_phn, "987654321")
        self.assertEqual(patient.phn, "987654321")
        
        # Update name
        updated_name = patient.set_name("Jane Doe")
        self.assertEqual(updated_name, "Jane Doe")
        self.assertEqual(patient.name, "Jane Doe")
        
        # Update birth_date
        updated_birth_date = patient.set_birth_date("1985-05-05")
        self.assertEqual(updated_birth_date, "1985-05-05")
        self.assertEqual(patient.birth_date, "1985-05-05")
        
        # Update phone
        updated_phone = patient.set_phone("555-5678")
        self.assertEqual(updated_phone, "555-5678")
        self.assertEqual(patient.phone, "555-5678")
        
        # Update email
        updated_email = patient.set_email("jane@example.com")
        self.assertEqual(updated_email, "jane@example.com")
        self.assertEqual(patient.email, "jane@example.com")
        
        # Update adress
        updated_adress = patient.set_adress("456 Elm St")
        self.assertEqual(updated_adress, "456 Elm St")
        self.assertEqual(patient.adress, "456 Elm St")
    
    def test_getters(self):
        # Test getters for retrieving patient info
        patient = Patient("123456789", "John Doe", "1990-01-01", "555-1234", "john@example.com", "123 Main St")
        
        self.assertEqual(patient.get_phn(), "123456789")
        self.assertEqual(patient.get_name(), "John Doe")
        self.assertEqual(patient.get_birth_date(), "1990-01-01")
        self.assertEqual(patient.get_phone(), "555-1234")
        self.assertEqual(patient.get_email(), "john@example.com")
        self.assertEqual(patient.get_adress(), "123 Main St")

if __name__ == "__main__":
    main()