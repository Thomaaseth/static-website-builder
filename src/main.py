from textnode import *
from htmlnode import *
import re


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"Invalid type: {text_node.text_type}")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        index = text.find(delimiter)
        if index != -1:
            last_index = text.find(delimiter, index + len(delimiter))
            if last_index != -1:
                # Text before delimiter
                text_before = text[:index]
                if text_before:
                    new_nodes.append(TextNode(text_before, TextType.TEXT))
                
                # Text between delimiters
                text_between = text[index + len(delimiter):last_index]
                new_nodes.append(TextNode(text_between, text_type))
                
                # Text after delimiter - recursively process this part
                text_after = text[last_index + len(delimiter):]
                # Create a new TextNode and recursively process it
                after_nodes = split_nodes_delimiter([TextNode(text_after, TextType.TEXT)], delimiter, text_type)
                new_nodes.extend(after_nodes)
            else:
                # No closing delimiter found
                raise Exception(f"No closing delimiter found for {delimiter}")
        else:
            # No delimiter found in this node, keep it as is
            new_nodes.append(old_node)
    
    return new_nodes

def extract_markdown_images(text):
    new_img_tuple = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return new_img_tuple

def extract_markdown_links(text):
    new_links_tuple = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return new_links_tuple

            
def main():

    node = TextNode("test", TextType.LINK, "www.google.com")
    print(node)   

main()

