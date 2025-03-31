from textnode import *
from htmlnode import *
from blocknode import *
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

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
    
        images = extract_markdown_images(old_node.text)

        if not images:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        for alt_text, image_url in images:
            image_markdown = f"![{alt_text}]({image_url})"
            parts = remaining_text.split(image_markdown, 1)
            
            # Create a node for the text before the image (if not empty)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # Create a node for the image
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))

            # Update remaining text for next iteration
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        
        # After processing all images, don't forget to add any remaining text
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
    
        links = extract_markdown_links(old_node.text)

        if not links:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        for link_text, link_url in links:
            link_markdown = f"[{link_text}]({link_url})"
            parts = remaining_text.split(link_markdown, 1)
            
            # Create a node for the text before the link (if not empty)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # Create a node for the link
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            # Update remaining text for next iteration
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        
        # After processing all links, don't forget to add any remaining text
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    # For bold text - need to pass delimiter "**" and TextType.BOLD
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    
    # For italic text - need to pass delimiter "_" and TextType.ITALIC
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    
    # For code blocks - need to pass delimiter "`" and TextType.CODE
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown):
    new_blocks = []
    splitted_blocks = markdown.split("\n\n")
    for splitted_block in splitted_blocks:
        stripped = splitted_block.strip()
        if stripped:
            cleaned_lines = [line.strip() for line in stripped.split("\n")]
            normalized_block = "\n".join(cleaned_lines)
            new_blocks.append(normalized_block)

    return new_blocks

def block_to_block_type(block):
    if block.startswith('#'):
        count = 0
        for char in block:
            if char == '#':
                count += 1
            else:
                break
        if 1 <= count <= 6 and block[count] == ' ':
            return BlockType.HEADING
            
    if block.startswith('```') and block.rstrip().endswith('```'):
        return BlockType.CODE
    
    lines = block.split('\n')

    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith('- ') for line in lines):
        return BlockType.ULIST
    
    is_ordered = True
    for i, line in enumerate(lines, 1):
        if not line.startswith(f"{i}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.OLIST
    
    return BlockType.PARAGRAPH

def main():

    node = TextNode("test", TextType.LINK, "www.google.com")
    print(node)   

main()

