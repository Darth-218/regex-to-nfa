import parser, constructor, visualizer
import streamlit as st

st.header("Regex to NFA Converter")

regex = st.text_input("Enter Regex")
clicked = st.button("Convert")

def process():
    try:
        ast = parser.Parser().parse(regex)
    except SyntaxError as e:
        st.error(e)
        return

    nfa = constructor.construct_nfa(ast)

    nfa_visualized = visualizer.GraphVisualizer().visualize_nfa(nfa)
    ast_visualized = visualizer.GraphVisualizer().visualize_ast(ast)

    st.subheader(f"For the Regex `{regex}`:")

    nfa_tab, ast_tab, all_tab = st.tabs(["NFA", "AST", "All"])

    with nfa_tab:
        st.image(nfa_visualized, use_container_width=True)

    with ast_tab:
        _, col, _ = st.columns([1, 2, 1])
        with col:
            st.image(ast_visualized, use_container_width=True)

    with all_tab:

        st.markdown(f"### The NFA")
        st.image(nfa_visualized, use_container_width=True)

        st.markdown(f"#### The AST")
        _, col, _ = st.columns([1, 2, 1])
        with col:
            st.image(ast_visualized, use_container_width=True)

if (clicked and regex) or regex:
    process()
