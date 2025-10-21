import parser

regex = input("Enter regex to parse: ")
print(parser.Parser().parse(regex))
