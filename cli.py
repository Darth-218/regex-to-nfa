import parser, visualizer, constructor

while True:
    regex = input("Enter regex to parse: ")

    ast = parser.Parser().parse(regex)
    nfa = constructor.Constructor(ast).construct_nfa()

    visualizer.GraphVisualizer().visualize_nfa(nfa)
    visualizer.GraphVisualizer().visualize_ast(ast)
