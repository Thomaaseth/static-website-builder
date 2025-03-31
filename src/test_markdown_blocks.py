import unittest
from main import *
from textnode import *

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_with_extra_newlines(self):
        md = """
    # Title


    This is a paragraph with **bold** text.


    - Item 1
    - Item 2
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Title",
                "This is a paragraph with **bold** text.",
                "- Item 1\n- Item 2",
            ],
        )

    def test_markdown_multiline_paragraph(self):
        md = """
    # A Heading

    Here is some text that
        spans multiple lines with inconsistent
        indentation.

    Another block follows.
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# A Heading",
                "Here is some text that\nspans multiple lines with inconsistent\nindentation.",
                "Another block follows.",
            ],
        )
    
    def test_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            []
        )
    
    def test_whitespace_only(self):
        md = "   \n   \n\n    "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            []
        )
    
    def test_list_blocks(self):
        md = """
    - This is a list
    - With several
        - Nested items
            - That are indented
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- This is a list\n- With several\n- Nested items\n- That are indented",
            ],
        )