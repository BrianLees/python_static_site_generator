import re
from enum import Enum
from textnode import TextNode, TextType
from leafnode import LeafNode


def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": f"{text_node.url}"})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": f"{text_node.url}", "alt": f"{text_node.text}"})


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_nodes = []
            split_text = node.text.split(delimiter)

            if len(split_text) % 2 == 0:
                raise Exception(
                    f"Invalid markdown syntax, unmatched: '{delimiter}'")

            for i in range(0, len(split_text)):
                node_type = text_type
                if i % 2 == 0:
                    node_type = TextType.TEXT
                split_nodes.append(TextNode(split_text[i], node_type))

            new_nodes.extend(split_nodes)
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)
            if len(images) > 0:
                image_nodes = []
                image = images[0]
                split_text = node.text.split(
                    f"![{image[0]}]({image[1]})", 1)
                image_nodes.append(TextNode(split_text[0], TextType.TEXT))
                image_nodes.append(
                    TextNode(image[0], TextType.IMAGE, image[1]))
                if len(split_text[1]) != 0:
                    image_nodes.append(
                        TextNode(split_text[1], TextType.TEXT))
                split_nodes = split_nodes_image(image_nodes)
                new_nodes.extend(split_nodes)
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            if len(links) > 0:
                link_nodes = []
                link = links[0]
                split_text = node.text.split(
                    f"[{link[0]}]({link[1]})", 1)
                link_nodes.append(TextNode(split_text[0], TextType.TEXT))
                link_nodes.append(
                    TextNode(link[0], TextType.LINK, link[1]))
                if len(split_text[1]) != 0:
                    link_nodes.append(
                        TextNode(split_text[1], TextType.TEXT))
                split_nodes = split_nodes_link(link_nodes)
                new_nodes.extend(split_nodes)
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def markdown_to_blocks(markdown):
    split_file = markdown.split("\n\n")
    final_blocks = []
    for line in split_file:
        if len(line) > 0:
            final_blocks.append(line.strip())
    return final_blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown):
    if re.match(r"^#{1,6} ", markdown):
        return BlockType.HEADING
    if re.match(r"^```[\s\S]*?```$", markdown):
        return BlockType.CODE

    starts_with_quote = True
    starts_with_unordered = True
    starts_with_ordered = True
    counter = 1
    for line in markdown.splitlines():
        if not (starts_with_ordered or starts_with_quote or starts_with_unordered):
            break
        if not re.match(r"^>", line):
            starts_with_quote = False
        if not re.match(r"^- ", line):
            starts_with_unordered = False
        if not re.match(rf"^{counter}\. ", line):
            starts_with_ordered = False
        counter += 1

    if starts_with_quote:
        return BlockType.QUOTE
    if starts_with_unordered:
        return BlockType.UNORDERED_LIST
    if starts_with_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
