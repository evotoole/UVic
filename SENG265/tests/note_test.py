from unittest import TestCase
from unittest import main
from clinic.note import *

class TestNoteClass(TestCase):

    def test_init(self):
        # Test initialization of Note
        note = Note("A1", "This is a note")
        self.assertEqual(note.code, "A1")
        self.assertEqual(note.text, "This is a note")
        self.assertIsNone(note.time_stamp)

    def test_create_note(self):
        # Test the create_note method
        note = Note.create_note("B2", "Another note")
        self.assertIsInstance(note, Note)
        self.assertEqual(note.code, "B2")
        self.assertEqual(note.text, "Another note")

    def test_repr(self):
        # Test the __repr__ method
        note = Note("C3", "Sample note")
        self.assertEqual(repr(note), "C3, Sample note")

    def test_eq(self):
        # Test the __eq__ method
        note1 = Note("D4", "Same note")
        note2 = Note("E5", "Same note")
        note3 = Note("F6", "Different note")
        
        self.assertTrue(note1 == "Same note")
        self.assertFalse(note2 == "Different note")
        self.assertFalse(note3 == "Same note")
        self.assertFalse(note1 == None)

    def test_set_note(self):
        # Test the set_note method
        note = Note("G7", "Initial note")
        updated_note = note.set_note("H8", "Updated note")
        self.assertIsInstance(updated_note, Note)
        self.assertEqual(updated_note.code, "H8")
        self.assertEqual(updated_note.text, "Updated note")


if __name__ == "__main__":
    unittest.main()