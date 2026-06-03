import streamlit as st
import time

st.set_page_config(
    page_title="ResearchMind",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
/* Dark theme background */
.stApp {
    background-color: #0b0f19;
    color: #ffffff;
}

/* Hide Streamlit header */
header {visibility: hidden;}

/* Style the text input */
[data-testid="stTextInput"] input {
    background-color: #1a1e29 !important;
    color: #ffffff !important;
    border: 1px solid #2a2f3d !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #ff6b00 !important;
    box-shadow: 0 0 0 1px #ff6b00 !important;
}

/* Style the primary button */
button[kind="primary"] {
    background: linear-gradient(90deg, #ff8a00 0%, #ff4d00 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
    transition: transform 0.1s ease !important;
}
button[kind="primary"]:active {
    transform: scale(0.98) !important;
}

/* Style secondary buttons (Try chips) */
button[kind="secondary"] {
    background-color: #1a1e29 !important;
    color: #8c92a4 !important;
    border: 1px solid #2a2f3d !important;
    border-radius: 8px !important;
    margin-bottom: 4px !important;
    padding: 4px 12px !important;
    font-size: 0.85rem !important;
}
button[kind="secondary"]:hover {
    color: #ffffff !important;
    border-color: #ff6b00 !important;
}

/* Pipeline cards */
.pipeline-card {
    background-color: #121620;
    border: 1px solid #1f2433;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.3s ease;
}
.pipeline-card.active {
    border-color: #ff6b00;
    box-shadow: 0 0 15px rgba(255, 107, 0, 0.15);
}
.pipeline-card.done {
    border-color: #2e7d32;
}

.step-info {
    display: flex;
    flex-direction: column;
}
.step-header {
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-bottom: 4px;
}
.step-num {
    color: #ff6b00;
    font-weight: 700;
    font-size: 0.9rem;
}
.step-title {
    color: #ffffff;
    font-weight: 600;
    font-size: 1rem;
}
.step-desc {
    color: #8c92a4;
    font-size: 0.8rem;
}
.step-status {
    font-family: monospace;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    color: #5a6072;
    text-transform: uppercase;
}
.step-status.active {
    color: #ff6b00;
}
.step-status.done {
    color: #2e7d32;
}

/* Titles */
.main-title {
    font-size: 4.5rem;
    font-weight: 900;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
    font-family: 'Arial Black', sans-serif;
}
.main-title span {
    color: #ff6b00;
}
.sub-title {
    color: #8c92a4;
    font-size: 1.1rem;
    line-height: 1.5;
    margin-bottom: 3rem;
}
.tagline {
    color: #ff6b00;
    font-weight: 700;
    letter-spacing: 0.15em;
    font-size: 0.75rem;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* Footer */
.footer {
    text-align: center;
    color: #4a5060;
    font-size: 0.8rem;
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid #1f2433;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="tagline" style="text-align: center;">MULTI-AGENT AI SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title" style="text-align: center;">Research<span>Mind</span></div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title" style="text-align: center;">Four specialized AI agents collaborate — searching, scraping, writing, and<br>critiquing — to deliver a polished research report on any topic.</div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

col1, col_space, col2 = st.columns([1, 0.2, 1.2])

def set_topic(t):
    st.session_state.topic_input = t

if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""

with col1:
    st.markdown('<div style="color: #ff6b00; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em; margin-bottom: -10px; text-transform: uppercase;">RESEARCH TOPIC</div>', unsafe_allow_html=True)
    
    topic = st.text_input(
        "RESEARCH TOPIC", 
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
        key="topic_input"
    )
    
    run_btn = st.button("⚡ Run Research Pipeline", type="primary", use_container_width=True)
    
    st.markdown('<div style="color: #5a6072; font-size: 0.75rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem;">TRY →</div>', unsafe_allow_html=True)
    
    st.button("LLM agents 2025", on_click=set_topic, args=("LLM agents 2025",))
    st.button("CRISPR gene editing", on_click=set_topic, args=("CRISPR gene editing",))
    st.button("Fusion energy progress", on_click=set_topic, args=("Fusion energy progress",))

with col2:
    st.markdown('<h3 style="color: white; margin-bottom: 1rem; font-family: sans-serif; font-size: 1.2rem;">Pipeline</h3>', unsafe_allow_html=True)
    
    STEPS = [
        ("01", "Search Agent", "Gathers recent web information"),
        ("02", "Reader Agent", "Scrapes & extracts deep content"),
        ("03", "Writer Chain", "Drafts the full research report"),
        ("04", "Critic Chain", "Reviews & scores the report"),
    ]
    
    def render_steps(active=-1, done_up_to=-1):
        html = ""
        for i, (num, title, desc) in enumerate(STEPS):
            if i < done_up_to:
                status, cls, status_cls = "DONE", "done", "done"
            elif i == active:
                status, cls, status_cls = "RUNNING", "active", "active"
            else:
                status, cls, status_cls = "WAITING", "", ""
                
            html += f"""
            <div class="pipeline-card {cls}">
                <div class="step-info">
                    <div class="step-header">
                        <span class="step-num">{num}</span>
                        <span class="step-title">{title}</span>
                    </div>
                    <span class="step-desc">{desc}</span>
                </div>
                <div class="step-status {status_cls}">{status}</div>
            </div>
            """
        return html
        
    steps_placeholder = st.empty()
    steps_placeholder.markdown(render_steps(), unsafe_allow_html=True)

# ── Pipeline Execution ─────────────────────────────────────────────────────────

if run_btn:
    if not topic.strip():
        st.error("Please enter a research topic before running.")
    else:
        state = {}
        error_occurred = False
        
        try:
            # Step 1
            steps_placeholder.markdown(render_steps(active=0, done_up_to=0), unsafe_allow_html=True)
            from agents import build_search_agent
            search_agent = build_search_agent()
            search_result = search_agent.invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]})
            state["search_results"] = search_result['messages'][-1].content
            
            # Step 2
            steps_placeholder.markdown(render_steps(active=1, done_up_to=1), unsafe_allow_html=True)
            from agents import build_scrape_agent
            scrape_agent = build_scrape_agent()
            reader_result = scrape_agent.invoke({
                "messages": [(
                    "user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}"
                )]
            })
            state["scraped_content"] = reader_result["messages"][-1].content
            
            # Step 3
            steps_placeholder.markdown(render_steps(active=2, done_up_to=2), unsafe_allow_html=True)
            from agents import writer_chain
            research_combined = (
                f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined
            })
            
            # Step 4
            steps_placeholder.markdown(render_steps(active=3, done_up_to=3), unsafe_allow_html=True)
            from agents import critic_chain
            state["feedback"] = critic_chain.invoke({
                "report": state["report"]
            })
            
            # Done
            steps_placeholder.markdown(render_steps(active=-1, done_up_to=4), unsafe_allow_html=True)
            
        except Exception as e:
            error_occurred = True
            st.error(f"Pipeline failed: {e}")

        # Render Results
        if not error_occurred and state:
            st.markdown("<hr style='border-color: #1f2433;'>", unsafe_allow_html=True)
            
            st.markdown(f"<h2 style='color: white; margin-bottom: 2rem;'>Results for: <span style='color: #ff6b00;'>{topic}</span></h2>", unsafe_allow_html=True)
            
            with st.expander("🔍 Web Search Findings"):
                st.write(state.get('search_results','—'))
                
            with st.expander("📄 Extracted Content"):
                st.write(state.get('scraped_content','—'))
                
            st.markdown("### 📋 Final Research Report")
            st.info(state.get('report','—'))
            
            st.markdown("### 🎯 Critic Feedback")
            st.warning(state.get('feedback','—'))
            
st.markdown('<div class="footer">ResearchMind • Powered by LangChain multi-agent pipeline • Built with Streamlit</div>', unsafe_allow_html=True)