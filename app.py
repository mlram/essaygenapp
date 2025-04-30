import streamlit as st
import requests

API_ENDPOINT = "https://2j2icw0a1e.execute-api.us-east-1.amazonaws.com/devenvironment/essaygeneration"

# --- Page Config ---
st.set_page_config(page_title="Essay Generator", page_icon="📝", layout="wide")

# --- Sidebar (Inputs) ---
st.sidebar.title("⚙️ Essay Settings")
st.sidebar.markdown("Customize your essay prompt")

essay_topic = st.sidebar.text_input(
    "📝 Essay Topic", placeholder="e.g., AIT Thailand and Education")
max_len = st.sidebar.slider(
    "✍️ Essay Length", min_value=100, max_value=1024, value=512, step=100)
show_debug = st.sidebar.checkbox("🧪 Show Raw API Response")

# --- Main Title ---
st.title("📚 EssayGenApp")
st.markdown("A coursework for cloud computing by Ram Chandra Giri")

# --- Main Action Button ---
col1, col2 = st.columns([2, 1])
with col1:
    if st.button("🚀 Generate Essay"):
        if not essay_topic.strip():
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("Generating your essay..."):
                try:
                    payload = {"essay-topic": essay_topic}
                    response = requests.post(API_ENDPOINT, json=payload)

                    if response.status_code == 200:
                        result = response.json()
                        essay_text = result.get("essay", "")

                        if essay_text:
                            st.success("✅ Essay successfully generated!")

                            # --- Output Section ---
                            st.subheader("📄 Generated Essay")
                            st.text_area("Essay", essay_text, height=400)

                            # --- Download Section ---
                            st.download_button(
                                label="💾 Download Essay as TXT",
                                data=essay_text,
                                file_name=f"{essay_topic.replace(' ', '_')}.txt",
                                mime="text/plain"
                            )

                            # --- Debug Output (optional) ---
                            if show_debug:
                                st.divider()
                                st.subheader("🛠 Raw Response")
                                st.json(result)
                        else:
                            st.error("⚠️ No essay was generated.")
                    else:
                        st.error(
                            f"❌ API Error: {response.status_code} - {response.text}")

                except Exception as e:
                    st.error(f"🚨 Error: {e}")
    else:
        st.info("Enter a topic and click 'Generate Essay' to get started.")
