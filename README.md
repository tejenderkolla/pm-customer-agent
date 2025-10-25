# Voice of the Customer (VoC) Synthesis Agent 🤖

An AI-powered agentic system to analyze and synthesize thousands of customer reviews into actionable product insights.

## 🚀 Live Demo.  
Link:- https://pm-customer-agent.onrender.com/

**Try the live application here:**  

---

## 🎯 The Business Problem

As a Product Manager, your most important job is to be the voice of the customer. However, product and marketing teams are often inundated with thousands of qualitative feedback entries from app stores, user surveys, and support tickets.

Manually reading, triaging, and synthesizing this data is a slow, expensive, and often biased process. It's incredibly difficult to get a clear, data-driven "signal" from all the "noise."

## 💡 The Solution

This project is an autonomous "crew" of AI agents that acts as a junior product analyst. A user can upload a CSV file containing thousands of customer reviews, and the agentic system will automatically:

1.  **Triage** every single review into distinct, actionable categories (e.g., "Bug Report," "Feature Request," "General Feedback").
2.  **Analyze** the "Bug Reports" to find the top 3-5 recurring root cause *themes*.
3.  **Synthesize** the "Feature Requests" to identify the top 3-5 most in-demand features.
4.  **Generate** a concise, management-ready report with the actionable insights a PM needs to update their product backlog.

---

## 🧠 Design Rationale: Why an Agentic Workflow?

A common question is, "Couldn't this be done with a simple script that just makes one big API call to an LLM?"

While a simple script could find basic keywords, I chose a more sophisticated **agentic architecture (using CrewAI)** for three key strategic reasons. This system isn't just a *tool*; it's an *autonomous process*.

### 1. Specialization and Quality
Instead of one "mega-prompt," this project uses a crew of four specialists with distinct roles, backstories, and goals:

* **`Triage_Specialist`**: An expert in customer support who only classifies feedback.
* **`Bug_Analyst_Agent`**: A "QA Engineer" persona who is an expert at finding root cause patterns.
* **`Feature_Analyst_Agent`**: A "Product Manager" persona skilled at grouping user needs into broader feature themes.
* **`Report_Agent`**: A "Senior Product Manager" who writes the final executive summary.

This separation of concerns results in a far higher quality and more nuanced analysis, as each agent is hyper-focused on one task.

### 2. Autonomous Collaboration
The agents work like a real-world assembly line. The `Bug_Analyst_Agent` doesn't see all the data; it *only* receives the classified "Bug Reports" from the `Triage_Specialist`. The final `Report_Agent` receives the already-synthesized lists from the two analyst agents.

This autonomous delegation and passing of context from one agent to the next is what allows the crew to handle a complex, multi-step reasoning task from end to end without human intervention.

### 3. Scalability and Maintenance
This system is modular. If tomorrow we wanted to add a new step—like an **`Urgency_Detection_Agent`** to flag safety-related complaints—we could simply add that agent to the "crew" without rewriting the entire logic. This makes the system far more scalable and easier to maintain than a single, monolithic script.

---

## 🛠️ Tech Stack

* **Framework:** CrewAI
* **Language:** Python
* **LLM:** OpenAI GPT-4o
* **UI & Hosting:** Streamlit & Streamlit Community Cloud
* **Data Handling:** Pandas

---

## 🔧 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/tejenderkolla/pm-customer-agent.git
    cd pm-customer-agent
    ```

2.  **Create and activate a virtual environment (using Python 3.11):**
    ```bash
    # We use Python 3.11 for maximum compatibility with data/AI libraries
    python3.11 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API key:**
    Create a file at `.streamlit/secrets.toml` and add your OpenAI key:
    ```toml
    OPENAI_API_KEY = "sk-YOUR_API_KEY_HERE"
    ```

5.  **Run the app:**
    ```bash
    streamlit run app.py
    ```