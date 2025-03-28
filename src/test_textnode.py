import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq_type(self):
       node = TextNode("This is a text node", TextType.BOLD)
       node2 = TextNode("This is a text node", TextType.ITALIC)
       self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
       node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
       node2 = TextNode("This is a text node", TextType.ITALIC)
       self.assertNotEqual(node, node2)

    
    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.CODE, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.CODE, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
       node = TextNode("This is a node", TextType.ITALIC, "https://www.boot.dev")
       node2 = TextNode("This is a text node", TextType.ITALIC)
       self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("test bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "test bold")

    def test_italic(self):
        node = TextNode("test italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "test italic")

    def test_code(self):
        node = TextNode("test code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "test code")

    def test_link(self):
        url = "https://bootdev.com"
        node = TextNode("test link", TextType.LINK, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "test link")
        self.assertEqual(html_node.props, {"href": url})

    def test_img(self):
        url = "https://bootdev.com"
        alt_text = "example img"
        node = TextNode(alt_text, TextType.IMAGE, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": url, "alt": alt_text})


if __name__ == "__main__":
    unittest.main()