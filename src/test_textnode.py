import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
    
    def test_not_eq_type(self):
       node = TextNode("This is a text node", TextType.BOLD_TEXT)
       node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
       self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
       node = TextNode("This is a text node", TextType.ITALIC_TEXT, "https://www.boot.dev")
       node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
       self.assertNotEqual(node, node2)

    
    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.CODE_TEXT, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.CODE_TEXT, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
       node = TextNode("This is a node", TextType.ITALIC_TEXT, "https://www.boot.dev")
       node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
       self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()