import unittest
import rendering


class FormattingTests(unittest.TestCase):
    def test_render_sequence_012(self):
        self.assertEqual(rendering.render_sequence([0, 1, 2]), "0-2")

    def test_render_sequence_0234(self):
        self.assertEqual(rendering.render_sequence([0, 2, 3, 4]), "0,2-4")

    def test_render_sequence_0124(self):
        self.assertEqual(rendering.render_sequence([0, 2, 3, 4]), "0,2-4")

    def test_render_sequence02(self):
        self.assertEqual(rendering.render_sequence([0, 2]), "0,2")

    def test_render_sequence0(self):
        self.assertEqual(rendering.render_sequence([0]), "0")

    def test_render_sequence_null(self):
        self.assertEqual(rendering.render_sequence([]), "")

    def test_render_sequence_biglist(self):
        self.assertEqual(rendering.render_sequence(
            [3, 4, 6, 7, 8, 9, 11, 12, 14, 16, 18, 19, 20, 21, 22, 23, 24]),
            "3,4,6-9,11,12,14,16,18-24")

    def test_render_sequence_biglist2(self):
        self.assertEqual(rendering.render_sequence(
            [3, 4, 6, 7, 8, 9, 11, 12, 14, 16, 18, 19, 20, 21, 24]),
            "3,4,6-9,11,12,14,16,18-21,24")
