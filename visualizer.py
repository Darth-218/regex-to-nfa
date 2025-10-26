import graphviz

from graphviz import Digraph
from itertools import count

class GraphVisualizer:
	@staticmethod
	def visualize_nfa_svg(nfa):
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

	@staticmethod
	def visualize_ast(ast):
		dot = Digraph()
		dot.attr(rankdir='TB')

		node_counter = count()

		def add_node(node, parent_id=None, edge_label=None):
			node_id = f'n{next(node_counter)}'

			if isinstance(node, dict):
				label = node.get('type', 'node')
			elif isinstance(node, (str, int, float, bool)) or node is None:
				label = '∅' if node is None else str(node)
			else:
				label = repr(node)

			dot.node(node_id, label)

			if parent_id is not None:
				if edge_label is not None:
					dot.edge(parent_id, node_id, label=str(edge_label))
				else:
					dot.edge(parent_id, node_id)

			if isinstance(node, dict):
				for key, value in node.items():
					if key == 'type' or value is None:
						continue
					add_child(value, node_id, key)
			elif isinstance(node, (list, tuple, set)):
				for index, value in enumerate(sorted(node) if isinstance(node, set) else node):
					add_child(value, node_id, index)

		def add_child(child, parent_id, edge_label):
			add_node(child, parent_id, edge_label)

		add_node(ast)

		return dot.pipe(format='svg').decode('utf-8')



#  Example usage
if __name__ == "__main__":
    nfa = {
        "states": {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12},
        "start_state": 0,
        "accept_states": {11},
        "transitions": {
            0: {"_e": {1, 7}},
            1: {"a": {2}},
            2: {"_e": {6}},
            7: {"b": {8}},
            8: {"_e": {6}},
            6: {"_e": {0, 9}},
            9: {"a": {10}},
            10: {"b": {11}},
            11: {"b": {12}}
        }
    }

    svg = GraphVisualizer.visualize_nfa_svg(nfa)
    with open("nfa.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Wrote nfa.svg")