import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Bank Loan Analysis",
    page_icon="🏦",
    layout="wide",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #F8FAFC;
}

[data-testid="stMainBlockContainer"] {
    width: 100% !important;
    max-width: none !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-top: 2rem !important;
}

[data-testid="stAppViewContainer"] {
    overflow-x: hidden !important;
}

[data-testid="column"] {
    min-width: 0 !important;
}

[data-testid="stHorizontalBlock"] {
    width: 100% !important;
    gap: 0.6rem !important;
}

[data-testid="stAppViewContainer"] {
    overflow-x: hidden;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 0rem;
    padding-left: 1.2rem;
    padding-right: 1.2rem;
    max-width: 1500px;
}


/* Main title */

.main-title {
    font-size: 32px;
    font-weight: 800;
    color: #172554;
    margin-bottom: 2px;
}

.subtitle {
    color: #64748B;
    font-size: 14px;
    margin-bottom: 20px;
}


/* Sidebar */

[data-testid="stSidebar"] {
    background-color: #F1F5F9;
}

.sidebar-title {
    font-size: 20px;
    font-weight: 800;
    color: #174A8B;
    margin-bottom: 20px;
}

.sidebar-section {
    font-size: 14px;
    font-weight: 800;
    color: #174A8B;
    margin-top: 15px;
    margin-bottom: 8px;
}


/* KPI cards */

.kpi-card {
    padding: 14px 16px;
    border-radius: 10px;
    height: 88px;
    box-sizing: border-box;
    margin-bottom: 12px;
    border: 1px solid #E2E8F0;
}

.kpi-title {
    font-size: 12px;
    font-weight: 600;
    color: #475569;
}

.kpi-value {
    font-size: 23px;
    font-weight: 750;
    margin-top: 7px;
    color: #172554;
}

.blue {
    background-color: #EFF6FF;
    border-left: 5px solid #2878C8;
}

.green {
    background-color: #ECFDF3;
    border-left: 5px solid #45B96B;
}

.red {
    background-color: #FEF2F2;
    border-left: 5px solid #E05252;
}

.yellow {
    background-color: #FFFBEB;
    border-left: 5px solid #E8B923;
}

.purple {
    background-color: #F5F3FF;
    border-left: 5px solid #8B5CF6;
}

.teal {
    background-color: #ECFEFF;
    border-left: 5px solid #14B8A6;
}


/* Chart containers */

.chart-title {
    font-size: 16px;
    font-weight: 700;
    color: #1E293B;
}


/* About box */

.about-box {
    background-color: #EAF3FF;
    border: 1px solid #C9DDF5;
    border-radius: 8px;
    padding: 15px;
    color: #334155;
    font-size: 13px;
    line-height: 1.6;
}


/* Footer */

.footer {
    background-color: #174A8B;
    color: white;
    text-align: center;
    padding: 10px;
    margin-top: 15px;
    font-size: 13px;
}


/* Hide unnecessary Streamlit elements */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

try:
    df = pd.read_csv("loan_approval.csv")
except FileNotFoundError:
    st.error("loan_approval.csv file not found. Keep the CSV file in the same folder as app.py.")
    st.stop()


# =========================================================
# BASIC CLEANING
# =========================================================

df.columns = df.columns.str.strip()


# ---------------------------------------------------------
# Loan Status
# ---------------------------------------------------------

if "loan_status" in df.columns:

    df["Loan Status"] = df["loan_status"].apply(
        lambda x: "Approved" if str(x).strip() in ["1", "1.0", "Approved", "approved", "Yes"]
        else "Rejected"
    )

else:
    df["Loan Status"] = "Unknown"


# ---------------------------------------------------------
# Gender
# ---------------------------------------------------------

if "person_gender_male" in df.columns:

    df["Gender"] = df["person_gender_male"].apply(
        lambda x: "Male" if str(x).strip().lower() in ["1", "1.0", "true", "male"]
        else "Female"
    )

elif "person_gender" in df.columns:

    df["Gender"] = df["person_gender"].astype(str).str.title()

else:

    df["Gender"] = "Not Available"


# ---------------------------------------------------------
# Loan Amount
# ---------------------------------------------------------

if "loan_amnt" not in df.columns:

    st.error("Column 'loan_amnt' not found in the dataset.")
    st.stop()

df["loan_amnt"] = pd.to_numeric(
    df["loan_amnt"],
    errors="coerce"
).fillna(0)


# ---------------------------------------------------------
# Annual Income
# ---------------------------------------------------------

if "person_income" not in df.columns:

    st.error("Column 'person_income' not found in the dataset.")
    st.stop()

df["person_income"] = pd.to_numeric(
    df["person_income"],
    errors="coerce"
).fillna(0)


# ---------------------------------------------------------
# Credit Score
# ---------------------------------------------------------

if "credit_score" in df.columns:

    df["credit_score"] = pd.to_numeric(
        df["credit_score"],
        errors="coerce"
    ).fillna(0)

else:

    df["credit_score"] = 0


# =========================================================
# LOAN PURPOSE
# =========================================================

loan_purpose_map = {
    "loan_intent_EDUCATION": "Education",
    "loan_intent_HOMEIMPROVEMENT": "Home Improvement",
    "loan_intent_MEDICAL": "Medical",
    "loan_intent_PERSONAL": "Personal",
    "loan_intent_VENTURE": "Venture",
    "loan_intent_DEBTCONSOLIDATION": "Debt Consolidation",
    "loan_intent_DEBT_CONSOLIDATION": "Debt Consolidation",
    "loan_intent_CREDITCARD": "Credit Card",
    "loan_intent_CREDIT_CARD": "Credit Card",
    "loan_intent_MAJORPURCHASE": "Major Purchase",
    "loan_intent_MAJOR_PURCHASE": "Major Purchase",
    "loan_intent_SMALLBUSINESS": "Small Business",
    "loan_intent_SMALL_BUSINESS": "Small Business",
    "loan_intent_CAR": "Car"
}


purpose_columns = [
    col for col in df.columns
    if col in loan_purpose_map
]


def get_loan_purpose(row):

    for col in purpose_columns:

        value = str(row[col]).strip().lower()

        if value in ["1", "1.0", "true", "yes"]:

            return loan_purpose_map[col]

    return "Other"


df["Loan Purpose"] = df.apply(
    get_loan_purpose,
    axis=1
)


# =========================================================
# EMPLOYMENT EXPERIENCE
# =========================================================

if "person_emp_exp" in df.columns:

    df["person_emp_exp"] = pd.to_numeric(
        df["person_emp_exp"],
        errors="coerce"
    ).fillna(0)

    df["Employment Experience"] = df["person_emp_exp"].apply(
        lambda x:
        "0 Years" if x == 0
        else "1-5 Years" if x <= 5
        else "6-10 Years" if x <= 10
        else "10+ Years"
    )

else:

    df["Employment Experience"] = "Not Available"


# =========================================================
# MARITAL STATUS
# =========================================================

if "person_marital_status" in df.columns:

    df["Marital Status"] = (
        df["person_marital_status"]
        .astype(str)
        .str.title()
    )

elif "marital_status" in df.columns:

    df["Marital Status"] = (
        df["marital_status"]
        .astype(str)
        .str.title()
    )

else:

    df["Marital Status"] = "Not Available"


# =========================================================
# APPLICATION ID
# =========================================================

df["Application ID"] = [
    f"LA{str(i + 1).zfill(3)}"
    for i in range(len(df))
]


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-title">
            🏦 BANK LOAN<br>
            &nbsp;&nbsp;&nbsp;&nbsp;ANALYSIS
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">FILTERS</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # Loan Status Filter
    # -----------------------------------------------------

    loan_status_filter = st.selectbox(
        "Loan Status",
        ["All", "Approved", "Rejected"],
        key="loan_status_filter"
    )


    # -----------------------------------------------------
    # Employment Experience Filter
    # -----------------------------------------------------

    experience_options = ["All"] + sorted(
        df["Employment Experience"].dropna().unique().tolist()
    )

    experience_filter = st.selectbox(
        "Employment Experience",
        experience_options,
        key="experience_filter"
    )


    # -----------------------------------------------------
    # Loan Purpose Filter
    # -----------------------------------------------------

    purpose_options = ["All"] + sorted(
        df["Loan Purpose"].dropna().unique().tolist()
    )

    purpose_filter = st.selectbox(
        "Loan Purpose",
        purpose_options,
        key="purpose_filter"
    )


    # -----------------------------------------------------
    # Credit Score Range
    # -----------------------------------------------------

    credit_min = int(df["credit_score"].min())
    credit_max = int(df["credit_score"].max())

    credit_range = st.slider(
        "Credit Score Range",
        min_value=credit_min,
        max_value=credit_max,
        value=(credit_min, credit_max),
        key="credit_range"
    )


    # -----------------------------------------------------
    # Income Range
    # -----------------------------------------------------

    income_min = int(df["person_income"].min())
    income_max = int(df["person_income"].max())

    income_range = st.slider(
        "Annual Income Range",
        min_value=income_min,
        max_value=income_max,
        value=(income_min, income_max),
        key="income_range"
    )


    # -----------------------------------------------------
    # Clear Filters
    # -----------------------------------------------------

    if st.button("🔄  Clear Filters", use_container_width=True):

        st.session_state["loan_status_filter"] = "All"
        st.session_state["experience_filter"] = "All"
        st.session_state["purpose_filter"] = "All"
        st.session_state["credit_range"] = (
            credit_min,
            credit_max
        )
        st.session_state["income_range"] = (
            income_min,
            income_max
        )

        st.rerun()


    st.markdown("---")


    # -----------------------------------------------------
    # About
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="about-box">

        <b>ⓘ ABOUT</b>

        <br><br>

        This dashboard provides insights into bank loan
        applications and approval patterns based on
        financial, credit and loan related factors.

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()


if loan_status_filter != "All":

    filtered_df = filtered_df[
        filtered_df["Loan Status"] == loan_status_filter
    ]


if experience_filter != "All":

    filtered_df = filtered_df[
        filtered_df["Employment Experience"] == experience_filter
    ]


if purpose_filter != "All":

    filtered_df = filtered_df[
        filtered_df["Loan Purpose"] == purpose_filter
    ]


filtered_df = filtered_df[
    (filtered_df["credit_score"] >= credit_range[0])
    &
    (filtered_df["credit_score"] <= credit_range[1])
]


filtered_df = filtered_df[
    (filtered_df["person_income"] >= income_range[0])
    &
    (filtered_df["person_income"] <= income_range[1])
]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🏦 Bank Loan Analysis Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Overview of loan applications and approval performance</div>',
    unsafe_allow_html=True
)


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_applications = len(filtered_df)

approved_loans = (
    filtered_df["Loan Status"] == "Approved"
).sum()

rejected_loans = (
    filtered_df["Loan Status"] == "Rejected"
).sum()


if total_applications > 0:

    approval_rate = (
        approved_loans / total_applications
    ) * 100

    total_loan_amount = (
        filtered_df["loan_amnt"].sum()
    )

    average_loan_amount = (
        filtered_df["loan_amnt"].mean()
    )

else:

    approval_rate = 0
    total_loan_amount = 0
    average_loan_amount = 0


# =========================================================
# KEY METRICS
# =========================================================

st.markdown("### 📊 Key Metrics")


col1, col2, col3, col4, col5, col6 = st.columns(6)


with col1:

    st.markdown(
        f"""
        <div class="kpi-card blue">
            <div class="kpi-title">Total Applications</div>
            <div class="kpi-value">{total_applications:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="kpi-card green">
            <div class="kpi-title">Approved Loans</div>
            <div class="kpi-value">{approved_loans:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="kpi-card red">
            <div class="kpi-title">Rejected Loans</div>
            <div class="kpi-value">{rejected_loans:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="kpi-card yellow">
            <div class="kpi-title">Approval Rate</div>
            <div class="kpi-value">{approval_rate:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col5:

    st.markdown(
        f"""
        <div class="kpi-card purple">
            <div class="kpi-title">Total Loan Amount</div>
            <div class="kpi-value">₹{total_loan_amount / 1000000:.2f}M</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col6:

    st.markdown(
        f"""
        <div class="kpi-card teal">
            <div class="kpi-title">Average Loan Amount</div>
            <div class="kpi-value">₹{average_loan_amount / 1000:.2f}K</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CHART 1
# =========================================================

chart_col1, chart_col2, chart_col3 = st.columns(3)


with chart_col1:

    status_counts = (
        filtered_df["Loan Status"]
        .value_counts()
        .reindex(["Approved", "Rejected"])
        .fillna(0)
    )

    fig_status = go.Figure(
        data=[
            go.Pie(
                labels=status_counts.index,
                values=status_counts.values,
                hole=0.55,
                marker=dict(
                    colors=["#45B96B", "#E05252"]
                ),
                textinfo="percent",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Applications: %{value:,}<br>"
                    "Percentage: %{percent}"
                    "<extra></extra>"
                )
            )
        ]
    )

    fig_status.update_layout(
        title="Loan Status Distribution",
        height=300,
        margin=dict(l=10, r=10, t=45, b=10),
        showlegend=True,
        legend=dict(
            orientation="v"
        )
    )

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )


# =========================================================
# CHART 2
# =========================================================

with chart_col2:

    employment_status = (
        filtered_df
        .groupby(
            ["Employment Experience", "Loan Status"]
        )
        .size()
        .reset_index(name="Applications")
    )

    fig_employment = px.bar(
        employment_status,
        x="Employment Experience",
        y="Applications",
        color="Loan Status",
        barmode="stack",
        color_discrete_map={
            "Approved": "#45B96B",
            "Rejected": "#E05252"
        },
        title="Loan Status by Employment Experience"
    )

    fig_employment.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=45, b=10),
        legend_title="Loan Status"
    )

    st.plotly_chart(
        fig_employment,
        use_container_width=True
    )


# =========================================================
# CHART 3
# =========================================================

with chart_col3:

    def credit_group(score):

        if score < 400:
            return "300-400"
        elif score < 500:
            return "400-500"
        elif score < 600:
            return "500-600"
        elif score < 700:
            return "600-700"
        else:
            return "700-850"


    credit_data = filtered_df.copy()

    credit_data["Credit Score Range"] = (
        credit_data["credit_score"]
        .apply(credit_group)
    )


    credit_summary = (
        credit_data
        .groupby("Credit Score Range")
        .agg(
            Applications=("Loan Status", "size"),
            Approved=(
                "Loan Status",
                lambda x: (x == "Approved").sum()
            )
        )
        .reset_index()
    )


    credit_summary["Approval Rate"] = (
        credit_summary["Approved"]
        /
        credit_summary["Applications"]
        * 100
    )


    credit_order = [
        "300-400",
        "400-500",
        "500-600",
        "600-700",
        "700-850"
    ]


    credit_summary["Credit Score Range"] = pd.Categorical(
        credit_summary["Credit Score Range"],
        categories=credit_order,
        ordered=True
    )


    credit_summary = (
        credit_summary
        .sort_values("Credit Score Range")
    )


    fig_credit = px.line(
        credit_summary,
        x="Credit Score Range",
        y="Approval Rate",
        markers=True,
        text="Approval Rate",
        title="Approval Rate by Credit Score Range"
    )


    fig_credit.update_traces(
        line=dict(
            color="#2878C8",
            width=3
        ),
        marker=dict(
            size=8
        ),
        texttemplate="%{text:.1f}%",
        textposition="top center"
    )


    fig_credit.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=45, b=10),
        yaxis_title="Approval Rate (%)",
        xaxis_title="Credit Score Range",
        yaxis=dict(
            range=[0, 100]
        )
    )


    st.plotly_chart(
        fig_credit,
        use_container_width=True
    )


# =========================================================
# SECOND ROW
# =========================================================

chart_col4, chart_col5, chart_col6 = st.columns(3)


# =========================================================
# CHART 4
# =========================================================

with chart_col4:

    purpose_summary = (
        filtered_df
        .groupby("Loan Purpose")["loan_amnt"]
        .sum()
        .reset_index()
        .sort_values(
            "loan_amnt",
            ascending=True
        )
    )


    fig_purpose = px.bar(
        purpose_summary,
        x="loan_amnt",
        y="Loan Purpose",
        orientation="h",
        text="loan_amnt",
        title="Total Loan Amount by Loan Purpose"
    )


    fig_purpose.update_traces(
        marker_color="#2878C8",
        texttemplate="%{x:.1s}",
        textposition="outside"
    )


    fig_purpose.update_layout(
        height=300,
        margin=dict(l=10, r=30, t=45, b=10),
        xaxis_title="Loan Amount",
        yaxis_title="Loan Purpose"
    )


    st.plotly_chart(
        fig_purpose,
        use_container_width=True
    )


# =========================================================
# CHART 5
# =========================================================

with chart_col5:

    experience_average = (
        filtered_df
        .groupby("Employment Experience")["loan_amnt"]
        .mean()
        .reset_index()
    )


    fig_average = px.bar(
        experience_average,
        x="Employment Experience",
        y="loan_amnt",
        text="loan_amnt",
        title="Average Loan Amount by Employment Experience"
    )


    fig_average.update_traces(
        marker_color="#2878C8",
        texttemplate="₹%{y:.2s}",
        textposition="outside"
    )


    fig_average.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=45, b=10),
        yaxis_title="Average Loan Amount",
        xaxis_title="Employment Experience"
    )


    st.plotly_chart(
        fig_average,
        use_container_width=True
    )


# =========================================================
# CHART 6
# =========================================================

with chart_col6:

    fig_scatter = px.scatter(
        filtered_df,
        x="person_income",
        y="loan_amnt",
        title="Loan Amount vs Annual Income",
        opacity=0.45,
        trendline=None
    )


    fig_scatter.update_traces(
        marker=dict(
            color="#2878C8",
            size=5
        )
    )


    fig_scatter.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=45, b=10),
        xaxis_title="Annual Income",
        yaxis_title="Loan Amount"
    )


    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )


# =========================================================
# RECENT LOAN APPLICATIONS
# =========================================================

st.markdown("## 📋 Recent Loan Applications")

recent_df = filtered_df[
    [
        "Gender",
        "person_age",
        "person_income",
        "loan_amnt",
        "loan_int_rate",
        "credit_score",
        "Loan Purpose",
        "Loan Status"
    ]
].tail(6).copy()

recent_df.columns = [
    "Gender",
    "Age",
    "Annual Income",
    "Loan Amount",
    "Interest Rate",
    "Credit Score",
    "Loan Purpose",
    "Loan Status"
]

def style_status(val):
    if val == "Approved":
        return "background-color: #DFF5E5; color: #15803D; font-weight: 600;"
    elif val == "Rejected":
        return "background-color: #FDE2E2; color: #B91C1C; font-weight: 600;"
    return ""

styled_recent_df = recent_df.style.map(
    style_status,
    subset=["Loan Status"]
)

st.dataframe(
    styled_recent_df,
    width="stretch",
    height=280,
    hide_index=True
)
# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Bank Loan Analysis Dashboard | Built with Streamlit ❤️
    </div>
    """,
    unsafe_allow_html=True
)