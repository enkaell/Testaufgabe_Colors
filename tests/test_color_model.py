import unittest
from color_model import HEXColor, HEXColorFactory, MessageErrors
from utils import find_color_name, ColorNotFoundException


class TestHEXColor(unittest.TestCase):
    
    def test_valid_hex_color(self):
        color = HEXColor("#FFAABB")
        self.assertEqual(color.value, "#FFAABB")

    def test_invalid_length(self):
        with self.assertRaises(ValueError) as context:
            HEXColor("#FFAA")  # Length != 7
        self.assertEqual(context.exception.args[0], MessageErrors.LENGTH)

    def test_invalid_format(self):
        with self.assertRaises(ValueError) as context:
            HEXColor("1FFAABB")  # No '#' prefix
        self.assertEqual(context.exception.args[0], MessageErrors.FORMAT)

    def test_invalid_hex_digits(self):
        with self.assertRaises(ValueError) as context:
            HEXColor("#GGGGGG")  # Not valid hex digits
        self.assertEqual(context.exception.args[0], MessageErrors.HEX_DIGITS)

    def test_brightness_calculation(self):
        color = HEXColor("#FFFFFF")
        self.assertEqual(color.brightness, 255.0)

        color = HEXColor("#000000")
        self.assertEqual(color.brightness, 0.0)

    def test_HEXtoRGBAdapter(self):
        color = HEXColor("#123456")
        r, g, b = color.HEXtoRGBAdapter()
        self.assertEqual((r, g, b), (18, 52, 86))


class TestHEXColorFactory(unittest.TestCase):

    def setUp(self):
        self.factory = HEXColorFactory()

    def test_create_single_hex_color(self):
        color = self.factory.create_hex_color("#ABCDEF")
        self.assertIsInstance(color, HEXColor)
        self.assertEqual(color.value, "#ABCDEF")

    def test_create_list_hex_colors(self):
        color_list = self.factory.create_list_hex_colors(["#111111", "#222222", "#333333"])
        self.assertEqual(len(color_list), 3)
        for color in color_list:
            self.assertIsInstance(color, HEXColor)


class TestFindColorName(unittest.TestCase):

    def setUp(self):
        self.sample_data = [
            {"hex": "ffffff", "name": "White"},
            {"hex": "000000", "name": "Black"},
            {"hex": "ff0000", "name": "Red"}
        ]

    def test_find_color_name_success(self):
        name = find_color_name("ffffff", "hex", self.sample_data)
        self.assertEqual(name, "White")

    def test_find_color_name_not_found(self):
        with self.assertRaises(ColorNotFoundException):
            find_color_name("123456", "hex", self.sample_data)


if __name__ == '__main__':
    unittest.main()
