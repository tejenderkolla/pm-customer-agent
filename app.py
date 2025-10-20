import streamlit as st
import pandas as pd
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# --- Page Configuration ---
st.set_page_config(page_title="Voice of the Customer AI Agent", layout="wide")
st.title("🤖 Voice of the Customer (VoC) Synthesis Agent")
st.markdown("Upload your customer feedback CSV, and the AI crew will analyze it for you.")

# --- API Key Setup ---
# Load the API key from Streamlit's secrets
try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4o")
except KeyError:
    st.error("OPENAI_API_KEY not found. Please add it to your Streamlit secrets.", icon="🚨")
    st.stop()

# --- Agent Definitions ---
# Agent 1: The Triage Specialist
triage_agent = Agent(
    role='Customer Feedback Triage Specialist',
    goal='Accurately classify each piece of customer feedback into one of three categories: "Bug Report", "Feature Request", or "General Feedback".',
    backstory=(
        "You are an expert in customer support operations. Your primary skill is to read "
        "a customer's comment and instantly understand its core intent. You are meticulous "
        "and ensure every item is correctly categorized for the right team."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Agent 2: The Root Cause Analyst (for Bugs)
bug_analyst_agent = Agent(
    role='Bug Report Root Cause Analyst',
    goal='Analyze all classified "Bug Reports" and identify the top 3-5 recurring root causes. Do not list individual bugs, but the *themes* of the bugs.',
    backstory=(
        "You are a senior QA engineer and product analyst. You have a keen eye for patterns. "
        "You don't just see 'the app crashed'; you see 'a pattern of crashes on the payment screen for iOS users'. "
        "You group similar bug reports to find the underlying problem."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Agent 3: The Feature Synthesizer (for Features)
feature_analyst_agent = Agent(
    role='Feature Request Synthesizer',
    goal='Analyze all classified "Feature Requests" and identify the top 3-5 most requested features or themes. Group similar requests into broader categories.',
    backstory=(
        "You are a savvy Product Manager who is an expert at synthesizing user needs. "
        "You can read 50 different requests for 'dark mode', 'night mode', and 'black screen' "
        "and correctly synthesize them into a single, high-priority request: 'User Demand for Dark Mode'."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Agent 4: The PM Report Writer
report_agent = Agent(
    role='Senior Product Manager',
    goal='Create a concise, actionable, management-ready report based on the analyses from the bug and feature agents. The report must be in markdown format.',
    backstory=(
        "You are a Senior PM responsible for presenting the 'Voice of the Customer' to leadership. "
        "Your reports are clear, data-driven, and actionable. You skip the fluff and get straight "
        "to the insights that matter for building a better product."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)


# --- Streamlit UI ---
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        
        # --- IMPORTANT: Column Name ---
        # Ask user to specify the column with review text
        review_column = st.selectbox(
            "Which column contains the customer review text?",
            df.columns
        )
        
        if st.button("Analyze Feedback", type="primary"):
            with st.spinner("AI Crew is analyzing... This may take a few minutes... 🕵️‍♂️"):
                # Convert the relevant column to a single string for the agents
                # We use a sample to keep costs/time down, you can use the full list
                sample_size = min(len(df), 200) # Limit to 200 reviews for this demo
                feedback_list = df[review_column].dropna().sample(sample_size).tolist()
                feedback_data_string = "\n".join(feedback_list)

                # --- Task Definitions ---
                triage_task = Task(
                    description=f"Classify each feedback item in the following list. Output ONLY the classified lists, with no other text.\n\nDATA:\n{feedback_data_string}",
                    expected_output='Three distinct lists: one for "Bug Reports", one for "Feature Requests", and one for "General Feedback".',
                    agent=triage_agent
                )
                
                bug_analysis_task = Task(
                    description='Analyze the list of "Bug Reports" provided by the Triage Specialist. Identify and list the top 3-5 recurring bug themes.',
                    expected_output='A bulleted list of the top 3-5 bug themes and a brief explanation for each.',
                    agent=bug_analyst_agent,
                    context=[triage_task] # This task depends on the triage task
                )

                feature_analysis_task = Task(
                    description='Analyze the list of "Feature Requests" provided by the Triage Specialist. Identify and list the top 3-5 most requested feature themes.',
                    expected_output='A bulleted list of the top 3-5 feature request themes and a brief explanation for each.',
                    agent=feature_analyst_agent,
                    context=[triage_task] # This task also depends on the triage task
                )
                
                report_task = Task(
                    description=(
                        "Create a final, management-ready report. The report must be in markdown. "
                        "It must include: \n"
                        "1. A brief executive summary. \n"
                        f"2. The 'Top Bug Themes' from the Bug Analyst's report. \n"
                        f"3. The 'Top Feature Requests' from the Feature Analyst's report. \n"
                        "Do not include the General Feedback list."
                    ),
                    expected_output='A concise, well-formatted markdown report with a summary, top bug themes, and top feature requests.',
                    agent=report_agent,
                    context=[bug_analysis_task, feature_analysis_task] # Depends on both analysis tasks
                )

                # --- Crew Definition ---
                product_crew = Crew(
                    agents=[triage_agent, bug_analyst_agent, feature_analyst_agent, report_agent],
                    tasks=[triage_task, bug_analysis_task, feature_analysis_task, report_task],
                    process=Process.sequential, # Tasks will run one after another
                    verbose=2
                )

                # --- Run the Crew ---
                final_report = product_crew.kickoff()

                # --- Display the Final Report ---
                st.subheader("Analysis Complete! ✅")
                st.markdown(final_report)

    except Exception as e:
        st.error(f"An error occurred: {e}", icon="🚨")