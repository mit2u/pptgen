from django.test import SimpleTestCase

from core.utils import SlideEnum


class SlideEnumTests(SimpleTestCase):
    def test_slide_enum_values_are_stable(self):
        self.assertEqual(SlideEnum.title.value, "1")
        self.assertEqual(SlideEnum.bullet.value, "2")
        self.assertEqual(SlideEnum.column.value, "3")
        self.assertEqual(SlideEnum.image.value, "4")

    def test_slide_enum_members_are_strings(self):
        self.assertIsInstance(SlideEnum.title, str)
        self.assertEqual(str(SlideEnum.title), "1")
