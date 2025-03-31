import unittest
from main import extract_markdown_images, extract_markdown_links

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

