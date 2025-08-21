import re
from textnode import TextType, TextNode
from leafnode import LeafNode

def text_node_to_html_node(text_node):
  match text_node.text_type:
    case TextType.TEXT:
      return LeafNode(None, text_node.text)
    case TextType.BOLD:
      return LeafNode("b", text_node.text)
    case TextType.ITALIC:
      return LeafNode("i", text_node.text)
    case TextType.CODE:
      return LeafNode("code", text_node.text)
    case TextType.LINK:
      return LeafNode(
        "a",
        text_node.text,
        { "href": text_node.url},
      )
    case TextType.IMAGE:
      return LeafNode(
        "img",
        "",
        {
          "src": text_node.url,
          "alt": text_node.text,
        },
      )
    case _:
      raise Exception(f"Invalid Text Type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for node in old_nodes:
    if (
      node.text_type != TextType.TEXT
      or delimiter is None
      or delimiter not in node.text
    ):
      new_nodes.append(node)
      continue
    working_list = node.text.split(delimiter)
    if len(working_list) % 2 == 0:
      raise Exception(f"Node '{node}' is missing a closing delimiter '{delimiter}'")
    for i, text in enumerate(working_list):
      if i % 2 == 0:
        new_nodes.append(TextNode(text, TextType.TEXT))
      else:
        new_nodes.append(TextNode(text, text_type))
  return list(filter(lambda node: node.text != "", new_nodes))

def split_nodes_image(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue
    images = extract_markdown_images(node.text)
    if len(images) == 0:
      new_nodes.append(node)
      continue
    rest = node.text
    for i in range(0, len(images)):
      tmp_list = rest.split(f"![{images[i][0]}]({images[i][1]})", 1)
      new_nodes.append(TextNode(tmp_list[0], TextType.TEXT))
      new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
      rest = tmp_list[1]
    new_nodes.append(TextNode(rest, TextType.TEXT))
  return list(filter(lambda node: node.text != "", new_nodes))

def split_nodes_link(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue
    links = extract_markdown_links(node.text)
    if len(links) == 0:
      new_nodes.append(node)
      continue
    rest = node.text
    for i in range(0, len(links)):
      tmp_list = rest.split(f"[{links[i][0]}]({links[i][1]})", 1)
      new_nodes.append(TextNode(tmp_list[0], TextType.TEXT))
      new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
      rest = tmp_list[1]
    new_nodes.append(TextNode(rest, TextType.TEXT))
  return list(filter(lambda node: node.text != "", new_nodes))
    
def extract_markdown_images(text):
  return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
  return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def text_to_textnodes(text):
  text_node = TextNode(text, TextType.TEXT)
  split_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
  split_nodes = split_nodes_delimiter(split_nodes, "_", TextType.ITALIC)
  split_nodes = split_nodes_delimiter(split_nodes, "`", TextType.CODE)
  split_nodes = split_nodes_image(split_nodes)
  split_nodes = split_nodes_link(split_nodes)
  return split_nodes

def markdown_to_blocks(text):
  return list(
    filter(
      lambda block: block != "",
      map(
        lambda block: block.strip(),
        text.split('\n\n')
      )
    )
  )
