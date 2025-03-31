import unittest
from main import *
from textnode import *

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        # Test basic image extraction
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
        # Test multiple images
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ], matches)
        
        # Test no images
        matches = extract_markdown_images("This text has no images")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        # Test basic link extraction
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
        
        # Test multiple links
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"), 
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ], matches)

     # Test no links
        matches = extract_markdown_links("This text has no links")
        self.assertListEqual([], matches)
        
        # Test links mixed with images
        matches = extract_markdown_links(
            "This text has a ![image](https://example.com/img.jpg) and a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)
    
    def test_complex_markdown(self):
        # Test complex markdown with both links and images
        text = """
        # My Markdown Document
        
        Here's an ![example image](https://example.com/image.png) and a [link to follow](https://example.com).
        
        * List item with a [nested link](https://nested.example.com)
        * Another item with ![nested image](https://example.com/nested.jpg)
        
        > Blockquote with [another link](https://quote.example.com)
        """
        
        image_matches = extract_markdown_images(text)
        self.assertEqual(2, len(image_matches))
        self.assertIn(("example image", "https://example.com/image.png"), image_matches)
        self.assertIn(("nested image", "https://example.com/nested.jpg"), image_matches)
        
        link_matches = extract_markdown_links(text)
        self.assertEqual(3, len(link_matches))
        self.assertIn(("link to follow", "https://example.com"), link_matches)
        self.assertIn(("nested link", "https://nested.example.com"), link_matches)
        self.assertIn(("another link", "https://quote.example.com"), link_matches)

class TestImageAndLinkSplit(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        """Test that a node with no images remains unchanged"""
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_with_empty_text(self):
        """Test that nodes with empty text are not included"""
        node = TextNode("![image](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://example.com/img.png")],
            new_nodes
        )

    def test_split_images_multiple_nodes(self):
        """Test splitting multiple nodes"""
        node1 = TextNode("Text with ![img](https://example.com/1.png)", TextType.TEXT)
        node2 = TextNode("More ![text](https://example.com/2.png) here", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://example.com/1.png"),
                TextNode("More ", TextType.TEXT),
                TextNode("text", TextType.IMAGE, "https://example.com/2.png"),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes
        )
    
    def test_split_images_non_text_nodes(self):
        """Test that non-TEXT nodes are left unchanged"""
        node1 = TextNode("regular text", TextType.TEXT)
        node2 = TextNode("bold text", TextType.BOLD)
        node3 = TextNode("![img](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("regular text", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes
        )

    def test_split_links(self):
        """Test splitting a node with links"""
        node = TextNode(
            "This is text with a [link](https://example.com) and [another](https://example.org/page)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.LINK, "https://example.org/page"),
            ],
            new_nodes
        )

    def test_split_links_no_links(self):
        """Test that a node with no links remains unchanged"""
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_with_empty_text(self):
        """Test that nodes with empty text are not included"""
        node = TextNode("[link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://example.com")],
            new_nodes
        )
