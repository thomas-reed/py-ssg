import re
import os
from enum import Enum
from textnode import TextType, TextNode
from leafnode import LeafNode
from parentnode import ParentNode

class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"

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

def isHeading(block):
  return re.match(r"^#{1,6} .+", block) is not None

def isCodeBlock(block):
  return re.fullmatch(r"^```[\s\S]*?```$", block) is not None

def isQuoteBlock(block):
  return re.fullmatch(r'(?:^\s*>.*\n?)+$', block, re.MULTILINE) is not None

def isUnorderedList(block):
  return re.fullmatch(r'^(?:\s*- .+\n?)+$', block, re.MULTILINE) is not None

def isOrderedList(block):
  return re.fullmatch(r'^(?:\s*\d+\. .+\n?)+$', block, re.MULTILINE) is not None

def block_to_block_type(md_block):
  checker_map = [
    (isHeading, BlockType.HEADING),
    (isCodeBlock, BlockType.CODE),
    (isQuoteBlock, BlockType.QUOTE),
    (isUnorderedList, BlockType.UNORDERED_LIST),
    (isOrderedList, BlockType.ORDERED_LIST),
  ]

  for checker, block_type in checker_map:
      if checker(md_block):
          return block_type
  return BlockType.PARAGRAPH

def handle_block_type(block_type, block):
  match block_type:
    case BlockType.CODE:
      cleaned_block = block.strip("`").lstrip("\n")
      return ParentNode(
        "pre",
        map(
          text_node_to_html_node,
          [
            TextNode(
              cleaned_block,
              TextType.CODE
            )
          ],
        ),
      )

    case BlockType.PARAGRAPH:
      cleaned_block = block.replace("\n", " ")
      return ParentNode(
        "p",
        map(
          text_node_to_html_node,
          text_to_textnodes(cleaned_block),
        ),
      )

    case BlockType.HEADING:
      i = 0
      while block[i] == '#':
        i += 1
      cleaned_block = block.lstrip("# ")
      return ParentNode(
        f"h{i}",
        map(
          text_node_to_html_node,
          text_to_textnodes(cleaned_block),
        ),
      )

    case BlockType.QUOTE:
      quote_text = " ".join(
        map(
          lambda line: re.sub(r'^\s*>\s*', '', line),
          block.splitlines(),
        )
      )
      return ParentNode(
        "blockquote",
        map(
          text_node_to_html_node,
          text_to_textnodes(quote_text),
        ),
      )

    case BlockType.UNORDERED_LIST:
      cleaned_block = "\n".join(
        map(
          lambda line: re.sub(r'^\s*-\s*', '', line),
          block.splitlines(),
        )
      )
      child_list = list(
        map(
          lambda line: ParentNode(
            "li",
            map(
              text_node_to_html_node,
              text_to_textnodes(line),
            ),
          ),
          cleaned_block.splitlines(),
        )
      )
      return ParentNode(
        "ul",
        child_list,
      )

    case BlockType.ORDERED_LIST:
      cleaned_block = "\n".join(
        map(
          lambda line: re.sub(r'^\s*\d+\.\s*', '', line),
          block.splitlines(),
        )
      )
      child_list = list(
        map(
          lambda line: ParentNode(
            "li",
            map(
              text_node_to_html_node,
              text_to_textnodes(line),
            ),
          ),
          cleaned_block.splitlines(),
        )
      )
      return ParentNode(
        "ol",
        child_list,
      )
      
    case _:
      raise Exception("invalid BlockType")

def markdown_to_html_node(markdown):
  md_blocks = markdown_to_blocks(markdown)
  html_nodes = []
  for block in md_blocks:
    block_type = block_to_block_type(block)
    html_nodes.append(handle_block_type(block_type, block))
  return ParentNode(
    "div",
    html_nodes,
  )

def extract_title(markdown):
  blocks = markdown_to_blocks(markdown)
  for block in blocks:
    if not isHeading(block):
      continue
    if block[1] == "#":
      continue
    return block[1:].strip()
    
def generate_page(from_path, template_path, dest_path):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}", end="...")
  with open(from_path, encoding="utf-8") as f:
    md = f.read()
  with open(template_path, encoding="utf-8") as f:
    template = f.read()
  md_html = markdown_to_html_node(md).to_html()
  title = extract_title(md)
  page_html = template.replace("{{ Title }}", title)
  page_html = page_html.replace("{{ Content }}", md_html)
  parent_dirs = os.path.dirname(dest_path)
  if parent_dirs:
    os.makedirs(parent_dirs, exist_ok=True)
  with open(dest_path, 'w', encoding="utf-8") as f:
    f.write(page_html)
  print("Done!")
  