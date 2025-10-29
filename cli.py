import parser, visualizer, constructor

while True:
    regex = input("Enter regex to parse: ")

    ast = parser.Parser().parse(regex)
    nfa = constructor.Constructor().construct_nfa(ast)

    visualizer.Visualizer().visualize_nfa(nfa)
    visualizer.Visualizer().visualize_ast(ast)
