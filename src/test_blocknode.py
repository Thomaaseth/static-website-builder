import unittest

from blocknode import *
from main import *

class TestBlockToBlockType(unittest.TestCase):
    
    def test_paragraph(self):
        block = "This is a simple paragraph with no special formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading_single_hash(self):
        block = "# This is a heading level 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_multiple_hashes(self):
        block = "### This is a heading level 3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_max_hashes(self):
        block = "###### This is a heading level 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_invalid_heading_too_many_hashes(self):
        block = "####### This has too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_invalid_heading_no_space(self):
        block = "#This has no space after the hash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code_block(self):
        block = "```\nfunction example() {\n  return 'Hello World';\n}\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_quote_block_single_line(self):
        block = ">This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_multiple_lines(self):
        block = ">This is the first line\n>This is the second line\n>This is the third line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_unordered_list_single_item(self):
        block = "- This is a single item"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
    
    def test_unordered_list_multiple_items(self):
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
    
    def test_ordered_list_single_item(self):
        block = "1. This is a single item"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
    
    def test_ordered_list_multiple_items(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
    
    def test_invalid_ordered_list_wrong_numbering(self):
        block = "1. First item\n3. Third item\n4. Fourth item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_invalid_ordered_list_not_starting_with_one(self):
        block = "2. Second item\n3. Third item\n4. Fourth item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_invalid_code_block_missing_end(self):
        block = "```\nSome code here without closing backticks"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_block(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_whitespace_only_block(self):
        block = "   \n  \n    "
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == '__main__':
    unittest.main()