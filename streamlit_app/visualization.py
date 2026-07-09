import streamlit as st
import pandas as pd
import plotly.express as px

# Security Overview

def show_security_overview(summary, processing_time):

    st.subheader("🔐 Security Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Traffic", summary["total"])

    c2.metric(
        "🟢 Safe",
        f'{summary["safe_count"]} ({summary["safe_percent"]}%)'
    )

    c3.metric(
        "🔴 Malicious",
        f'{summary["malicious_count"]} ({summary["malicious_percent"]}%)'
    )

    c4.metric("Risk Level",summary["risk_level"])

    st.info(f"⚡ Analysis completed in **{processing_time} seconds**")

    if summary["malicious_count"] > 0:

        st.error(f"⚠️ {summary['malicious_count']:,} malicious network flow(s) detected.")

    else:
        st.success( "✅ No malicious traffic detected.")

# Network Traffic Pie Chart

def plot_network_status(summary):

    st.subheader("📊 Network Traffic Status")

    status_df = pd.DataFrame(
        {
            "Status": [
                "🟢 Safe Traffic",
                "🔴 Malicious Traffic"
            ],
            "Count": [
                summary["safe_count"],
                summary["malicious_count"]
            ]
        }
    )

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

    fig.update_traces(textinfo="label+percent",textfont_size=17,pull=[0, 0.08])

    fig.update_layout(height=450,showlegend=True,legend_title="Traffic Status")

    st.plotly_chart(fig,use_container_width=True)

# Malicious Traffic Table

def show_malicious_flows(result):
    malicious_flows = result[
        result["traffic_status"].str.contains("Malicious")].copy()

    if malicious_flows.empty:
        return

    st.subheader("🚨 Detected Malicious Network Flows")

    malicious_flows.insert(0,"Row Number", malicious_flows.index + 1)

    st.info(f"Detected **{len(malicious_flows):,}** malicious network flow(s).")

    important_columns = [
        "Row Number",
        "attack_type",
        "confidence",
        "traffic_status"
    ]

    existing_columns = [
        col for col in important_columns
        if col in malicious_flows.columns
    ]

    st.dataframe(
        malicious_flows[existing_columns],
        use_container_width=True
    )

# Attack Distribution

def plot_attack_distribution(result):

    st.subheader("📈 Attack Analysis")

    attack_df = (
        result[
            result["attack_type"] != "BENIGN"]["attack_type"].value_counts().reset_index())

    if attack_df.empty:

        st.success("✅ No attack categories detected. All traffic is classified as BENIGN.")
        return

    attack_df.columns = ["Attack Type","Count"]

    attack_df["Percentage"] = (attack_df["Count"]/ attack_df["Count"].sum()* 100).round(2)

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
        showlegend=False,
        xaxis_title="Number of Flows",
        yaxis_title="Attack Type"
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

# Prediction Report

def show_prediction_report(result):

    st.subheader("📋 Detailed Prediction Report")

    st.dataframe(result,use_container_width=True)

    csv = result.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Security Report",
        data=csv,
        file_name="network_intrusion_report.csv",
        mime="text/csv"
    )