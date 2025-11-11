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
    def test_image_images_extraction(self):
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

    def test_link_extraction_with_no_matches(self):
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

    def test_markdown_to_blocks_extra_spaces(self):
        md = """
This is **bolded** paragraph





This is another paragraph with _italic_ text and `code` here

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here",
            ],
        )

    def test_blocktype_paragraph(self):
        test_block = "This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(test_block), BlockType.PARAGRAPH)

    def test_blocktype_paragraph_with_multiline(self):
        test_block = "This\n # is\n```not code\n> or qoute\n- or unordered\n1. lists"
        self.assertEqual(block_to_block_type(test_block), BlockType.PARAGRAPH)

    def test_blocktype_heading(self):
        test_block = "# This"
        self.assertEqual(block_to_block_type(test_block), BlockType.HEADING)

    def test_blocktype_middle_heading(self):
        test_block = "### This"
        self.assertEqual(block_to_block_type(test_block), BlockType.HEADING)

    def test_blocktype_full_heading(self):
        test_block = "###### This"
        self.assertEqual(block_to_block_type(test_block), BlockType.HEADING)

    def test_blocktype_no_match_on_heading(self):
        test_block = "####### This"
        self.assertEqual(block_to_block_type(test_block), BlockType.PARAGRAPH)

    def test_blocktype_no_match_on_heading_without_space(self):
        test_block = "######This"
        self.assertEqual(block_to_block_type(test_block), BlockType.PARAGRAPH)

    def test_blocktype_code(self):
        test_block = "``` SOme code\nentered over\nseveral lines\n```"
        self.assertEqual(block_to_block_type(test_block), BlockType.CODE)

    def test_blocktype_code_no_closing(self):
        test_block = "``` SOme code\nentered over\nseveral lines"
        self.assertEqual(block_to_block_type(test_block), BlockType.PARAGRAPH)

    def test_blocktype_code_wrong_start(self):
        test_block = "`` SOme code\nentered over\nseveral lines\n```"
        self.assertEqual(block_to_block_type(test_block), BlockType.PARAGRAPH)

    def test_blocktype_quote(self):
        test_block = "> some code\n> entered over\n> several lines\n"
        self.assertEqual(block_to_block_type(test_block), BlockType.QUOTE)

    def test_blocktype_quote_missing_symbol(self):
        test_block = "> some code\nentered over\n> several lines\n"
        self.assertEqual(block_to_block_type(test_block), BlockType.PARAGRAPH)

    def test_blocktype_unordered_list(self):
        test_block = "- some code\n- entered over\n- several lines\n"
        self.assertEqual(block_to_block_type(
            test_block), BlockType.UNORDERED_LIST)

    def test_blocktype_unordered_list_missing_space(self):
        test_block = "- some code\n- entered over\n-several lines\n"
        self.assertEqual(block_to_block_type(
            test_block), BlockType.PARAGRAPH)

    def test_blocktype_unordered_list_but_start_with_space(self):
        test_block = " - some code\n - entered over\n - several lines\n"
        self.assertEqual(block_to_block_type(
            test_block), BlockType.PARAGRAPH)

    def test_blocktype_ordered_list(self):
        test_block = "1. some code\n2. entered over\n3. several lines\n"
        self.assertEqual(block_to_block_type(
            test_block), BlockType.ORDERED_LIST)

    def test_blocktype_ordered_list_missing_spaces(self):
        test_block = "1.some code\n2.entered over\n3.several lines\n"
        self.assertEqual(block_to_block_type(
            test_block), BlockType.PARAGRAPH)

    def test_blocktype_ordered_list_missing_one_line(self):
        test_block = "1.some code\n2.entered over\nseveral lines\n"
        self.assertEqual(block_to_block_type(
            test_block), BlockType.PARAGRAPH)

    def test_blocktype_ordered_list_wrong_order(self):
        test_block = "1. some code\n2. entered over\n2. several lines\n"
        self.assertEqual(block_to_block_type(
            test_block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            # "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quotes(self):
        md = """
This is a paragraph and a quote

> A special
> Quote by someone
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph and a quote</p><blockquote>A special\nQuote by someone</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
This is a paragraph and a list

- an item
- another item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph and a list</p><ul><li>an item</li><li>another item</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
This is a paragraph and a list

1. first item
2. second item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph and a list</p><ol><li>first item</li><li>second item</li></ol></div>"
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        )

    if __name__ == "__main__":
        unittest.main()
