import unittest
from textnode import TextNode, TextType
from conversions import text_node_to_html_node

class TestConversions(unittest.TestCase):
  def test_conv_text_to_html(self):
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

  def test_conv_bold_to_html(self):
    node = TextNode("This is a bold node", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "b")
    self.assertEqual(html_node.value, "This is a bold node")

  def test_conv_italic_to_html(self):
    node = TextNode("This is an italic node", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "i")
    self.assertEqual(html_node.value, "This is an italic node")

  def test_conv_code_to_html(self): 
    node = TextNode("This is a code node", TextType.CODE)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "code")
    self.assertEqual(html_node.value, "This is a code node")

  def test_conv_link_to_html(self):
    node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.value, "This is a link node")
    self.assertEqual(html_node.props["href"], "https://www.boot.dev")

  def test_conv_image_to_html(self):
    node = TextNode("This is a image node", TextType.IMAGE, "public/image.jpg")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.value, "")
    self.assertEqual(html_node.props["src"], "public/image.jpg")
    self.assertEqual(html_node.props["alt"], "This is a image node")


if __name__ == "__main__":
  unittest.main()