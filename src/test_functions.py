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

    # split node images
    def test_split_image_with_no_image(self):
        node = TextNode("Text without an image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual([node], new_nodes)

    def test_split_non_text_with_no_image(self):
        node = TextNode("Text without an image", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertEqual([node], new_nodes)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_duplicate_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    # split nodes link
    def test_split_link_with_no_link(self):
        node = TextNode("Text without an link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual([node], new_nodes)

    def test_split_non_text_with_no_link(self):
        node = TextNode("Text without an link", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertEqual([node], new_nodes)

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK,
                         "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_duplicate_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK,
                         "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK,
                         "https://www.boot.dev"),
            ],
            new_nodes,
        )

    # text_to_textnodes
    def test_split_everything(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(actual, expected)

    def test_split_simple(self):
        text = "This is simple"
        expected = [TextNode("This is simple", TextType.TEXT),]
        actual = text_to_textnodes(text)
        self.assertEqual(actual, expected)

    if __name__ == "__main__":
        unittest.main()
