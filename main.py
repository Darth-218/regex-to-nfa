import parser, constructor, visualizer
import streamlit as st

st.header("Regex to NFA Converter")

regex = st.text_input("Enter Regex", placeholder="Example Regex: (ab)*b+a")
st.caption("Valid operators: `|`, `*`, `+`, `?`")
clicked = st.button("Convert")

def get_nfa_info(nfa):
    transition_rows = []
    for state, transitions in sorted(nfa["transitions"].items()):
        for symbol, targets in transitions.items():
            transition_rows.append({
                "From State": state,
                "Symbol": symbol if symbol != "_e" else "ε",
                "To States": ", ".join(map(str, targets)),
            })

    states = [{
        "States": nfa["states"],
        "Start State": nfa["start_state"],
        "Accepted States": nfa["accept_states"]
    }]

    return states, transition_rows


def get_ast_info(node, parent=None, level=0, rows=None):
    if rows is None:
        rows = []
    if isinstance(node, str):  # leaf symbol
        rows.append({
            "Node Type": "symbol",
            "Parent": parent,
            "Level": level,
            "Value": node
        })
        return rows
    if isinstance(node, int):
        return rows

    rows.append({
        "Node Type": node["type"],
        "Parent": parent,
        "Level": level,
        "Value": node.get("value", "")
    })

    if "left" in node:
        get_ast_info(node["left"], parent=node["type"], level=level+1, rows=rows)
    if "right" in node:
        get_ast_info(node["right"], parent=node["type"], level=level+1, rows=rows)
    return rows

def process():
    try:
        ast = parser.Parser().parse(regex)
    except SyntaxError as e:
        st.error(e)
        return

    nfa = constructor.Constructor().construct_nfa(ast)

    nfa_info = get_nfa_info(nfa)
    ast_info = get_ast_info(ast)


    nfa_visualized = visualizer.GraphVisualizer().visualize_nfa(nfa)
    ast_visualized = visualizer.GraphVisualizer().visualize_ast(ast)

    st.subheader(f"For the Regex `{regex}`:")

    all_tab, nfa_tab, ast_tab = st.tabs(["All", "NFA", "AST"])

    with nfa_tab:
        st.image(nfa_visualized, width='stretch')
        st.dataframe(nfa_info[0], hide_index=True)
        st.dataframe(nfa_info[1], hide_index=True)

    with ast_tab:
        _, col, _ = st.columns([1, 2, 1])
        with col:
            st.image(ast_visualized, width='stretch')
        st.dataframe(ast_info, hide_index=True)

    with all_tab:

        st.markdown(f"### The NFA")
        st.image(nfa_visualized, width='stretch')
        st.dataframe(nfa_info[0], hide_index=True)
        st.dataframe(nfa_info[1], hide_index=True)

        st.markdown(f"#### The AST")
        _, col, _ = st.columns([1, 2, 1])
        with col:
            st.image(ast_visualized, width='stretch')
        st.dataframe(ast_info, hide_index=True)
    return

if (clicked and regex) or regex:
    process()
