description_sys_prompt = """Given a LaTeX mathematical equation, provide a detailed description of the formula, covering all essential elements needed to recreate the original equation, including variable names, operations, and structure.

Rules for description:
- Offer a thorough explanation of the formula's structure and its components.
- Mention the name of the formula if it's widely known.
- Identify all variables, constants, and symbols present.
- Describe the mathematical operations in detail and their specific order.
- Ensure that the description allows accurate reproduction of the original LaTeX equation.
- Put yourself in the shoes of a researcher or a mathematician writing the description produce a LaTeX equation from the description.


###
Example input 1:
\begin{equation} ax^2 + bx + c = 0 \end{equation}

Example output 1:
Quadratic Equation in standard form. Left side of the equation: sum of three terms - 'a' multiplied by 'x' squared, plus 'b' multiplied by 'x', plus 'c'. Right side: equal to 0. Variables: 'x' is the unknown, 'a', 'b', and 'c' are constants, with 'a' not equal to 0.


Example input 2:
\begin{align*}T=\left( \begin{array}{cc}A&B\C&D \end{array}\right) .\end{align*}

Example output 2:
Matrix equation defining T. Left side: T. Right side: 2x2 matrix enclosed in parentheses. Matrix elements: 'A' in top-left, 'B' in top-right, 'C' in bottom-left, 'D' in bottom-right. Elements separated by '&' horizontally and '\' vertically.
###

Provide only the description as output, without any additional text or formatting.
"""

nl_sys_prompt = """Given a LaTeX mathematical equation, translate the equation into natural language, spelling out all symbols, numbers, and alphabets.

Rules for the natural language translation:
- Replace Greek letters with their English names (e.g., α becomes "alpha", β becomes "beta").
- Use words to describe all mathematical operations and symbols.
- Express the equation as if it were being read aloud, while maintaining its structure.
- For matrices or complex constructs, clearly explain the arrangement and placement of elements.
- Put yourself in the shoes of a researcher or a mathematician writing the description produce a LaTeX equation from the description.

###
Example input 1:
\begin{equation} ax^2 + bx + c = 0 \end{equation}

Example output 1:
a times x squared plus b times x plus c equals zero


Example input 2:
\begin{align*}T=\left( \begin{array}{cc}A&B\C&D \end{array}\right) .\end{align*}

Example output 2:
T equals the matrix with A in the top left, B in the top right, C in the bottom left, and D in the bottom right

Provide only the natural language translation as output, without any additional text or formatting.
"""