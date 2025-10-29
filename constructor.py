import copy

class StateCounter:
    def __init__(self):
        self.count = 0

    def increment(self):
        s = self.count
        self.count += 1
        return s

class Constructor:
    def __init__(self):
        self.ast = None
        self.counter = StateCounter()


    def buildNfa(self, ast):
        if not isinstance(ast, dict):
            ast = {"type": "char", "value": ast}
        type_ = ast["type"]

        if type_ == "char":
            start = self.counter.increment()
            accept = self.counter.increment()
            transitions = {start: {ast["value"]: {accept}}}
            return start, accept, transitions

        elif type_ == "concat":
            start1, accept1, transitions1 = self.buildNfa(ast["left"])
            start2, accept2, transitions2 = self.buildNfa(ast["right"])

            transitions1.setdefault(accept1, {}).setdefault("_e", set()).add(start2)

            transitions = copy.deepcopy(transitions1)
            transitions.update(copy.deepcopy(transitions2))

            return start1, accept2, transitions

        elif type_ == "union":
            s = self.counter.increment()
            a = self.counter.increment()
            start1, accept1, transitions1 = self.buildNfa(ast["left"])
            start2, accept2, transitions2 = self.buildNfa(ast["right"])

            transitions = copy.deepcopy(transitions1)
            transitions.update(copy.deepcopy(transitions2))

            transitions.setdefault(s, {}).setdefault("_e", set()).update({start1, start2})
            transitions.setdefault(accept1, {}).setdefault("_e", set()).add(a)
            transitions.setdefault(accept2, {}).setdefault("_e", set()).add(a)

            return s, a, transitions

        elif type_ == "star":
            left_ast = ast["left"] 
            s = self.counter.increment()
            a = self.counter.increment()
            start1, accept1, transitions1 = self.buildNfa(ast["left"])
            transitions = copy.deepcopy(transitions1)

            transitions.setdefault(s, {}).setdefault("_e", set()).update({start1, a})
            transitions.setdefault(accept1, {}).setdefault("_e", set()).update({start1, a})

            return s, a, transitions
        
        elif type_ == "plus":
            left_ast = ast["left"] 
            s = self.counter.increment()
            a = self.counter.increment()
            start1, accept1, transitions1 = self.buildNfa(ast["left"])

            transitions = copy.deepcopy(transitions1)
            transitions.setdefault(s, {}).setdefault("_e", set()).add(start1)
            transitions.setdefault(accept1, {}).setdefault("_e", set()).update({start1, a})

            return s, a, transitions
        
        elif type_ == "optional":
            left_ast = ast["left"] 
            s = self.counter.increment()
            a = self.counter.increment()
            start1, accept1, transitions1 = self.buildNfa(ast["left"])

            transitions = copy.deepcopy(transitions1)
            transitions.setdefault(s, {}).setdefault("_e", set()).update({start1, a})
            transitions.setdefault(accept1, {}).setdefault("_e", set()).add(a)

            return s, a, transitions


    def construct_nfa(self, ast):
        self.ast = ast
        start, accept, transitions = self.buildNfa(self.ast)
        nfa = {
            "states": set(range(self.counter.count)),
            "start_state": start,
            "accept_states": {accept},
            "transitions": transitions,
        }
        return nfa


def main():

# (a|b)*abb:
#     ast_representation = {
#     "type": "concat",
#     "left": {
#         "type": "star",
#         "left": {
#             "type": "union",
#             "left": "a",
#             "right": "b"
#         },
#         "right": 0,
#     },
#     "right": {
#         "type": "concat",
#         "left": "a",
#         "right": {
#             "type": "concat",
#             "left": "b",
#             "right": "b"
#         }
#     }
# }

# Regex: ab
#     ast_representation = {
#     "type": "concat",
#     "left": {"type": "char", "value": "a"},
#     "right": {"type": "char", "value": "b"}
# }


# Regex: (ab)*|c
#     ast_representation = {
#     "type": "union",
#     "left": {
#         "type": "star",
#         "left": {
#             "type": "concat",
#             "left": {"type": "char", "value": "a"},
#             "right": {"type": "char", "value": "b"}
#         }
#     },
#     "right": {"type": "char", "value": "c"}
# }

    ast_representation = ast_representation = {
    "type": "question",
    "left": {"type": "concat", "left": "a", "right": "b"},
    "right": 0
}


    
    nfa_builder = Constructor()
    nfa = nfa_builder.construct_nfa(ast_representation)
    print(nfa)


if __name__ == "__main__":
    main()
