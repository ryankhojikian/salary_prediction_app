import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="AI Salary Storyteller", layout="wide", page_icon="📖")

# Custom CSS for storytelling theme
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #A23B72;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
    }
    .story-section {
        background-color: #F8F9FA;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #2E86AB;
    }
    .prediction-reveal {
        background-color: #E8F4FD;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        animation: fadeIn 2s;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">📖 Your Salary Story Awaits</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Embark on a journey to discover how your career choices shape your financial destiny. Each decision weaves into your unique salary narrative.</p>', unsafe_allow_html=True)

st.markdown("---")

# Sidebar for additional context
with st.sidebar:
    st.header("💡 Career Insights")
    st.write("**Experience Levels:**")
    st.write("- Entry: Building foundations")
    st.write("- Mid: Gaining momentum")
    st.write("- Senior: Leading the way")
    st.write("- Executive: Visionary leadership")
    
    st.write("**Company Sizes:**")
    st.write("- Small: Intimate, agile environments")
    st.write("- Medium: Balanced growth opportunities")
    st.write("- Large: Scale and stability")

experience_codes = {
    "Entry": "EN",
    "Mid": "MI", 
    "Senior": "SE",
    "Executive": "EX"
}
employment_codes = {
    "Full-time": "FT",
    "Part-time": "PT",
    "Contract": "CT",
    "Freelance": "FL"
}
company_codes = {
    "Small": "S",
    "Medium": "M",
    "Large": "L"
}

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="story-section">', unsafe_allow_html=True)
    st.subheader("🌟 Chapter 1: Define Your Character")
    job_title = st.text_input("What is your job title?", placeholder="e.g. Data Scientist", help="Enter the role that defines your professional identity")
    
    col_a, col_b = st.columns(2)
    with col_a:
        experience_level = st.selectbox("Experience Level", options=list(experience_codes.keys()), help="Your journey stage in the career path")
        employment_type = st.selectbox("Employment Type", options=list(employment_codes.keys()), help="How you engage with your work")
    with col_b:
        company_size = st.selectbox("Company Size", options=list(company_codes.keys()), help="The scale of your professional arena")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="story-section">', unsafe_allow_html=True)
    st.subheader("🎭 Why These Choices Matter")
    st.write(
        "Every career is a story of growth, challenges, and triumphs. "
        "Your experience level represents chapters of learning, "
        "your employment type defines your commitment style, "
        "and company size sets the stage for your professional drama."
    )
    st.info("💭 *Think of this as crafting your character in an epic tale.*")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

if st.button("✨ Weave My Salary Story", type="primary", use_container_width=True):
    if job_title:
        payload = {
            "job_title": job_title,
            "experience_level": experience_codes[experience_level],
            "employment_type": employment_codes[employment_type],
            "company_size": company_codes[company_size]
        }

        # Interactive loading sequence
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            progress_bar.progress(i + 1)
            if i < 30:
                status_text.text("Analyzing your career path...")
            elif i < 60:
                status_text.text("Consulting the salary oracle...")
            elif i < 90:
                status_text.text("Crafting your personal narrative...")
            else:
                status_text.text("Finalizing your story...")
            time.sleep(0.02)
        
        progress_bar.empty()
        status_text.empty()

        try:
            with st.spinner("Sending your story to the oracle..."):
                response = requests.post("http://127.0.0.1:8001/predict", json=payload)

            if response.status_code == 200:
                data = response.json()
                predicted_salary = data["predicted_salary_usd"]
                story = data.get("story", "Your salary story is one of potential and growth.")

                # Final reveal loading
                reveal_status = st.empty()
                reveal_status.text("Revealing your story...")

                # Typewriter success message
                typewriter_placeholder = st.empty()
                message = "🎉 Success! Your salary story has been revealed!"
                for i in range(len(message) + 1):
                    typewriter_placeholder.markdown(f"<h3 style='color: #2E86AB; font-family: monospace;'>{message[:i]}</h3>", unsafe_allow_html=True)
                    time.sleep(0.05)
                time.sleep(1)
                typewriter_placeholder.empty()
                reveal_status.empty()

                st.markdown('<div class="prediction-reveal">', unsafe_allow_html=True)
                st.subheader("🎉 Your Salary Revelation")
                st.metric("Predicted Annual Salary", f"${predicted_salary:,.0f}", delta="USD")
                st.markdown('</div>', unsafe_allow_html=True)

                # Expandable story section
                with st.expander("📚 Read Your Full Career Story", expanded=True):
                    st.write(story)

                st.markdown('<div class="story-section">', unsafe_allow_html=True)
                st.subheader("📊 Your Place in the Salary Landscape")
                st.write("See how your prediction compares to industry benchmarks:")
                
                chart_df = pd.DataFrame(
                    {
                        "Role": ["Your Story", "Entry Benchmark", "Executive Benchmark"],
                        "Salary": [predicted_salary, 65000, 180000],
                    }
                )
                st.bar_chart(chart_df, use_container_width=True)
                
                # Additional insights
                if predicted_salary < 70000:
                    st.info("🌱 This is a foundation-building chapter. Focus on skills and experience to advance your plot.")
                elif predicted_salary < 120000:
                    st.success("🚀 You're in a growth arc! Consider leadership opportunities to elevate your story.")
                else:
                    st.warning("🏆 Executive level achieved! Your expertise commands premium compensation.")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                st.write("**💡 Pro Tip:** Use this insight as a guidepost for your career journey. Negotiate boldly, learn continuously, and write your own success story!")
                
            else:
                st.error("The story couldn't be told right now. Is the backend server running?")
        except Exception as e:
            st.error(f"The connection to your story failed: {e}")
    else:
        st.warning("Every great story needs a protagonist. Please enter your job title to begin.")
