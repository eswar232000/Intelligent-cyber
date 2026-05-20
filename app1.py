import os
import requests
import streamlit as st
from datetime import datetime

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Cybersecurity Incident Analyzer",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

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
    border: 1px solid #333;
}

.severity-critical {
    color: red;
    font-size: 24px;
    font-weight: bold;
}

.severity-high {
    color: orange;
    font-size: 24px;
    font-weight: bold;
}

.severity-medium {
    color: yellow;
    font-size: 24px;
    font-weight: bold;
}

.severity-low {
    color: lightgreen;
    font-size: 24px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# GET HUGGING FACE TOKEN FROM SECRETS
# =====================================================

HF_TOKEN = os.getenv("HF_TOKEN")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("⚙️ AI Configuration")

model_name = st.sidebar.selectbox(
    "Select AI Model",
    [
        "mistralai/Mistral-7B-Instruct-v0.3",
        "google/gemma-2-9b-it"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info("""
### Enterprise SOC Features

✅ Threat Detection  
✅ Severity Analysis  
✅ Attack Pattern Detection  
✅ Mitigation Strategy  
✅ SOC Report Generation  
""")

# =====================================================
# HEADER
# =====================================================

st.title("🛡️ AI Cybersecurity Incident Analyzer")

st.markdown("""
### Enterprise Generative AI Security Platform

Analyze cybersecurity incidents using:
- Chain-of-Thought Prompting
- AI Threat Intelligence
- SOC Automation
- Enterprise Security AI
""")

# =====================================================
# SYSTEM PROMPT
# =====================================================

SYSTEM_PROMPT = """
You are an Enterprise Cybersecurity Threat Intelligence Analyst.

PERSONA:
- Senior SOC Analyst
- Ethical Hacker
- Incident Response Specialist
- Threat Intelligence Expert

INSTRUCTION:
Analyze cybersecurity incidents using Chain-of-Thought reasoning.

TASKS:
1. Threat Summary
2. Chain-of-Thought Analysis
3. Attack Pattern Detection
4. Severity Analysis
5. Affected Systems
6. Indicators of Compromise
7. Threat Propagation Risk
8. Mitigation Strategy
9. Prevention Recommendations
10. Final SOC Report

CONTEXT:
Enterprise environment includes:
- SIEM systems
- EDR platforms
- Firewalls
- Hybrid cloud infrastructure
- Zero Trust Architecture

TONE:
Professional
Technical
Analytical
Action-oriented
"""

# =====================================================
# INPUT AREA
# =====================================================

incident_logs = st.text_area(
    "📄 Enter Cybersecurity Incident Logs",
    height=300,
    placeholder="""
Example:

Suspicious outbound traffic detected.
Multiple failed login attempts observed.
PowerShell execution identified.
Possible ransomware activity detected.
Privilege escalation attempt found.
"""
)

# =====================================================
# ANALYZE BUTTON
# =====================================================

if st.button("🚀 Analyze Incident"):

    if not HF_TOKEN:
        st.error("HF_TOKEN not found in environment variables.")

    elif not incident_logs.strip():
        st.warning("Please enter cybersecurity incident logs.")

    else:

        try:

            API_URL = f"https://api-inference.huggingface.co/models/{model_name}"

            headers = {
                "Authorization": f"Bearer {HF_TOKEN}"
            }

            final_prompt = f"""
            {SYSTEM_PROMPT}

            INCIDENT LOGS:
            {incident_logs}

            Generate enterprise cybersecurity analysis.
            Use detailed step-by-step reasoning.
            """

            payload = {
                "inputs": final_prompt,
                "parameters": {
                    "max_new_tokens": 1000,
                    "temperature": 0.3
                }
            }

            with st.spinner("Analyzing Cybersecurity Threats..."):

                response = requests.post(
                    API_URL,
                    headers=headers,
                    json=payload,
                    timeout=120
                )

            # =====================================================
            # HANDLE EMPTY RESPONSE
            # =====================================================

            if response.text.strip() == "":
                st.error("Empty response from Hugging Face API.")
                st.stop()

            # =====================================================
            # SAFE JSON PARSING
            # =====================================================

            try:
                result = response.json()
            except Exception:
                st.error("Invalid JSON response.")
                st.text(response.text)
                st.stop()

            # =====================================================
            # HANDLE API ERRORS
            # =====================================================

            if isinstance(result, dict) and "error" in result:
                st.error(result["error"])
                st.stop()

            # =====================================================
            # EXTRACT GENERATED TEXT
            # =====================================================

            if isinstance(result, list):

                if "generated_text" in result[0]:
                    generated_text = result[0]["generated_text"]
                else:
                    generated_text = str(result)

            else:
                generated_text = str(result)

            st.success("Threat Analysis Completed Successfully")

            # =====================================================
            # SEVERITY DISPLAY
            # =====================================================

            if "Critical" in generated_text:
                st.markdown(
                    "<p class='severity-critical'>🔴 Severity: CRITICAL</p>",
                    unsafe_allow_html=True
                )

            elif "High" in generated_text:
                st.markdown(
                    "<p class='severity-high'>🟠 Severity: HIGH</p>",
                    unsafe_allow_html=True
                )

            elif "Medium" in generated_text:
                st.markdown(
                    "<p class='severity-medium'>🟡 Severity: MEDIUM</p>",
                    unsafe_allow_html=True
                )

            else:
                st.markdown(
                    "<p class='severity-low'>🟢 Severity: LOW</p>",
                    unsafe_allow_html=True
                )

            # =====================================================
            # REPORT SECTION
            # =====================================================

            st.markdown("---")

            st.subheader("📊 Enterprise Threat Intelligence Report")

            with st.expander("📑 View Full SOC Report", expanded=True):
                st.write(generated_text)

            # =====================================================
            # DOWNLOAD REPORT
            # =====================================================

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            st.download_button(
                label="📥 Download SOC Report",
                data=generated_text,
                file_name=f"soc_report_{timestamp}.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Application Error: {str(e)}")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
### 🔐 Enterprise AI Cybersecurity Platform

Built Using:
- Streamlit
- Hugging Face Inference API
- Prompt Engineering
- Chain-of-Thought AI

Use Cases:
- SOC Monitoring
- Incident Response
- Threat Intelligence
- Enterprise Security Automation
""")
