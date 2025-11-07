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
