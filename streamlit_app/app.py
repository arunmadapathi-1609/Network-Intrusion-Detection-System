import streamlit as st
import pandas as pd
import time
import requests

from preprocessing import preprocess_data
from api import predict_batch
from utils import (merge_predictions,calculate_summary)
from visualization import (
    show_security_overview,
    plot_network_status,
    show_malicious_flows,
    plot_attack_distribution,
    show_prediction_report,
)
# Page Configuration

st.set_page_config(
    page_title="Network Intrusion Detection System",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Network Intrusion Detection System")

st.caption(
    "XGBoost based network traffic classification and threat detection dashboard"
)

# Upload Dataset

uploaded_file = st.file_uploader(
    "📂 Upload Network Traffic CSV",
    type=["csv"]
)

# Main Application

if uploaded_file:

    original_df = pd.read_csv(uploaded_file)

    st.subheader("📄 Dataset Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Flows",len(original_df))

    col2.metric("Features",original_df.shape[1])

    col3.metric("File",uploaded_file.name)

    st.dataframe(original_df.head(),use_container_width=True)

    if st.button("🚀 Analyze Traffic"):

        with st.spinner("Analyzing network traffic..."):
            start_time = time.time()

            try:
                 # Data Preprocessing

                processed_df = preprocess_data(original_df)

                # FastAPI Prediction
                predictions = predict_batch(processed_df)

                # Merge Results
                result = merge_predictions(original_df,predictions)
                processing_time = round(time.time() - start_time,2)

                summary = calculate_summary(result)

                st.success("Traffic analysis completed successfully!")

                # Dashboard

                show_security_overview(summary,processing_time)
                
                plot_network_status(summary)

                show_malicious_flows(result)

                plot_attack_distribution(result)

                show_prediction_report(result)

            except requests.exceptions.ConnectionError:

                st.error("❌ Unable to connect to the FastAPI server.")

            except requests.exceptions.HTTPError as e:

                st.error(f"❌ API Error: {e}")

            except Exception as e:

                st.exception(e)