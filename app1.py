import streamlit as st
import requests

HF_TOKEN = "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"

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"

API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

st.set_page_config(
    page_title="AI Cybersecurity Incident Analyzer",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI Cybersecurity Incident Analyzer")

incident_logs = st.text_area(
    "Enter Cybersecurity Incident Logs",
    height=300
)

SYSTEM_PROMPT = """
You are an Enterprise Cybersecurity Threat Intelligence Analyst.

Analyze cybersecurity incidents step-by-step.

Provide:
1. Threat Summary
2. Attack Pattern
3. Severity Level
4. Affected Systems
5. Mitigation Strategy
6. Prevention Recommendations
7. Final SOC Report
"""

if st.button("Analyze Incident"):

    if incident_logs.strip() == "":
        st.warning("Please enter incident logs.")

    else:

        prompt = f"""
        {SYSTEM_PROMPT}

        INCIDENT LOGS:
        {incident_logs}
        """

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 700,
                "temperature": 0.3
            }
        }

        with st.spinner("Analyzing Threats..."):

            response = requests.post(
                API_URL,
                headers=headers,
                json=payload
            )

        try:

            result = response.json()

            if isinstance(result, list):
                output = result[0]["generated_text"]
            else:
                output = str(result)

            st.success("Analysis Completed")

            st.write(output)

        except Exception as e:
            st.error(str(e))
