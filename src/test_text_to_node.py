import unittest
from main import *
from textnode import *

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_simple(self):
        # Test with plain text (no markdown)
        text = "Just plain text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Just plain text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertIsNone(nodes[0].url)

    def test_text_to_textnodes_bold(self):
        # Test with bold text
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " text")

    def test_text_to_textnodes_italic(self):
        # Test with italic text
        text = "This is _italic_ text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " text")

    def test_text_to_textnodes_image(self):
        # Test with an image
        text = "This has an ![image](https://example.com/img.jpg)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "This has an ")
        self.assertEqual(nodes[1].text, "image")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://example.com/img.jpg")

    def test_text_to_textnodes_link(self):
        # Test with a link
        text = "Visit [my website](https://example.com)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "Visit ")
        self.assertEqual(nodes[1].text, "my website")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://example.com")

    def test_text_to_textnodes_code(self):
        # Test with code
        text = "Use `print()` function"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Use ")
        self.assertEqual(nodes[1].text, "print()")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " function")

    def test_text_to_textnodes_mixed(self):
        # Test with multiple markdown elements
        text = "This is **bold** with a [link](https://example.com)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 4)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " with a ")
        self.assertEqual(nodes[3].text, "link")
        self.assertEqual(nodes[3].text_type, TextType.LINK)
        self.assertEqual(nodes[3].url, "https://example.com")