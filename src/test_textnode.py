import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_initializes_properly(self):
        text = "This is a test node"
        type = TextType.CODE
        url = "https://www.example.com"
        node = TextNode(text, type, url)
        self.assertEqual(text, node.text)
        self.assertEqual(type, node.text_type)
        self.assertEqual(url, node.url)

    def test_no_url_is_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_invalid_text_type(self):
        with self.assertRaises(AttributeError):
            TextNode("this is bad", TextType.DOG)

    def test_eq_functions_properly_on_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_functions_properly_on_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_eq_functions_properly_on_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "example2.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
