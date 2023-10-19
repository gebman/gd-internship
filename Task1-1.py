# Create a script that accepts the file name and puts its extension to output.
# If there is no extension - an exception should be raised.

import argparse

parser = argparse.ArgumentParser(
    description="a simple script that returns the extension of a filename"
)
parser.add_argument("filename", type=str)
args = parser.parse_args()

dot_index = args.filename.rfind(".")
extension = args.filename[dot_index + 1 :]
if dot_index <= 0 or extension == "":
    raise Exception("this filename doesn't have an extension")

print(extension)
