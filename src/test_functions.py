import unittest

from parentnode import ParentNode
from textnode import TextNode, TextType
from functions import *


class TestFunctions(unittest.TestCase):
    # TESTING text_node_to_html_node
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "www.google.com"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE,
                        "www.example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
                         "src": "www.example.com/image.png", "alt": "This is an image node"})

    # TESTING split_nodes_delimiter
    def test_bold_split(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_italic_split(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_code_split(self):
        node = TextNode("This is text with a `code` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_multiple_code_split(self):
        node = TextNode("This is `text` with a `code` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.CODE),
            TextNode(" with a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_mismatch_split(self):
        with self.assertRaises(Exception) as cm:

            node = TextNode("This is text with a **code word", TextType.TEXT)
            split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(str(cm.exception),
                         "Invalid markdown syntax, unmatched: '**'")

    # extract_markdown_images
    def test_image_link_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected_matches = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
                            ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertEqual(matches, expected_matches)

    def test_image_extraction_with_no_matches(self):
        text = "This is text without images"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [])

    # extract markdown links
    def test_image_link_extraction(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected_matches = [('to boot dev', 'https://www.boot.dev'),
                            ('to youtube', 'https://www.youtube.com/@bootdotdev')]
        self.assertEqual(matches, expected_matches)

    def test_image_extraction_with_no_matches(self):
        text = "This is text without links"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [])


if __name__ == "__main__":
    unittest.main()
