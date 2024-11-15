import gradio as gr
import pandas as pd
from course_search import CourseSearchSystem

# Initialize the search system
df = pd.read_csv('updated_Analytics_vidhya.csv')
search_system = CourseSearchSystem()
search_system.load_and_prepare_data(df)

def search_courses(query: str, skill_level: str, min_rating: float) -> str:
    """Search function for Gradio interface with skill level and rating filters."""
    if not query.strip():
        return "Please enter a search query to find relevant courses!"
    
    results = search_system.search_courses(query)
    
    # Filter results based on skill level and minimum rating
    filtered_results = [
        course for course in results 
        if (course['difficulty'] == skill_level or skill_level == "No preference") and course['ratings'] >= min_rating
    ]
    
    return search_system.generate_response(query, filtered_results)

# Custom CSS for improved UI and aesthetics
custom_css = """
.gradio-container {
    font-family: 'Arial', sans-serif;
    background: linear-gradient(to bottom, #f0f2f5, #ffffff);
    padding: 2rem !important;
}
.title {
    text-align: center;
    font-size: 2em;
    color: #333;
    margin-bottom: 1rem;
}
.search-container {
    display: flex;
    gap: 1rem;
}
.results-container {
    margin-top: 1.5rem;
    padding: 1rem;
    background: #fafafa;
    border: 1px solid #ddd;
    border-radius: 8px;
}
.result-card {
    background: #fff;
    padding: 1.2rem;
    margin-bottom: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
button {
    transition: background 0.3s ease;
}
button:hover {
    background: #007bff !important;
    color: white !important;
}
"""

# Gradio UI with skill level and rating filters
with gr.Blocks(css=custom_css) as iface:
    gr.Markdown(
        """
        <div class="title">
            <h1>Analytics Vidhya Course Finder</h1>
            <p>Search and filter for the best free courses curated just for you!</p>
        </div>
        """,
        elem_id="title"
    )
    
    with gr.Row(elem_id="search-container"):
        query_input = gr.Textbox(
            label="Search Courses",
            placeholder="E.g., 'Deep Learning projects', 'Python for data analysis'"
        )
        
        skill_level = gr.Radio(
            choices=["Beginner", "Intermediate", "Advanced", "No preference"],
            label="Skill Level",
            value="Beginner"
        )
        
        min_rating = gr.Slider(
            minimum=1.0,
            maximum=5.0,
            value=3.0,
            step=0.1,
            label="Minimum Rating (1.0 - 5.0)",
            interactive=True
        )
        
        search_button = gr.Button("🔍 Find Courses", variant="primary")
    
    # Results section in card format
    output = gr.Markdown(label="Results", elem_classes="results-container")
    
    # Set up the click event
    search_button.click(
        fn=search_courses,
        inputs=[query_input, skill_level, min_rating],
        outputs=output
    )

if __name__ == "__main__":
    iface.launch(share=False, debug=False)