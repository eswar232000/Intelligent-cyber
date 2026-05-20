import streamlit as st
from huggingface_hub import InferenceClient
from datetime import datetime

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Cybersecurity Incident Analyzer",
    page_icon="🛡️",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.stTextArea textarea {
    background-color: #1E1E1E;
    color: white;
    border-radius: 10px;
}

.severity-critical {
    color: red;
    font-weight: bold;
    font-size: 22px;
}

.severity-high {
    color: orange;
    font-weight: bold;
    font-size: 22px;
}

.severity-medium {
    color: yellow;
    font-weight: bold;
    font-size: 22px;
}

.severity-low {
    color: lightgreen;
    font-weight: bold;
    font-size: 22px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("⚙️ AI Configuration")

hf_token = st.sidebar.text_input(
    "Enter Hugging Face API Key",
    type="password"
)

model_name = st.sidebar.selectbox(
    "Select Model",
    [
        "meta-llama/Llama-3.1-8B-Instruct",
        "mistralai/Mistral-7B-Instruct-v0.3",
        "google/gemma-2-9b-it"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info("""
### Enterprise SOC Features

✅ Threat Intelligence  
✅ Incident Analysis  
✅ Severity Detection  
✅ Mitigation Strategy  
✅ SOC Report Generation  
""")

# ---------------------------------------------------
# SYSTEM PROMPT
# ---------------------------------------------------

SYSTEM_PROMPT = """
You are an elite Enterprise Cybersecurity Threat Intelligence Analyst.

PERSONA:
- Senior SOC Analyst
- Ethical Hacker
- Threat Intelligence Expert
- Incident Response Specialist

INSTRUCTION:
Analyze cybersecurity incidents using Chain-of-Thought reasoning.

CONTEXT:
Enterprise infrastructure includes:
- SIEM systems
- EDR tools
- Firewalls
- Hybrid cloud
- Zero Trust Architecture

TASKS:
1. Detect attack patterns
2. Analyze severity
3. Identify affected systems
4. Predict propagation risks
5. Generate mitigation strategy
6. Generate prevention recommendations
7. Generate SOC incident report

TONE:
Professional
Technical
Analytical
Action-oriented

OUTPUT FORMAT:
1. Threat Summary
2. Chain-of-Thought Analysis
3. Attack Pattern
4. Severity Level
5. Affected Systems
6. Indicators of Compromise
7. Threat Propagation Risk
8. Mitigation Strategy
9. Prevention Recommendations
10. Final SOC Report
"""

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🛡️ AI Cybersecurity Incident Analyzer")

st.markdown("""
### Enterprise Generative AI Threat Intelligence Platform

Analyze enterprise cybersecurity incidents using:
- Chain-of-Thought Prompting
- AI Threat Intelligence
- SOC Automation
- Generative AI Reasoning
""")

# ---------------------------------------------------
# INPUT AREA
# ---------------------------------------------------

incident_logs = st.text_area(
    "📄 Enter Cybersecurity Incident Logs",
    height=300,
    placeholder="""
Example:

Multiple failed login attempts detected.
PowerShell execution observed.
Ransomware encryption activity identified.
Suspicious outbound traffic detected.
Privilege escalation attempt found.
"""
)

# ---------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------

if st.button("🚀 Analyze Incident"):

    if not hf_token:
        st.error("Please enter Hugging Face API Key.")
    
    elif not incident_logs.strip():
        st.warning("Please enter incident logs.")
    
    else:

        try:

            client = InferenceClient(
                model=model_name,
                token=hf_token
            )

            final_prompt = f"""
            {SYSTEM_PROMPT}

            INCIDENT LOGS:
            {incident_logs}

            Begin enterprise cybersecurity analysis now.
            Use step-by-step reasoning.
            """

            with st.spinner("Analyzing cybersecurity threats..."):

                response = client.text_generation(
                    prompt=final_prompt,
                    max_new_tokens=1200,
                    temperature=0.3
                )

            st.success("Threat Analysis Completed Successfully")

            # ---------------------------------------------------
            # SEVERITY DETECTION
            # ---------------------------------------------------

            if "Critical" in response:
                st.markdown(
                    "<p class='severity-critical'>🔴 Severity: CRITICAL</p>",
                    unsafe_allow_html=True
                )

            elif "High" in response:
                st.markdown(
                    "<p class='severity-high'>🟠 Severity: HIGH</p>",
                    unsafe_allow_html=True
                )

            elif "Medium" in response:
                st.markdown(
                    "<p class='severity-medium'>🟡 Severity: MEDIUM</p>",
                    unsafe_allow_html=True
                )

            else:
                st.markdown(
                    "<p class='severity-low'>🟢 Severity: LOW</p>",
                    unsafe_allow_html=True
                )

            # ---------------------------------------------------
            # REPORT DISPLAY
            # ---------------------------------------------------

            st.markdown("---")

            with st.expander("📑 View Enterprise SOC Report", expanded=True):
                st.markdown(response)

            # ---------------------------------------------------
            # DOWNLOAD REPORT
            # ---------------------------------------------------

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            st.download_button(
                label="📥 Download SOC Report",
                data=response,
                file_name=f"soc_report_{timestamp}.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error: {str(e)}")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.markdown("""
### 🔐 Enterprise Security Platform

Built Using:
- Streamlit
- Hugging Face Inference API
- LLaMA 3.1 / Mistral / Gemma
- Prompt Engineering
- Chain-of-Thought AI Reasoning

Use Cases:
- SOC Monitoring
- Threat Intelligence
- Incident Response
- Enterprise Cybersecurity
""")
