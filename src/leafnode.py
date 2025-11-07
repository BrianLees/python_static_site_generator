from htmlnode import HtmlNode


class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        children = None
        super().__init__(tag, value, children, props)

    def to_html(self):
        props_string = ""
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        if self.props is not None:
            for prop in self.props:
                props_string += f' {prop}="{self.props[prop]}"'
        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"
