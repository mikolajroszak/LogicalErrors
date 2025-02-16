import os
import sys
from pycparser import c_parser, c_ast
def PrintPreorder(node, AST_file):
	children = (list)(node.children())
	for (child_name, child) in children:
		name = child.__class__.__name__
		AST_file.write(name+"\n")
		PrintPreorder(child, AST_file)

ProgramFileName = sys.argv[1]
pwd = "/home/krithika/correct_logical_errors/"
command = "gcc "+ProgramFileName+" -E -std=c99 -I "+pwd+"utils/fake_libc_include > "+pwd+"preprocessed.txt"
os.system(command)
PreprocessedFile = open(pwd+"preprocessed.txt")
Program = PreprocessedFile.read()
diff = Program.count('{')-Program.count('}')
while(diff):
	Program = Program+"\n}"
	diff = diff-1
PreprocessedFile.close()
#os.system("rm "+pwd+"preprocessed.txt")
parser = c_parser.CParser()
ast = parser.parse(Program, filename='<none>')
AST_file = open("AST_file.txt", "w")
PrintPreorder(ast, AST_file)
AST_file.close()
