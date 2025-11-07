import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_no_children_error(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None).to_html()

        self.assertEqual(str(context.exception), "Missing children object")

    def test_no_tag_error(self):
        with self.assertRaises(ValueError):
            child_node = LeafNode("span", "child")
            ParentNode(None, [child_node]).to_html()

    def test_with_multiple_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("a", "star", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(),
                         '<div><span>child</span><a href="https://www.google.com">star</a></div>')


if __name__ == "__main__":
    unittest.main()
