#Create a script that accepts the file name and puts its extension to output. 
#If there is no extension - an exception should be raised.

import sys
 
if len(sys.argv)<2:
    raise Exception("argument missing! provide 1 argument with a filename")
elif len(sys.argv)>2:
    raise Exception("too many arguments!")

filename = sys.argv[1]

dot_index = filename.rfind(".")
extension = filename[dot_index+1:]
if dot_index <=0 or extension=="":
    raise Exception("not a valid filename")

print(f"File extension: {filename[dot_index+1:]}")
