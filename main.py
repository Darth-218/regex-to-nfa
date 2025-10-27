import parser, visualizer, constructor

regex = input("Enter regex to parse: ")

ast = parser.Parser().parse(regex)
nfa = constructor.construct_nfa(ast)

visualizer.GraphVisualizer().visualize_nfa(nfa)
visualizer.GraphVisualizer().visualize_ast(ast)
