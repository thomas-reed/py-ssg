import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
  def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

  def test_leaf_to_html_no_tag(self):
    node = LeafNode(None, "Hello, world!")
    self.assertEqual(node.to_html(), "Hello, world!")

  def test_leaf_to_html_img_with_props(self):
    props = {
      "src": "image.jpg",
      "height": "500",
      "width": "600",
      "alt": "alt text for image",
    }
    node = LeafNode("img", "", props)
    self.assertEqual(
      node.to_html(), 
      '<img src="image.jpg" height="500" width="600" alt="alt text for image"></img>',
    )

  def test_leaf_to_html_a(self):
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    self.assertEqual(
      node.to_html(),
      '<a href="https://www.google.com">Click me!</a>',
    )

  def test_repr(self):
    node = LeafNode(
      "p",
      "What a strange world",
      {"class": "primary"},
    )
    self.assertEqual(
      node.__repr__(),
      "LeafNode(p, What a strange world, {'class': 'primary'})",
    )

if __name__ == "__main__":
  unittest.main()