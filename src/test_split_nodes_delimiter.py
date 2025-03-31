import unittest

from textnode import *
from main import *

class TestSplitNode(unittest.TestCase):

    def test_split_nodes_delimiter(self):
        # Test case 1: No delimiters
        node = TextNode("This is plain text with no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is plain text with no delimiters")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        
        # Test case 2: Single pair of delimiters
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

        # Test case 3: Multiple pairs of delimiters
        node = TextNode("This has **two** bold **words**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This has ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "two")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " bold ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "words")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[4].text, "")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)