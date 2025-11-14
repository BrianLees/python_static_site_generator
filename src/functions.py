import re
import os
from enum import Enum
from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from htmlnode import HtmlNode


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
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


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


def markdown_to_html_node(markdown):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    # print(f"All of the blocks: {blocks}")
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.CODE:
            children = text_to_code(block)
            code_node = ParentNode(block_type.value, children)
            html_nodes.append(ParentNode("pre", [code_node]))
        elif block_type == BlockType.QUOTE:
            children = text_to_quote(block)
            html_nodes.append(ParentNode(block_type.value, children))
        elif block_type == BlockType.UNORDERED_LIST:
            children = text_to_unordered_list(block)
            html_nodes.append(ParentNode(block_type.value, children))
        elif block_type == BlockType.ORDERED_LIST:
            children = text_to_ordered_list(block)
            html_nodes.append(ParentNode(block_type.value, children))
        elif block_type == BlockType.HEADING:
            heading_size, heading_text = text_to_heading(block)
            html_nodes.append(
                LeafNode(f"{block_type.value}{heading_size}", heading_text))
        else:
            children = text_to_children(block)
            html_nodes.append(ParentNode(block_type.value, children))
    html_doc = ParentNode("div", html_nodes)
    # print(f"Full structure:\n {html_doc}")
    # print(f"Output:\n{repr(html_doc.to_html())}")
    return html_doc


def text_to_children(text):
    html_nodes = []
    nodes = text_to_textnodes(text.replace("\n", " "))
    for node in nodes:
        created_node = text_node_to_html_node(node)
        html_nodes.append(created_node)
    return html_nodes


def text_to_code(text):
    cleaned_text = text.replace("```", "").lstrip()
    text_node = text_node_to_html_node(TextNode(cleaned_text, TextType.TEXT))
    return [text_node]


def text_to_quote(text):
    cleaned_text = text.replace("> ", "")
    text_node = text_node_to_html_node(TextNode(cleaned_text, TextType.TEXT))
    return [text_node]


def text_to_unordered_list(text):
    list_nodes = []
    for line in text.splitlines():
        cleaned_text = line.replace("- ", "")
        children = text_to_children(cleaned_text)
        list_nodes.append(ParentNode("li", children))
    return list_nodes


def text_to_ordered_list(text):
    list_nodes = []
    for line in text.splitlines():
        cleaned_text = line[3:]
        children = text_to_children(cleaned_text)
        list_nodes.append(ParentNode("li", children))
    return list_nodes


def text_to_heading(text):
    cleaned_text = ""
    counter = 0
    for ch in text:
        if ch == "#":
            counter += 1
        else:
            cleaned_text += ch

    return counter, cleaned_text.lstrip()


def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Markdown file does not contain a title")


def generate_page(from_path, template_path, destination_path):
    print(
        f"Generating Markdown from {from_path} to {destination_path} using {template_path}")
    markdown = get_file_contents(from_path)
    template = get_file_contents(template_path)

    html_object = markdown_to_html_node(markdown)
    html_string = html_object.to_html()
    title = extract_title(markdown)

    template_with_title = template.replace("{{ Title }}", title)
    template_with_content = template_with_title.replace(
        "{{ Content }}", html_string)

    destination_dir = os.path.dirname(destination_path)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    with open(destination_path, "w") as new_file:
        new_file.write(template_with_content)

    print("...Markdown generation completed.")
    return False


def get_file_contents(file):
    file = open(file)
    return file.read()


def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        item_name = os.path.join(dir_path_content, item)
        destination_name = os.path.join(dest_dir_path, item)

        if os.path.isfile(item_name) and item[-3:] == ".md":
            new_file = destination_name.replace(".md", ".html")
            generate_page(item_name, template_path, new_file)
        elif os.path.isdir(item_name):
            generate_pages_recursively(
                item_name, template_path, destination_name)
