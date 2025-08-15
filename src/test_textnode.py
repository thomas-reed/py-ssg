import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node, node2)

  def test_text_not_eq(self):
    node = TextNode("This is a text node", TextType.ITALIC)
    node2 = TextNode("This is a different text node", TextType.ITALIC)
    self.assertNotEqual(node, node2)

  def test_type_not_eq(self):
    node = TextNode("This is a text node", TextType.ITALIC)
    node2 = TextNode("This is a text node", TextType.IMAGE)
    self.assertNotEqual(node, node2)

  def test_url_not_eq(self):
    node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
    node2 = TextNode("This is a text node", TextType.LINK, "https://www.boots.dev")
    self.assertNotEqual(node, node2)
    
  def test_eq_url(self):
    node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
    node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
    self.assertEqual(node, node2)

  def test_repr(self):
    node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
    self.assertEqual(
        "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
    )

if __name__ == "__main__":
  unittest.main()