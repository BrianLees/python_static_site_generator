import unittest

from htmlnode import HtmlNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HtmlNode("p", "Just a paragraph")
        node2 = HtmlNode("p", "Just a paragraph")
        self.assertEqual(node, node2)

    def test_initializes_properly(self):
        tag = "p"
        value = "This is a test node"
        children = [HtmlNode("p", "Just a paragraph")]
        props = {"href": "http://www.example.com"}
        node = HtmlNode(tag, value, children, props)
        self.assertEqual(tag, node.tag)
        self.assertEqual(value, node.value)
        self.assertEqual(children, node.children)
        self.assertEqual(props, node.props)

    def test_all_default_to_none(self):
        node = HtmlNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, None)

    def test_eq_functions_properly_on_tag(self):
        node = HtmlNode("p")
        node2 = HtmlNode("a")
        self.assertNotEqual(node, node2)

    def test_eq_functions_properly_on_value(self):
        node = HtmlNode(value="p")
        node2 = HtmlNode(value="a")
        self.assertNotEqual(node, node2)

    def test_eq_functions_properly_on_children(self):
        node = HtmlNode(children=[HtmlNode("p", "Just a paragraph")])
        node2 = HtmlNode(children=[HtmlNode("a", "Just a link")])
        self.assertNotEqual(node, node2)

    def test_eq_functions_properly_on_children(self):
        node = HtmlNode(props={"href": "http://www.example.com"})
        node2 = HtmlNode(props={"href": "http://www.example.com/login"})
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
