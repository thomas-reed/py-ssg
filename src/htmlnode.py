class HtmlNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError("To be implemented by child classes")

  def props_to_html(self):
    if not self.props:
      return ""
    html_attrs = ""
    for prop in self.props.items():
      html_attrs += f' {prop[0]}="{prop[1]}"'
    return html_attrs

  def __repr__(self):
    return f"HtmlNode({self.tag}, {self.value}, children: {self.children}, {self.props})"