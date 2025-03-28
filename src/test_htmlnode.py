import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_node_attributes(self):
        children = [HTMLNode("span", "child", None, None)]
        node = HTMLNode("p", "test", children, {"href": "https://www.google.com"})

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "test")
        self.assertEqual(node.props, {"href": "https://www.google.com"})

        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "span")
        self.assertEqual(node.children[0].value, "child")

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

    def test_node_diff_attributes(self):
        children = [HTMLNode("span", "child", None, None)]
        children2 = [HTMLNode("span", "child", None, {"href": "https://www.google.com"})]

        node = HTMLNode("h1", "test", children, {"href": "https://www.google.com"})
        node2 = HTMLNode("span", "test", children, {"href": "https://www.google.com"})

        node3 = HTMLNode("h1", "test", [children, children2], {"href": "https://www.google.com"})

        self.assertNotEqual(node.tag, node2.tag)
        self.assertNotEqual(node3.children[0], node3.children[1])




if __name__ == "__main__":
    unittest.main()