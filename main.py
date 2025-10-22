import parser, visualizer

regex = input("Enter regex to parse: ")

ast = parser.Parser().parse(regex)
nfa = constructor.Constructor().construct(ast)

visualizer.GraphVisualizer().visualize(nfa)
