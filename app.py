# Import necessary libraries
import streamlit as st
import os
from together import Together

# Set up API key
os.environ['TOGETHER_API_KEY'] = st.secrets.get("TOGETHER_API_KEY", "")

# Initialize Together client
client = Together()

# Function to generate Python code using CodeLlama
def generate_code_with_codellama(description):
    """
    Generate Python code based on a natural language description using CodeLlama.

    Parameters:
    description (str): A plain-text description of the desired Python code.

    Returns:
    str: Generated Python code or an error message.
    """
    try:
        prompt = (
            f"You are a Python programming assistant. Based on the following description, "
            f"generate the Python code. Ensure the code is clear, well-commented, and includes necessary imports.\n\n"
            f"Description: {description}\n\n"
            f"Generated Python Code:"
        )

        # Call Together AI
        response = client.chat.completions.create(
            model="codellama/CodeLlama-34b-Instruct-hf",  # CodeLlama model
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract the generated code
        generated_code = response.choices[0].message.content.strip()
        return generated_code

    except Exception as e:
        return f"Error with CodeLlama: {e}"

# Streamlit app layout
st.title("Python Code Generator with CodeLlama")
st.write("Enter a description of the Python application or code you need. CodeLlama will generate the corresponding Python code.")

# Initialize session state for inputs and outputs
if "generated_code" not in st.session_state:
    st.session_state["generated_code"] = ""

# Input box for the user to enter a description
description = st.text_area(
    "Application or Code Description",
    placeholder="Describe the application or code you want",
    key="description"
)

# Button to trigger code generation
if st.button("Generate Code"):
    if st.session_state["description"].strip():  # Use session_state directly
        with st.spinner("Generating Python code..."):
            # Generate code
            generated_code = generate_code_with_codellama(st.session_state["description"])
            if generated_code and "Error" not in generated_code:
                st.session_state["generated_code"] = generated_code  # Store in session state
                st.session_state["description"] = ""  # Clear the input field
                st.write("### Generated Python Code")
                st.code(generated_code, language="python")
            else:
                st.error("The model did not return any usable code. Try refining your description.")
    else:
        st.error("Please provide a valid description.")

# Display previously generated code
if st.session_state["generated_code"]:
    st.write("### Previously Generated Code")
    st.code(st.session_state["generated_code"], language="python")

# Button to edit the generated code
if st.session_state["generated_code"]:
    with st.expander("Edit Generated Code"):
        edited_code = st.text_area(
            "Edit Code",
            st.session_state["generated_code"],
            height=300
        )
        if st.button("Save Changes"):
            st.session_state["generated_code"] = edited_code  # Save edits
            st.success("Changes saved successfully!")

# Add an option to copy the code
if st.session_state["generated_code"]:
    st.download_button(
        "Download Generated Code",
        st.session_state["generated_code"],
        file_name="generated_code.py"
    )

# Tips for effective descriptions
with st.expander("Tips for Writing Effective Descriptions"):
    st.write("""
    - Be clear and concise about the functionality.
    - Mention any specific libraries or frameworks you want to include.
    - Include edge cases or examples if applicable.
    - Specify input/output formats or constraints.
    """)

# Check API key validity
if not os.environ['TOGETHER_API_KEY']:
    st.error("API key not found! Please ensure it is set in Streamlit secrets.")
