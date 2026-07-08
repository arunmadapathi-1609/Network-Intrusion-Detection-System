import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px
import os

API_URL = "https://network-intrusion-detection-system-1-9ay5.onrender.com/predict_batch"

st.title("🛡️ Network Intrusion Detection System")

st.caption(
    "XGBoost based network traffic classification and threat detection dashboard"
)


uploaded_file = st.file_uploader(
    "📂 Upload Network Traffic CSV",
    type=["csv"]
)


if uploaded_file:

    df = pd.read_csv(uploaded_file)


    # Keep original data for report
    original_df = df.copy()


    # Clean column names
    df.columns = df.columns.str.strip()


    # Remove target column
    target_columns = [
        "Label",
        "label",
        "Attack",
        "attack"
    ]


    for col in target_columns:

        if col in df.columns:
            df = df.drop(
                col,
                axis=1
            )


    st.subheader(
        "📄 Dataset Overview"
    )


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Total Flows",
        len(df)
    )


    col2.metric(
        "Features",
        df.shape[1]
    )


    col3.metric(
        "File",
        uploaded_file.name
    )


    st.dataframe(
        original_df.head(),
        use_container_width=True
    )


    if st.button(
        "🚀 Analyze Traffic"
    ):


        with st.spinner(
            "Analyzing network traffic..."
        ):
            start_time = time.time()


            try:


                # -----------------------------
                # Data preprocessing
                # -----------------------------


                input_df = df.copy()


                # Replace infinity values

                input_df = input_df.replace(
                    [
                        float("inf"),
                        float("-inf")
                    ],
                    0
                )


                # Convert all columns safely

                input_df = input_df.apply(
                    pd.to_numeric,
                    errors="coerce"
                )


                # Replace missing values

                input_df = input_df.fillna(0)


                payload = input_df.to_dict(
                    orient="records"
                )


                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=300
                )


                if response.status_code != 200:


                    st.error(
                        response.text
                    )

                    st.stop()

                predictions = pd.DataFrame(
                     response.json()
                )

                processing_time = round(
                    time.time() - start_time,
                    2
                )

                result = pd.concat(
                    [
                        original_df.reset_index(drop=True),
                        predictions
                    ],
                    axis=1
                )


                st.success(
                    "Traffic analysis completed successfully!"
                )


                # -----------------------------
                # Security Overview
                # -----------------------------


                st.subheader(
                    "🔐 Security Overview"
                )


                safe_count = (
                    result["traffic_status"]
                    .str.contains("Safe")
                    .sum()
                )


                malicious_count = (
                    result["traffic_status"]
                    .str.contains("Malicious")
                    .sum()
                )
                safe_percent = round(
                       safe_count / len(result) * 100,
                       2
                )
                malicious_percent = round(
                    malicious_count / len(result) * 100,
                    2
                )
                c1, c2, c3, c4 = st.columns(4)


                c1.metric(
                    "Total Traffic",
                    len(result)
                )


                c2.metric(
                    "🟢 Safe",
                    f"{safe_count} ({safe_percent}%)"
                )


                c3.metric(
                    "🔴 Malicious",
                    f"{malicious_count} ({malicious_percent}%)"
                )

                risk = "🟢 Low"
                if malicious_percent <= 5:
                      risk = "🟢 Low"
                      
                elif malicious_percent <= 15:
                      risk = "🟡 Medium"
                elif malicious_percent <= 30:
                      risk = "🟠 High"
                else:
                    risk = "🔴 Critical"
                
                c4.metric(
                     "Risk Level",
                     risk
                )
                st.info(
                      f"⚡ Analysis completed in **{processing_time} seconds**"
                )
                
                if malicious_count > 0:
                      st.error(
                            f"⚠️ {malicious_count:,} malicious network flow(s) detected."
                      )
                else:
                     st.success(
                          "✅ No malicious traffic detected."
                    )
                # ==========================================================
                # Network Traffic Status
                # ==========================================================

                st.subheader("📊 Network Traffic Status")
                
                status_df = pd.DataFrame({
                       "Status": ["🟢 Safe Traffic", "🔴 Malicious Traffic"],
                       "Count": [safe_count, malicious_count]
                })
                fig = px.pie(
                       status_df,
                       names="Status",
                       values="Count",
                       hole=0.55,
                       title="Overall Network Traffic",
                       color="Status",
                       color_discrete_map={
                               "🟢 Safe Traffic": "#2ECC71",
                               "🔴 Malicious Traffic": "#E74C3C"
                        }
                )
                fig.update_traces(
                       textinfo="label+percent",
                       textfont_size=17,
                       pull=[0, 0.08]
                )
                fig.update_layout(
                       showlegend=True,
                       height=450,
                       legend_title="Traffic Status"
                )
                st.plotly_chart(
                     fig,
                     use_container_width=True
                )
                # -----------------------------
                # Threat Detection
                # -----------------------------

                if malicious_count > 0:
                      st.subheader("🚨 Detected Malicious Network Flows")
                      malicious_flows = result[
                            result["traffic_status"].str.contains("Malicious")
                      ].copy()
                      
                      malicious_flows.insert(
                            0,
                            "Row Number",
                            malicious_flows.index + 1
                      )
                      st.info(
                            f"Detected **{malicious_count:,}** malicious network flows."
                      )
                      
                      important_columns = [
                            "Row Number",
                            "attack_type",
                            "confidence",
                            "traffic_status"
                      ]
                      
                      existing = [
                            col for col in important_columns
                            if col in malicious_flows.columns
                      ]
                      
                      st.dataframe(
                           malicious_flows[existing],
                           use_container_width=True
                     )

                # -----------------------------
                # Attack Analysis
                # -----------------------------
                st.subheader("📈 Attack Analysis")
                attack_df = (
                     result[
                          result["attack_type"] != "BENIGN"
                          ]["attack_type"]
                          .value_counts()
                          .reset_index()
                    )
                if not attack_df.empty:
                     attack_df.columns = [
                           "Attack Type",
                           "Count"
                     ]
                     attack_df["Percentage"] = (
                          attack_df["Count"]
                          / attack_df["Count"].sum()
                          * 100
                     ).round(2)
                     
                     top_attack = attack_df.iloc[0]
                     st.success(
                          f"Most frequent attack detected: **{top_attack['Attack Type']}** "
                          f"({top_attack['Count']:,} flows)"
                     )
                     fig = px.bar(
                          attack_df,
                          x="Count",
                          y="Attack Type",
                          orientation="h",
                          color="Attack Type",
                          text="Percentage",
                          title="Detected Attack Distribution"
                     )
                     fig.update_traces(
                          texttemplate="%{text}%",
                          textposition="outside"
                     )
                     fig.update_layout(
                          height=500,
                          xaxis_title="Number of Flows",
                          yaxis_title="Attack Type",
                          showlegend=False
                     )
                     st.plotly_chart(
                          fig,
                          use_container_width=True
                     )
                     st.dataframe(
                          attack_df,
                          use_container_width=True,
                          hide_index=True
                     )
                else:
                     st.success(
                          "✅ No attack categories detected. All traffic is classified as BENIGN."
                     )

                # ==========================================================
                # Prediction Report
                # ==========================================================

                st.subheader("📋 Detailed Prediction Report")
                
                st.dataframe(
                     result,
                     use_container_width=True
                )
                csv = result.to_csv(
                     index=False
                ).encode("utf-8")
                
                st.download_button(
                     label="📥 Download Security Report",
                     data=csv,
                     file_name="network_intrusion_report.csv",
                     mime="text/csv"
                )
            except requests.exceptions.ConnectionError:
                 st.error("❌ FastAPI server is not running.")
                 
            except Exception as e:
                 st.exception(e)