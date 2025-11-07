from htmlnode import HtmlNode


class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        value = None
        super().__init__(tag, value, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError
        if not self.children:
            raise ValueError("Missing children object")
        html_string = f'<{self.tag}'
        props_string = ""

        if self.props is not None:
            for prop in self.props:
                props_string += f' {prop}="{self.props[prop]}"'

        html_string += props_string
        html_string += ">"

        for child in self.children:
            html_string += child.to_html()

        html_string += f'</{self.tag}>'
        return html_string
