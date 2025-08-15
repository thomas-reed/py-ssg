import unittest
from htmlnode import HtmlNode

class TestHtmlNode(unittest.TestCase):
  def test_props_to_html_no_props(self):
    node = HtmlNode("a", "broken link")
    self.assertEqual(node.props_to_html(), "")

  def test_props_to_html_single_prop(self):
    prop = {
      "href": "https://www.boot.dev"
    }
    node = HtmlNode(tag="a", value="valid link", props=prop)
    self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev"')

  def test_props_to_html_multi_prop(self):
    props = {
      "src": "image.jpg",
      "height": "500",
      "width": "600",
      "alt": "alt text for image"
    }
    node = HtmlNode(tag="img", props=props)
    self.assertEqual(
      node.props_to_html(),
      ' src="image.jpg" height="500" width="600" alt="alt text for image"',
    )

  def test_values(self):
    node = HtmlNode(
        "div",
        "I wish I could read",
    )
    self.assertEqual(
        node.tag,
        "div",
    )
    self.assertEqual(
        node.value,
        "I wish I could read",
    )
    self.assertEqual(
        node.children,
        None,
    )
    self.assertEqual(
        node.props,
        None,
    )

  def test_repr(self):
    node = HtmlNode(
      "p",
      "What a strange world",
      None,
      {"class": "primary"},
    )
    self.assertEqual(
      node.__repr__(),
      "HtmlNode(p, What a strange world, children: None, {'class': 'primary'})",
    )

if __name__ == "__main__":
  unittest.main()