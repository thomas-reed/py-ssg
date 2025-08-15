from htmlnode import HtmlNode

class ParentNode(HtmlNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag=tag, children=children, props=props)

  def to_html(self):
    if self.tag is None:
      raise ValueError("ParentNode must have a tag")
    if self.children is None:
      raise ValueError("ParentNode must have children")
    children_html = ""
    for child in self.children:
        children_html += child.to_html()
    return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

  def __repr__(self):
    return f"ParentNode({self.tag}, children: {self.children}, {self.props})"