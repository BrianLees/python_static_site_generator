

class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props

    def to_html(self):
        raise (NotImplementedError)

    def props_to_html(self):
        html_string = ""
        if self.props is not None:
            for prop in self.props:
                html_string += f' {prop}="{self.props[prop]}"'
        return html_string

    def __eq__(self, other):
        if not isinstance(other, HtmlNode):
            return NotImplemented

        # quick field checks
        if self.tag != other.tag or self.value != other.value:
            return False

        # dict equality is deep & order-independent by keys
        if self.props != other.props:
            return False

        # list equality is order-sensitive and recurses via each child's __eq__
        if len(self.children) != len(other.children):
            return False

        return all(c1 == c2 for c1, c2 in zip(self.children, other.children))

    def __repr__(self):
        if not self.children and not self.props:
            return f"HtmlNode(tag={self.tag!r}, value={self.value!r}, props={self.props!r})"

        props_repr = ""
        if self.props:
            props_repr = ",\n    ".join(
                f"{k!r}: {v!r}" for k, v in self.props.items())
            props_repr = f", props={{\n    {props_repr}\n}}"

        children_repr = ""
        if self.children:
            children_repr = ",\n    ".join(repr(child)
                                           for child in self.children)
            children_repr = f", children=[\n    {children_repr}\n]"

        return f"HtmlNode(tag={self.tag!r}, value={self.value!r}{props_repr}{children_repr})"
