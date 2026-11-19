
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="👥",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #F4F7FC;
    }

    h1, h2, h3 {
        color: #17365D;
    }

    .main-title {
        color: #17365D;
        font-size: 34px;
        font-weight: 700;
    }

    .subtitle {
        color: #64748B;
        font-size: 15px;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
    }

    section[data-testid="stSidebar"] {
        background-color: #EAF0F8;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

DATA_FILE = Path(__file__).resolve().parent / "customer_data.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

try:
    df = load_data()
except FileNotFoundError:
    st.error("customer_data.csv was not found. Please run data.py first.")
    st.stop()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">Customer Segmentation Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Customer analytics | Demographics | Purchase behavior | K-Means clustering</div>',
    unsafe_allow_html=True
)

st.write("")

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("Dashboard Filters")

gender_options = ["All"] + sorted(df["Gender"].dropna().unique().tolist())
category_options = ["All"] + sorted(df["Preferred Category"].dropna().unique().tolist())
channel_options = ["All"] + sorted(df["Shopping Channel"].dropna().unique().tolist())

selected_gender = st.sidebar.selectbox("Select Gender", gender_options)
selected_category = st.sidebar.selectbox("Preferred Category", category_options)
selected_channel = st.sidebar.selectbox("Shopping Channel", channel_options)

st.sidebar.divider()
st.sidebar.subheader("Clustering Settings")

cluster_count = st.sidebar.slider(
    "Number of Customer Segments",
    min_value=2,
    max_value=8,
    value=5
)

# --------------------------------------------------
# K-MEANS CLUSTERING
# --------------------------------------------------

features = [
    "Age",
    "Annual Income",
    "Purchase Frequency",
    "Average Order Value",
    "Days Since Last Purchase"
]

scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[features])

kmeans = KMeans(
    n_clusters=cluster_count,
    random_state=42,
    n_init=10
)

df["Cluster"] = kmeans.fit_predict(scaled_data)

# --------------------------------------------------
# CREATE CUSTOMER SEGMENT PROFILES
# --------------------------------------------------

cluster_profile = (
    df.groupby("Cluster")
    .agg(
        Customers=("Customer ID", "count"),
        Average_Age=("Age", "mean"),
        Average_Income=("Annual Income", "mean"),
        Average_Frequency=("Purchase Frequency", "mean"),
        Average_Order_Value=("Average Order Value", "mean"),
        Average_Spending=("Total Spending", "mean"),
        Average_Recency=("Days Since Last Purchase", "mean")
    )
)

# Give segments meaningful names based on their actual profiles.
# Each special label is assigned to a different cluster.

remaining = set(cluster_profile.index)
segment_names = {}

# Highest average spending
high_value = cluster_profile["Average_Spending"].idxmax()
segment_names[high_value] = "High-Value Customers"
remaining.remove(high_value)

# Highest purchase frequency among remaining clusters
if remaining:
    frequent = cluster_profile.loc[
        list(remaining), "Average_Frequency"
    ].idxmax()
    segment_names[frequent] = "Frequent Shoppers"
    remaining.remove(frequent)

# Longest time since last purchase among remaining clusters
if remaining:
    at_risk = cluster_profile.loc[
        list(remaining), "Average_Recency"
    ].idxmax()
    segment_names[at_risk] = "At-Risk Customers"
    remaining.remove(at_risk)

# Lowest average income among remaining clusters
if remaining:
    budget = cluster_profile.loc[
        list(remaining), "Average_Income"
    ].idxmin()
    segment_names[budget] = "Budget-Conscious Customers"
    remaining.remove(budget)

# Give any additional clusters a neutral name
for number, cluster_id in enumerate(sorted(remaining), start=1):
    segment_names[cluster_id] = f"Other Customer Group {number}"

df["Segment"] = df["Cluster"].map(segment_names)

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()

if selected_gender != "All":
    filtered_df = filtered_df[
        filtered_df["Gender"] == selected_gender
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Preferred Category"] == selected_category
    ]

if selected_channel != "All":
    filtered_df = filtered_df[
        filtered_df["Shopping Channel"] == selected_channel
    ]

if filtered_df.empty:
    st.warning("No customers match the selected filters.")
    st.stop()

# --------------------------------------------------
# CUSTOMER OVERVIEW
# --------------------------------------------------

st.subheader("Customer Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{len(filtered_df):,}")
col2.metric("Average Age", f"{filtered_df['Age'].mean():.1f} years")
col3.metric("Average Annual Income", f"₹{filtered_df['Annual Income'].mean():,.0f}")
col4.metric("Total Customer Spending", f"₹{filtered_df['Total Spending'].sum():,.0f}")

st.write("")

# --------------------------------------------------
# CUSTOMER SEGMENT DISTRIBUTION
# --------------------------------------------------

st.subheader("Customer Segment Distribution")

segment_counts = (
    filtered_df["Segment"]
    .value_counts()
    .reset_index()
)

segment_counts.columns = ["Segment", "Customers"]

fig_segment = px.pie(
    segment_counts,
    names="Segment",
    values="Customers",
    hole=0.45,
    title="Distribution of Customer Segments",
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig_segment.update_layout(template="plotly_white")
st.plotly_chart(fig_segment, use_container_width=True)

# --------------------------------------------------
# DEMOGRAPHIC ANALYSIS
# --------------------------------------------------

st.subheader("Demographic Analysis")

col1, col2 = st.columns(2)

with col1:
    fig_age = px.histogram(
        filtered_df,
        x="Age",
        nbins=20,
        title="Customer Age Distribution",
        color_discrete_sequence=["#4472C4"]
    )
    fig_age.update_layout(template="plotly_white")
    st.plotly_chart(fig_age, use_container_width=True)

with col2:
    gender_data = (
        filtered_df["Gender"]
        .value_counts()
        .reset_index()
    )
    gender_data.columns = ["Gender", "Customers"]

    fig_gender = px.bar(
        gender_data,
        x="Gender",
        y="Customers",
        title="Customers by Gender",
        color="Gender",
        color_discrete_sequence=["#4472C4", "#ED7D9A"]
    )
    fig_gender.update_layout(template="plotly_white")
    st.plotly_chart(fig_gender, use_container_width=True)

# --------------------------------------------------
# PURCHASE BEHAVIOR ANALYSIS
# --------------------------------------------------

st.subheader("Purchase Behavior Analysis")

col1, col2 = st.columns(2)

with col1:
    fig_frequency = px.box(
        filtered_df,
        x="Segment",
        y="Purchase Frequency",
        color="Segment",
        title="Purchase Frequency by Segment"
    )
    fig_frequency.update_layout(template="plotly_white")
    st.plotly_chart(fig_frequency, use_container_width=True)

with col2:
    spending_data = (
        filtered_df.groupby("Segment", as_index=False)["Total Spending"]
        .mean()
        .sort_values("Total Spending")
    )

    fig_spending = px.bar(
        spending_data,
        x="Total Spending",
        y="Segment",
        orientation="h",
        color="Segment",
        title="Average Spending by Segment"
    )
    fig_spending.update_layout(
        template="plotly_white",
        showlegend=False,
        xaxis_title="Average Spending (₹)",
        yaxis_title="Customer Segment"
    )
    st.plotly_chart(fig_spending, use_container_width=True)

# --------------------------------------------------
# CUSTOMER CLUSTER VISUALIZATION
# --------------------------------------------------

st.subheader("Customer Cluster Visualization")

fig_clusters = px.scatter(
    filtered_df,
    x="Annual Income",
    y="Total Spending",
    color="Segment",
    hover_data=[
        "Customer ID",
        "Age",
        "Purchase Frequency",
        "Preferred Category"
    ],
    title="Customer Segments: Income vs Spending",
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig_clusters.update_layout(
    template="plotly_white",
    xaxis_title="Annual Income (₹)",
    yaxis_title="Total Spending (₹)"
)

st.plotly_chart(fig_clusters, use_container_width=True)

# --------------------------------------------------
# SEGMENT-WISE CUSTOMER PREFERENCES
# --------------------------------------------------

st.subheader("Customer Preferences by Segment")

col1, col2 = st.columns(2)

with col1:
    category_segment = (
        filtered_df.groupby(
            ["Preferred Category", "Segment"]
        )
        .size()
        .reset_index(name="Customers")
    )

    fig_category = px.bar(
        category_segment,
        x="Customers",
        y="Preferred Category",
        color="Segment",
        orientation="h",
        barmode="group",
        title="Preferred Categories by Customer Segment"
    )

    fig_category.update_layout(
        template="plotly_white",
        yaxis_title="Preferred Category",
        xaxis_title="Number of Customers"
    )

    st.plotly_chart(fig_category, use_container_width=True)

with col2:
    channel_segment = (
        filtered_df.groupby(
            ["Shopping Channel", "Segment"]
        )
        .size()
        .reset_index(name="Customers")
    )

    fig_channel = px.bar(
        channel_segment,
        x="Customers",
        y="Shopping Channel",
        color="Segment",
        orientation="h",
        barmode="group",
        title="Shopping Channels by Customer Segment"
    )

    fig_channel.update_layout(
        template="plotly_white",
        yaxis_title="Shopping Channel",
        xaxis_title="Number of Customers"
    )

    st.plotly_chart(fig_channel, use_container_width=True)

# --------------------------------------------------
# CUSTOMER SEGMENT CHARACTERISTICS
# --------------------------------------------------

st.subheader("Customer Segment Characteristics")

profile = (
    filtered_df.groupby("Segment")
    .agg(
        Customers=("Customer ID", "count"),
        Average_Age=("Age", "mean"),
        Average_Income=("Annual Income", "mean"),
        Average_Frequency=("Purchase Frequency", "mean"),
        Average_Order_Value=("Average Order Value", "mean"),
        Average_Spending=("Total Spending", "mean"),
        Average_Days_Since_Purchase=("Days Since Last Purchase", "mean")
    )
    .reset_index()
)

profile = profile.round(2)

st.dataframe(
    profile,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# TARGETED MARKETING STRATEGIES
# --------------------------------------------------

st.subheader("Targeted Marketing Recommendations")

strategies = {
    "High-Value Customers": (
        "Offer premium loyalty rewards, exclusive benefits and early access "
        "to new products to strengthen customer relationships."
    ),
    "Frequent Shoppers": (
        "Introduce repeat-purchase rewards, subscription options and "
        "personalized product recommendations."
    ),
    "At-Risk Customers": (
        "Consider re-engagement messages, limited-time offers and reminders "
        "to encourage another purchase."
    ),
    "Budget-Conscious Customers": (
        "Promote affordable bundles, discounts and value-for-money products."
    )
}

for segment in sorted(filtered_df["Segment"].unique()):
    with st.expander(segment):
        if segment in strategies:
            st.write(strategies[segment])
        else:
            st.write(
                "Study this group's purchase patterns and preferences "
                "to design suitable personalized offers."
            )

# --------------------------------------------------
# AUTOMATED BUSINESS INSIGHTS
# --------------------------------------------------

st.subheader("Business Insights")

overall_profile = (
    df.groupby("Segment")
    .agg(
        Customers=("Customer ID", "count"),
        Average_Spending=("Total Spending", "mean"),
        Average_Frequency=("Purchase Frequency", "mean"),
        Average_Recency=("Days Since Last Purchase", "mean")
    )
)

top_spending_segment = overall_profile["Average_Spending"].idxmax()
top_frequency_segment = overall_profile["Average_Frequency"].idxmax()
largest_segment = overall_profile["Customers"].idxmax()
most_inactive_segment = overall_profile["Average_Recency"].idxmax()

insight1, insight2 = st.columns(2)

with insight1:
    st.info(
        f"**Highest spending:** {top_spending_segment} has the highest "
        f"average customer spending (₹"
        f"{overall_profile.loc[top_spending_segment, 'Average_Spending']:,.0f})."
    )

    st.info(
        f"**Most frequent shoppers:** {top_frequency_segment} has the "
        f"highest average purchase frequency."
    )

with insight2:
    st.info(
        f"**Largest customer group:** {largest_segment} contains "
        f"{int(overall_profile.loc[largest_segment, 'Customers'])} customers."
    )

    st.info(
        f"**Longest time since purchase:** {most_inactive_segment} has "
        f"the highest average days since last purchase."
    )

# --------------------------------------------------
# CUSTOMER DETAILS
# --------------------------------------------------

st.subheader("Customer Details")

display_columns = [
    "Customer ID",
    "Gender",
    "Age",
    "Annual Income",
    "Purchase Frequency",
    "Average Order Value",
    "Total Spending",
    "Days Since Last Purchase",
    "Preferred Category",
    "Shopping Channel",
    "Segment"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# DOWNLOAD REPORT
# --------------------------------------------------

csv_data = filtered_df[display_columns].to_csv(index=False)

st.download_button(
    label="Download Customer Segmentation Report",
    data=csv_data,
    file_name="customer_segmentation_report.csv",
    mime="text/csv"
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Customer Segmentation Project | Python | Pandas | "
    "Scikit-learn | Streamlit | Plotly"
)

st.caption(
    "This project uses synthetic sample customer records for educational analysis."
)
