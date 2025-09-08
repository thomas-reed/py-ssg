import unittest
from textnode import TextNode, TextType
from utilities import (
  BlockType,
  text_node_to_html_node,
  split_nodes_delimiter,
  extract_markdown_images,
  extract_markdown_links,
  split_nodes_image,
  split_nodes_link,
  text_to_textnodes,
  markdown_to_blocks,
  block_to_block_type,
  markdown_to_html_node,
  extract_title,
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

  def test_block_to_block_type_heading(self):
    md_block = "### This is a heading"
    self.assertEqual(block_to_block_type(md_block), BlockType.HEADING)

  def test_block_to_block_type_code(self):
    md_block = """```
This is a code block.
Everything in here should be inside the code block.
Including this
And this
```"""
    self.assertEqual(block_to_block_type(md_block), BlockType.CODE)

  def test_block_to_block_type_quote(self):
    md_block = """> Hear me now,
  > Quote me later.
    > Like for real, dawg"""
    self.assertEqual(block_to_block_type(md_block), BlockType.QUOTE)

  def test_block_to_block_type_unordered_list(self):
    md_block = """ - This is an unordered list
 - I need to do this
 - And this
 - And this too"""
    self.assertEqual(block_to_block_type(md_block), BlockType.UNORDERED_LIST)

  def test_block_to_block_type_ordered_list(self):
      md_block = """ 5. This is an ordered list
  8. I need to do this first
  1. And this next
  4. And this last"""
      self.assertEqual(block_to_block_type(md_block), BlockType.ORDERED_LIST)

  def test_markdown_to_html_node_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

  def test_markdown_to_html_node_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
  
  def test_markdown_to_html_node_quote(self):
    md = """
> This is quoted text that has some _italics_
  > and here's more quote with some **bold** and `code` text as well
  > and here's just some regular text
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><blockquote>This is quoted text that has some <i>italics</i> and here's more quote with some <b>bold</b> and <code>code</code> text as well and here's just some regular text</blockquote></div>",
    )

  def test_markdown_to_html_node_heading(self):
    md = """
# **H1** Heading

Here's some text under the bold H1 heading

### _H3_ Heading

Here's some other text under the italicized H3 heading
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><h1><b>H1</b> Heading</h1><p>Here's some text under the bold H1 heading</p><h3><i>H3</i> Heading</h3><p>Here's some other text under the italicized H3 heading</p></div>",
    )

  def test_markdown_to_html_node_unordered_list(self):
    md = """
- unordered list item 1 that has some _italic_ text
  - unordered list item 2 that has some **bold** text
 - unordered list item 3 that has some `code`
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><ul><li>unordered list item 1 that has some <i>italic</i> text</li><li>unordered list item 2 that has some <b>bold</b> text</li><li>unordered list item 3 that has some <code>code</code></li></ul></div>",
    )

  def test_markdown_to_html_node_ordered_list(self):
    md = """
5. ordered list item 1 that has some _italic_ text
  2. ordered list item 2 that has some **bold** text
 456. ordered list item 3 that has some `code`
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><ol><li>ordered list item 1 that has some <i>italic</i> text</li><li>ordered list item 2 that has some <b>bold</b> text</li><li>ordered list item 3 that has some <code>code</code></li></ol></div>",
    )

  def test_extract_title(self):
    md = """
## This is not the title

### This is not the title either

[this is a link](https://www.google.com)

# This is the title

# This could be considered a title
"""
    self.assertEqual(extract_title(md), "This is the title")

  def test_extract_title_bad_spacing(self):
    md = """
## This is not the title

      # This is the title
"""
    self.assertEqual(extract_title(md), "This is the title")



if __name__ == "__main__":
  unittest.main()