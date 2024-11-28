import streamlit as st
import ollama

# Initialize session state for progress tracking and clearing prompts
if "progress" not in st.session_state:
    st.session_state.progress = {
        "Basics": "Not Started",
        "Data Structures": "Not Started",
        "Object-Oriented Programming": "Not Started",
        "Advanced Topics": "Not Started",
        "Libraries": "Not Started"
    }

if "explanation" not in st.session_state:
    st.session_state.explanation = ""

if "answer" not in st.session_state:
    st.session_state.answer = ""

# App Title
st.title("Learn Python with AI - PyLearn Pro")

# Sidebar for Main Topics and Subtopics
st.sidebar.title("Python Topics")
topics = {
    "Basics": ["Variables", "Data Types",
                "Loops", "File Handling", "Regex",
               "Input/Output", "Control Flow"],
    "Data Structures": ["Lists", "Tuples", "Dictionaries", "Sets"],
    "Object-Oriented Programming": ["Classes", "Inheritance", "Polymorphism"],
    "Advanced Topics": ["Generators", "Decorators", "Context Managers"],
    "Libraries": ["NumPy", "Pandas", "Matplotlib"]
}

selected_topic = st.sidebar.selectbox("Select a Topic", list(topics.keys()))
subtopics = topics[selected_topic]
selected_subtopic = st.sidebar.radio(f"{selected_topic} Subtopics", subtopics)

# Display Topic Explanation
st.header(f"{selected_topic} - {selected_subtopic}")

# Ollama AI Explanation
if st.button(f"Explain {selected_subtopic}"):
    with st.spinner("Fetching explanation..."):
        prompt = f"Explain {selected_subtopic} in Python with examples."
        response = ollama.generate(model="llama3.2", prompt=prompt, stream=True)

        # Stream response for faster display
        explanation_placeholder = st.empty()
        explanation = ""
        for part in response:
            explanation += part['response']
            if "```" in explanation:  # Check if the response contains code snippets
                explanation_placeholder.code(explanation, language="python")
            else:
                explanation_placeholder.text(explanation)

# Clear Explanation
if st.button("Clear Explanation"):
    st.session_state.explanation = ""
    st.write("")  # Clear placeholder

# AI-Powered Mentor Section
st.subheader("Ask Python Questions")
user_query = st.text_input("Type your Python-related question here:")

if st.button("Get Answer"):
    if user_query:
        with st.spinner("Thinking..."):
            prompt = user_query
            response = ollama.generate(model="llama3.2", prompt=prompt, stream=True)

            # Stream response for faster display
            answer_placeholder = st.empty()
            answer = ""
            for part in response:
                answer += part['response']
                if "```" in answer:  # Check if the response contains code snippets
                    answer_placeholder.code(answer, language="python")
                else:
                    answer_placeholder.text(answer)
    else:
        st.warning("Please enter a question.")

# Clear Q&A
if st.button("Clear Answer"):
    st.session_state.answer = ""
    st.write("")  # Clear placeholder

# Interactive Progress Tracker
st.sidebar.subheader("Progress Tracker")
for topic, status in st.session_state.progress.items():
    col1, col2 = st.sidebar.columns([2, 1])
    with col1:
        st.write(f"{topic}: {status}")
    with col2:
        if st.sidebar.button(f"Update {topic}", key=f"{topic}_button"):
            st.session_state.progress[topic] = "In Progress" if status == "Not Started" else "Completed"

st.sidebar.markdown("---")
if st.sidebar.button("Reset Progress"):
    for key in st.session_state.progress:
        st.session_state.progress[key] = "Not Started"
              
# About Section
st.write("### About PyLearn Pro")
st.markdown("""
**PyLearn Pro** is an interactive platform for learning Python, enriched with AI-driven explanations.
Explore topics, ask questions, and track your progress—all in one place!
""")
