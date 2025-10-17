# Regex to NFA

## Project Components

- Parser
- NFA Constructor
- NFA Visualizer

## Parsing

**Goal**: Convert an input string regex into a structured blueprint for representation.
**Input**: A valid string regex.
**Output**: Abstract syntax tree.

### Process

1. Validate the input string.
2. Tokenize the string.
3. Add explicit operators.
4. Apply precedence.
5. Convert to AST.

## Constructing

**Goal**: Convert the blueprint into an actual NFA.
**Input**: AST.
**Output**: Data representing NFA (Formal definition).

### Process

- Handle operations using Thompson's Construction Algorithm.

## Visualization

**Goal**: Visualize the NFA
**Input**: NFA representation.
**Output**: NFA graph.
