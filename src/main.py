import os
import shutil
from textnode import TextNode, TextType

def build_site():
  if os.path.exists("public"):
    print("Removing existing public directory", end="...")
    try:
      shutil.rmtree("public")
    except Exception as e:
      print(f"Error:\n{e}")
    print("Done!")
  copy_static_to_public("static")
  
def copy_static_to_public(source):
  destination = os.path.join("public", "/".join(source.split("/")[1:]))
  print(f"Copying {source} to {destination}", end="...")
  if os.path.isfile(source):
    try:
      shutil.copy(source, destination)
    except Exception as e:
      print(f"Error:\n{e}")
    print("Done!")
  else:
    try:
      os.mkdir(destination)
    except Exception as e:
      print(f"Error:\n{e}")
    print("Done!")
    file_list = os.listdir(source)
    for file in file_list:
      path = os.path.join(source, file)
      copy_static_to_public(path)

def main():
  build_site()

if __name__ == "__main__":
  main()