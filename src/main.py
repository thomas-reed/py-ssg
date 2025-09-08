import os
import sys
import shutil
from textnode import TextNode, TextType
from utilities import (generate_page)

def copy_static_files_to_public():
  if os.path.exists("public"):
    print("Removing existing public directory", end="...")
    try:
      shutil.rmtree("public")
    except Exception as e:
      print(f"Error:\n{e}")
    print("Done!")
  copy_static_recursive("static")
  
def copy_static_recursive(source):
  destination = os.path.join("public", "/".join(source.split("/")[1:]))
  print(f"Copying {source} to {destination}", end="...")
  if os.path.isfile(source):
    try:
      shutil.copy(source, destination)
    except Exception as e:
      print(f"Error:\n{e}")
    print("Done!")
  else:
    os.makedirs(destination, exist_ok=True)
    print("Done!")
    content_list = os.listdir(source)
    for item in content_list:
      path = os.path.join(source, item)
      copy_static_recursive(path)

def generate_pages_recursive(
  dir_path_content,
  template_path,
  dest_dir_path,
  basepath
):
  item_name = os.path.basename(dir_path_content)
  if os.path.isfile(dir_path_content):
    filename, ext = os.path.splitext(item_name)
    if ext == ".md":
      new_file = os.path.join(dest_dir_path, filename + ".html")
      generate_page(dir_path_content, template_path, new_file, basepath)
    else:
      print(f"Skipping file {item_name}, as it is not markdown")
  else:
    contents = os.listdir(dir_path_content)
    for item in contents:
      next_item_path = os.path.join(dir_path_content, item)
      next_dest_path = (
        dest_dir_path if os.path.isfile(next_item_path)
        else os.path.join(dest_dir_path, item)
      )
      generate_pages_recursive(
        next_item_path,
        template_path,
        next_dest_path,
        basepath
      )

def main():
  # first cmd line arg should be the root path for site if different from '/'
  basepath = sys.argv[1] if len(sys.argv) >= 2 else "/"
  copy_static_files_to_public()
  generate_pages_recursive(
    "content",
    "template.html",
    "docs",
    basepath,
  )

if __name__ == "__main__":
  main()