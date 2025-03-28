import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_span(self):
        node = LeafNode("span", "Hello")
        self.assertEqual(node.to_html(), "<span>Hello</span>")

    def test_leaf_to_html_prop(self):
        node = LeafNode("p", "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<p href="https://www.google.com">Hello, world!</p>')

    def test_leaf_node_without_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_node_with_multiple_props(self):
        node = LeafNode("a", "Click me", {"href": "https://www.example.com", "class": "button", "id": "main-btn"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com" class="button" id="main-btn">Click me</a>')

    def test_leaf_node_with_empty_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_node_with_empty_string_value(self):
        node = LeafNode("div", "")
        self.assertEqual(node.to_html(), "<div></div>")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_nesting(self):
        great_grand_child_node = LeafNode("p", "great-grandchild")
        grandchild_node = ParentNode("h3", [great_grand_child_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("h1", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<h1><span><h3><p>great-grandchild</p></h3></span></h1>",
        )
    
    def test_to_html_with_no_tag(self):
        """Test that a ValueError is raised when tag is None"""
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "text")]).to_html()

    def test_to_html_with_no_children(self):
        """Test that a ValueError is raised when children is None"""
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_to_html_with_empty_children_list(self):
        """Test that an empty children list works correctly"""
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_with_multiple_children(self):
        """Test with multiple children at the same level"""
        parent = ParentNode("ul", [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2"),
            LeafNode("li", "Item 3")
        ])
        self.assertEqual(
            parent.to_html(),
            "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
        )

    def test_to_html_with_props(self):
        """Test that properties are included correctly"""
        node = ParentNode("div", [LeafNode("span", "text")], {"class": "container", "id": "main"})
        # The order of props might vary, so we'll check parts separately
        html = node.to_html()
        self.assertTrue(html.startswith("<div "))
        self.assertTrue(' class="container"' in html)
        self.assertTrue(' id="main"' in html)
        self.assertTrue(html.endswith('><span>text</span></div>'))

    def test_to_html_with_mixed_node_types(self):
        """Test with a mix of parent and leaf nodes at the same level"""
        parent = ParentNode("div", [
            LeafNode("span", "Text node"),
            ParentNode("ul", [
                LeafNode("li", "Item 1"),
                LeafNode("li", "Item 2")
            ]),
            LeafNode("p", "Another text node")
        ])
        self.assertEqual(
            parent.to_html(),
            "<div><span>Text node</span><ul><li>Item 1</li><li>Item 2</li></ul><p>Another text node</p></div>"
        )

    def test_to_html_with_deeply_nested_structure(self):
        """Test with a deeply nested structure (4+ levels)"""
        level4 = LeafNode("b", "Level 4")
        level3 = ParentNode("em", [level4])
        level2 = ParentNode("p", [level3, LeafNode("span", "Sibling at level 3")])
        level1 = ParentNode("div", [level2])
        
        self.assertEqual(
            level1.to_html(),
            "<div><p><em><b>Level 4</b></em><span>Sibling at level 3</span></p></div>"
        )

if __name__ == "__main__":
    unittest.main()