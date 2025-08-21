import unittest
from textnode import TextNode, TextType
from utilities import (
  text_node_to_html_node,
  split_nodes_delimiter,
  extract_markdown_images,
  extract_markdown_links,
  split_nodes_image,
  split_nodes_link,
  text_to_textnodes,
  markdown_to_blocks,
)

class TestUtilities(unittest.TestCase):
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

  def test_split_nodes_single_text(self):
    node = TextNode("This is just text", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], None, TextType.TEXT)
    self.assertEqual(len(new_nodes), 1)
    self.assertEqual(new_nodes[0].text, "This is just text")
    self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

  def test_split_nodes_single_code_block(self):
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(len(new_nodes), 3)
    self.assertEqual(new_nodes[0].text, "This is text with a ")
    self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[1].text, "code block")
    self.assertEqual(new_nodes[1].text_type, TextType.CODE)
    self.assertEqual(new_nodes[2].text, " word")
    self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

  def test_split_nodes_double_italic_block(self):
    node = TextNode("Here is one `italic block` and `another italic block`, two total", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.ITALIC)
    self.assertEqual(len(new_nodes), 5)
    self.assertEqual(new_nodes[0].text, "Here is one ")
    self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[1].text, "italic block")
    self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
    self.assertEqual(new_nodes[2].text, " and ")
    self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[3].text, "another italic block")
    self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)
    self.assertEqual(new_nodes[4].text, ", two total")
    self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

  def test_split_nodes_code_block_in_front(self):
    node = TextNode("`code block` is at the beginning", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(len(new_nodes), 2)
    self.assertEqual(new_nodes[0].text, "code block")
    self.assertEqual(new_nodes[0].text_type, TextType.CODE)
    self.assertEqual(new_nodes[1].text, " is at the beginning")
    self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

  def test_split_nodes_bold_at_end(self):
    node = TextNode("This text should be **bold**", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertEqual(len(new_nodes), 2)
    self.assertEqual(new_nodes[0].text, "This text should be ")
    self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[1].text, "bold")
    self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

  def test_split_nodes_uneven_delimiters(self):
    node = TextNode("This text **should be **bold**", TextType.TEXT)
    with self.assertRaises(Exception) as context:
      new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)    
    self.assertEqual(str(context.exception), "Node 'TextNode(This text **should be **bold**, text, None)' is missing a closing delimiter '**'")
  
  def test_split_nodes_bold_and_italic(self):
    node = TextNode("**bold** and _italic_", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    self.assertEqual(len(new_nodes), 3)
    self.assertEqual(new_nodes[0].text, "bold")
    self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
    self.assertEqual(new_nodes[1].text, " and ")
    self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[2].text, "italic")
    self.assertEqual(new_nodes[2].text_type, TextType.ITALIC)

  def test_extract_markdown_images_1(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual(
      [
        ("image", "https://i.imgur.com/zjjcJKZ.png")
      ],
      matches,
    )

  def test_extract_markdown_images_2(self):
    matches = extract_markdown_images(
        "This is text with 2 image links ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    )
    self.assertListEqual(
      [
        ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
        ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
      ],
      matches,
    )

  def test_extract_markdown_images_no_match(self):
    matches = extract_markdown_images(
        "This is text with 2 image links ![rick [roll]](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.(imgur).com/fJRm4Vk.jpeg)"
    )
    self.assertListEqual([], matches)

  def test_extract_markdown_link_1(self):
    matches = extract_markdown_links(
        "This is text with a link [to boot dev](https://www.boot.dev)"
    )
    self.assertListEqual(
      [
        ("to boot dev", "https://www.boot.dev"),
      ],
      matches,
    )

  def test_extract_markdown_links_2(self):
    matches = extract_markdown_links(
        "This is text with 2 links: [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    )
    self.assertListEqual(
      [
        ("to boot dev", "https://www.boot.dev"),
        ("to youtube", "https://www.youtube.com/@bootdotdev"),
      ],
      matches,
    )

  def test_extract_markdown_links_no_match(self):
    matches = extract_markdown_links(
      "This is text with 3 links: [to boot [dev]](https://www.boot.dev), [to youtube](https://www.(youtube).com/@bootdotdev), and ![to google](https://www.google.com)"
    )
    self.assertListEqual([], matches)

  def test_split_images_0(self):
    node = TextNode(
      "This is text with no included images",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("This is text with no included images", TextType.TEXT),
      ],
      new_nodes,
    )

  def test_split_images_1(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and some more text",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and some more text", TextType.TEXT),
      ],
      new_nodes,
    )

  def test_split_images_2(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.TEXT),
        TextNode(
          "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
        ),
      ],
      new_nodes,
    )

  def test_split_links_0(self):
    node = TextNode(
      "This is text with no included links",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode("This is text with no included links", TextType.TEXT),
      ],
      new_nodes,
    )

  def test_split_links_1(self):
    node = TextNode(
      "This is text with a [link](https://www.boot.dev) and some more text",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and some more text", TextType.TEXT),
      ],
      new_nodes,
    )

  def test_split_links_2(self):
    node = TextNode(
      "This is text with a [link](https://www.boot.dev) and another [second link](https://www.google.com)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and another ", TextType.TEXT),
        TextNode(
          "second link", TextType.LINK, "https://www.google.com"
        ),
      ],
      new_nodes,
    )

  def test_text_to_textnodes(self):
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    new_nodes = text_to_textnodes(text)
    self.assertListEqual(
      [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
      ],
        new_nodes,
    )

  def test_text_to_textnodes_just_text(self):
    text = "This is just plain text, making sure there's no extra nodes generated."
    new_nodes = text_to_textnodes(text)
    self.assertListEqual(
      [
        TextNode("This is just plain text, making sure there's no extra nodes generated.", TextType.TEXT),
      ],
        new_nodes,
    )

  def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
      blocks,
      [
        "This is **bolded** paragraph",
        "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
        "- This is a list\n- with items",
      ],
    )

  def test_markdown_to_blocks_strip_newlines(self):
    md = """





This is a single paragraph with loads of newlines







"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
      blocks,
      [
        "This is a single paragraph with loads of newlines",
      ],
    )

  def test_markdown_to_blocks_extra_newlines(self):
    md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items


"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
      blocks,
      [
        "This is **bolded** paragraph",
        "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
        "- This is a list\n- with items",
      ],
    )

if __name__ == "__main__":
  unittest.main()