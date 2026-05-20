import streamlit as st
import requests
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Cybersecurity Incident Analyzer",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("⚙️ Configuration")

hf_token = st.sidebar.text_input(
    "Enter Hugging Face API Key",
    type="password"
)

model_name = st.sidebar.selectbox(
    "Select Model",
    [
        "mistralai/Mistral-7B-Instruct-v0.3",
        "google/gemma-2-9b-it",
        "meta-llama/Llama-3.1-8B-Instruct"
    ]
)

# =====================================================
# HEADER
# =====================================================

st.title("🛡️ AI Cybersecurity Incident Analyzer")

st.markdown("""
Analyze cybersecurity incidents using:
- Chain-of-Thought Prompting
- AI Threat Intelligence
- Enterprise SOC Automation
""")

# =====================================================
# SYSTEM PROMPT
# =====================================================

SYSTEM_PROMPT = """
You are an Enterprise Cybersecurity Threat Intelligence Analyst.

Analyze cybersecurity incidents step-by-step.

Tasks:
1. Threat Summary
2. Attack Pattern Detection
3. Severity Analysis
4. Affected Systems
5. Indicators of Compromise
6. Threat Propagation Risk
7. Mitigation Strategy
8. Prevention Recommendations
9. Final SOC Report

Use professional cybersecurity terminology.
"""

# =====================================================
# INPUT AREA
# =====================================================

incident_logs = st.text_area(
    "📄 Enter Cybersecurity Incident Logs",
    height=300
)

# =====================================================
# ANALYZE BUTTON
# =====================================================

if st.button("🚀 Analyze Incident"):

    if not hf_token:
        st.error("Please enter Hugging Face API Key.")

    elif not incident_logs.strip():
        st.warning("Please enter cybersecurity logs.")

    else:

        try:

            API_URL = f"https://api-inference.huggingface.co/models/{model_name}"

            headers = {
                "Authorization": f"Bearer {hf_token}"
            }

            final_prompt = f"""
            {SYSTEM_PROMPT}

            INCIDENT LOGS:
            {incident_logs}

            Generate enterprise cybersecurity analysis.
            """

            payload = {
                "inputs": final_prompt,
                "parameters": {
                    "max_new_tokens": 1000,
                    "temperature": 0.3
                }
            }

            with st.spinner("Analyzing cybersecurity threats..."):

                response = requests.post(
                    API_URL,
                    headers=headers,
                    json=payload
                )

                result = response.json()

            # =====================================================
            # OUTPUT EXTRACTION
            # =====================================================

            if isinstance(result, list):
                generated_text = result[0]["generated_text"]
            else:
                generated_text = str(result)

            st.success("Threat Analysis Completed Successfully")

            # =====================================================
            # SEVERITY DISPLAY
            # =====================================================

            if "Critical" in generated_text:
                st.error("🔴 Severity Level: CRITICAL")

            elif "High" in generated_text:
                st.warning("🟠 Severity Level: HIGH")

            elif "Medium" in generated_text:
                st.warning("🟡 Severity Level: MEDIUM")

            else:
                st.success("🟢 Severity Level: LOW")

            # =====================================================
            # REPORT DISPLAY
            # =====================================================

            st.markdown("---")

            st.subheader("📊 Enterprise Threat Intelligence Report")

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
            st.error(f"Error: {str(e)}")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
### 🔐 Enterprise AI Cybersecurity Platform

Built Using:
- Streamlit
- Hugging Face API
- Prompt Engineering
- Chain-of-Thought AI
""")
