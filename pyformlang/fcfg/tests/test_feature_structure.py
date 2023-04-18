"""Testing of the feature structure"""
import unittest

from pyformlang.fcfg.feature_structure import FeatureStructure, PathDoesNotExistsException, \
    ContentAlreadyExistsException, FeatureStructuresNotCompatibleException


def _get_agreement_subject_number_person():
    fs2 = FeatureStructure.from_text("AGREEMENT=(1)[NUMBER=sg, PERSON=3], SUBJECT=[AGREEMENT->(1)]")
    return fs2


class TestFeatureStructure(unittest.TestCase):
    """Testing of the feature structure"""

    def test_creation(self):
        """Test of creation"""
        feature_structure = FeatureStructure()
        self.assertEqual(len(feature_structure.content), 0)
        self.assertEqual(feature_structure.pointer, None)
        self.assertEqual(feature_structure.get_feature_by_path().value, None)
        with self.assertRaises(PathDoesNotExistsException):
            feature_structure.get_feature_by_path(["NUMBER"])
        feature_structure.add_content("NUMBER", FeatureStructure("sg"))
        self.assertEqual(feature_structure.get_feature_by_path(["NUMBER"]).value, "sg")
        with self.assertRaises(ContentAlreadyExistsException):
            feature_structure.add_content("NUMBER", FeatureStructure("sg"))
        feature_structure = _get_agreement_subject_number_person()
        self.assertEqual(feature_structure.get_feature_by_path(["SUBJECT", "AGREEMENT", "NUMBER"]).value, "sg")

    def test_unify1(self):
        """First tests to unify"""
        left = FeatureStructure()
        right = FeatureStructure()
        left.unify(right)
        self.assertEqual(len(left.content), len(right.content))

    def test_unify2(self):
        """Second test to unify"""
        left = FeatureStructure("pl")
        right = FeatureStructure("sg")
        with self.assertRaises(FeatureStructuresNotCompatibleException):
            left.unify(right)

    def test_unify3(self):
        """Test to unify"""
        left = FeatureStructure()
        right = FeatureStructure("sg")
        left.unify(right)
        self.assertEqual(len(left.content), len(right.content))
        self.assertEqual(left.value, right.value)

    def test_unify4(self):
        """Test to unify"""
        left = FeatureStructure("pl")
        right = FeatureStructure()
        left.unify(right)
        self.assertEqual(len(left.content), len(right.content))
        self.assertEqual(left.value, right.value)

    def test_unify5(self):
        """Test to unify"""
        left = FeatureStructure()
        right = FeatureStructure()
        right.add_content("NUMBER", FeatureStructure("sg"))
        left.unify(right)
        self.assertEqual(len(left.content), len(right.content))
        self.assertEqual(left.value, right.value)
        self.assertEqual(left.get_feature_by_path(["NUMBER"]).value, right.get_feature_by_path(["NUMBER"]).value)
        self.assertEqual(left.get_feature_by_path(["NUMBER"]).value, "sg")

    def test_unify6(self):
        """Test to unify"""
        left = FeatureStructure()
        left.add_content("PERSON", FeatureStructure("M"))
        right = FeatureStructure()
        left.add_content("NUMBER", FeatureStructure("sg"))
        left.unify(right)
        self.assertTrue(len(left.content) >= len(right.content))
        self.assertEqual(left.value, right.value)
        self.assertEqual(left.get_feature_by_path(["NUMBER"]).value, right.get_feature_by_path(["NUMBER"]).value)
        self.assertEqual(left.get_feature_by_path(["NUMBER"]).value, "sg")

    def test_unify7(self):
        """Test to unify"""
        left = FeatureStructure()
        agreement_left = FeatureStructure()
        agreement_left.add_content("NUMBER", FeatureStructure("sg"))
        left.add_content("AGREEMENT", agreement_left)
        subject_left = FeatureStructure()
        subject_left.add_content("AGREEMENT", agreement_left)
        left.add_content("SUBJECT", subject_left)
        right = FeatureStructure()
        right.add_content("SUBJECT", FeatureStructure())
        right.add_content_path("AGREEMENT", FeatureStructure(), ["SUBJECT"])
        right.add_content_path("PERSON", FeatureStructure("3rd"), ["SUBJECT", "AGREEMENT"])
        left.unify(right)
        self.assertEqual(left.get_feature_by_path(["AGREEMENT", "PERSON"]).value,
                         right.get_feature_by_path(["AGREEMENT", "PERSON"]).value)
        self.assertEqual(left.get_feature_by_path(["SUBJECT", "AGREEMENT", "PERSON"]).value,
                         right.get_feature_by_path(["AGREEMENT", "PERSON"]).value)
        self.assertEqual(left.get_feature_by_path(["SUBJECT", "AGREEMENT", "PERSON"]).value,
                         "3rd")

    def test_subsumes1(self):
        """Test to subsume"""
        fs0 = FeatureStructure()
        fs0.add_content("NUMBER", FeatureStructure("pl"))
        fs1 = FeatureStructure()
        fs1.add_content("NUMBER", FeatureStructure("sg"))
        fs2 = FeatureStructure()
        fs2.add_content("PERSON", FeatureStructure("3"))
        fs3 = FeatureStructure()
        fs3.add_content("NUMBER", FeatureStructure("sg"))
        fs3.add_content("PERSON", FeatureStructure("3"))
        fs4 = FeatureStructure()
        fs4.add_content("CAT", FeatureStructure("VP"))
        agreement = FeatureStructure()
        fs4.add_content("AGREEMENT", agreement)
        subject = FeatureStructure()
        subject.add_content("AGREEMENT", agreement)
        fs4.add_content("SUBJECT", subject)
        fs5 = FeatureStructure()
        fs5.add_content("CAT", FeatureStructure("VP"))
        agreement = FeatureStructure()
        agreement.add_content("PERSON", FeatureStructure("3"))
        agreement.add_content("NUMBER", FeatureStructure("sg"))
        fs5.add_content("AGREEMENT", agreement)
        subject = FeatureStructure()
        subject.add_content("AGREEMENT", agreement)
        fs5.add_content("SUBJECT", subject)
        self.assertFalse(fs1.subsumes(fs0))
        # Identify
        self.assertTrue(fs1.subsumes(fs1))
        self.assertTrue(fs2.subsumes(fs2))
        self.assertTrue(fs3.subsumes(fs3))
        self.assertTrue(fs4.subsumes(fs4))
        self.assertTrue(fs5.subsumes(fs5))
        # Subsumes
        self.assertTrue(fs1.subsumes(fs3))
        self.assertTrue(fs2.subsumes(fs3))
        self.assertTrue(fs4.subsumes(fs5))
        # Not Subsumes
        self.assertFalse(fs1.subsumes(fs2))
        self.assertFalse(fs1.subsumes(fs4))
        self.assertFalse(fs1.subsumes(fs5))
        self.assertFalse(fs2.subsumes(fs1))
        self.assertFalse(fs2.subsumes(fs4))
        self.assertFalse(fs2.subsumes(fs5))
        self.assertFalse(fs3.subsumes(fs1))
        self.assertFalse(fs3.subsumes(fs2))
        self.assertFalse(fs3.subsumes(fs4))
        self.assertFalse(fs3.subsumes(fs5))
        self.assertFalse(fs4.subsumes(fs1))
        self.assertFalse(fs4.subsumes(fs2))
        self.assertFalse(fs4.subsumes(fs3))
        self.assertFalse(fs5.subsumes(fs1))
        self.assertFalse(fs5.subsumes(fs2))
        self.assertFalse(fs5.subsumes(fs3))
        self.assertFalse(fs5.subsumes(fs4))

    def test_copy(self):
        """Test to subsume"""
        fs1 = FeatureStructure()
        agreement = FeatureStructure()
        subject = FeatureStructure()
        subject.add_content("AGREEMENT", agreement)
        fs1.add_content("SUBJECT", subject)
        fs1.add_content("AGREEMENT", agreement)
        fs2 = _get_agreement_subject_number_person()
        fs1_copy = fs1.copy()
        fs1_copy.unify(fs2)
        self._assertions_test_copy(fs1_copy)
        fs1_copy2 = fs1.copy()
        subject_copy = fs1_copy2.get_feature_by_path(["SUBJECT"])
        subject2 = fs2.get_feature_by_path(["SUBJECT"])
        subject_copy.unify(subject2)
        self._assertions_test_copy(fs1_copy2)
        copy_of_copy = fs1_copy2.copy()
        self._assertions_test_copy(copy_of_copy)

    def _assertions_test_copy(self, fs1_copy):
        self.assertEqual(fs1_copy.get_feature_by_path(["AGREEMENT", "NUMBER"]).value, "sg")
        self.assertEqual(fs1_copy.get_feature_by_path(["AGREEMENT", "PERSON"]).value, "3")
        self.assertEqual(fs1_copy.get_feature_by_path(["SUBJECT", "AGREEMENT", "NUMBER"]).value, "sg")
        self.assertEqual(fs1_copy.get_feature_by_path(["SUBJECT", "AGREEMENT", "PERSON"]).value, "3")

    def test_paths(self):
        """Test the path generation"""
        fs2 = _get_agreement_subject_number_person()
        self.assertEqual(len(fs2.get_all_paths()), 4)
        representation = repr(fs2)
        self.assertIn("AGREEMENT.NUMBER", representation)
        self.assertIn("AGREEMENT.PERSON", representation)
        self.assertIn("SUBJECT.AGREEMENT.NUMBER", representation)
        self.assertIn("SUBJECT.AGREEMENT.PERSON", representation)
