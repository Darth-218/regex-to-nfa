from graphviz import Digraph

class GraphVisualizer:
    def visualize_nfa_svg(self, nfa):
        dot = Digraph()
        dot.attr(rankdir='LR')
        dot.node('', shape='none')
        dot.edge('', str(nfa['start_state']))

        for state in nfa['states']:
            shape = 'doublecircle' if state in nfa['accept_states'] else 'circle'
            dot.node(str(state), shape=shape)

        for src, transitions in nfa['transitions'].items():
            for symbol, dests in transitions.items():
                for dest in dests:
                    label = 'ε' if symbol == '_e' else symbol
                    dot.edge(str(src), str(dest), label=label)

        return dot.pipe(format='svg').decode('utf-8')
