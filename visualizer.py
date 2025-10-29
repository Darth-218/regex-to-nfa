from graphviz import Digraph

class Counter:
    def __init__(self) -> None:
        self.current = 0
    def next(self):
        self.current += 1
        return self.current + 1

class Visualizer:
	def visualize_nfa(self, nfa):
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

		dot.render("nfa", format="svg")
		return dot.pipe(format='svg').decode('utf-8')

	def visualize_ast(self, ast):
		dot = Digraph()
		dot.attr(rankdir='TB')

		node_counter = Counter()

		def add_node(node, parent_id=None, edge_label=None):
			node_id = f'n{node_counter.next()}'

			if isinstance(node, dict):
				label = node.get('type', 'node')
			elif isinstance(node, (str, int, float, bool)) or node is None:
				label = '∅' if node is None else str(node)
			else:
				label = repr(node)

			dot.node(node_id, label)

			if parent_id is not None:
				if edge_label is not None:
					dot.edge(parent_id, node_id)
				else:
					dot.edge(parent_id, node_id)

			if isinstance(node, dict):
				for key, value in node.items():
					if key == 'type' or value is None or value == 0:
						continue
					add_child(value, node_id, key)
			elif isinstance(node, (list, tuple, set)):
				for index, value in enumerate(sorted(node) if isinstance(node, set) else node):
					add_child(value, node_id, index)

		def add_child(child, parent_id, edge_label):
			add_node(child, parent_id, edge_label)

		add_node(ast)

		dot.render("ast", format="svg")
		return dot.pipe(format='svg').decode('utf-8')
