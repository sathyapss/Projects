import streamlit as st
import pandas as pd
from modules.connector import DataConnector

# Initialize Modules
connector = DataConnector()

# Page Config
st.set_page_config(
    page_title="DataNudge",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI/UX
def load_css():
    st.markdown("""
        <style>
        /* Main Gradient Background */
        .stApp {
            background: linear-gradient(to right, #f8f9fa, #e9ecef);
        }
        
        /* CARD STYLING */
        .stMetric {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* HEADER STYLING */
        h1, h2, h3 {
            color: #2c3e50;
            font-family: 'Helvetica', sans-serif;
        }
        h1 {
            background: -webkit-linear-gradient(45deg, #6a11cb, #2575fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        
        /* NAVIGATION - RADIO BUTTON (TOP NAV) */
        div[role="radiogroup"] > label {
            background: #ffffff;
            padding: 12px 30px; /* Larger padding */
            border-radius: 30px;
            border: 2px solid #e0e0e0;
            margin-right: 15px;
            transition: all 0.3s ease;
        }
        div[role="radiogroup"] > label > div {
            font-size: 22px !important; /* Larger Text */
            font-weight: 800 !important;
            color: #555;
        }
        div[role="radiogroup"] > label:hover {
            border-color: #6a11cb;
            transform: translateY(-2px);
        }
        div[role="radiogroup"] > label[data-checked="true"] {
            background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
            border: none;
            box-shadow: 0 6px 15px rgba(106, 17, 203, 0.4);
        }
        div[role="radiogroup"] > label[data-checked="true"] > div {
            color: white !important;
        }
        
        /* NAVIGATION - TABS (DASHBOARD NAV) */
        button[data-baseweb="tab"] {
            padding: 15px 30px !important;
            background-color: transparent;
            border: None !important;
        }
        button[data-baseweb="tab"] > div > div > p {
            font-size: 24px !important; /* Huge Font for Tabs */
            font-weight: 700 !important;
            color: #666;
        }
        button[data-baseweb="tab"][aria-selected="true"] > div > div > p {
            color: #2575fc !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            background-color: #eef2ff !important;
            border-radius: 10px;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #f7f9fc;
            border-right: 1px solid #e0e0e0;
        }
        
        /* Button Styling */
        .stButton>button {
            border-radius: 20px;
            background: linear-gradient(90deg, #efd5ff 0%, #515ada 100%);
            color: white;
            border: none;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            font-size: 16px !important;
            padding: 10px 25px !important;
        }
        </style>
    """, unsafe_allow_html=True)

load_css()

# Title
st.title("DataNudge 🌈")
st.caption("🚀 AI-Powered Data Analyst - Transforming Data into Stories")

# Session State for Data
if 'data' not in st.session_state:
    st.session_state.data = None
if 'filename' not in st.session_state:
    st.session_state.filename = ""

# --- TOP NAVIGATION ---
if st.session_state.data is not None:
    # stylized container for nav
    with st.container():
        page = st.radio("Navigation", ["Home", "Dashboard", "Export"], horizontal=True, label_visibility="collapsed")
else:
    page = "Home"

# --- PAGE: HOME ---
if page == "Home":
    st.markdown("### 📂 Connect Your Data")
    
    tab1, tab2 = st.tabs(["Upload CSV/Excel", "Connect Database"])
    
    with tab1:
        uploaded_file = st.file_uploader("Drop your file here", type=['csv', 'xlsx'])
        if uploaded_file:
            df = connector.load_csv(uploaded_file)
            if isinstance(df, pd.DataFrame):
                st.session_state.data = df
                st.session_state.filename = uploaded_file.name
                st.success(f"✅ Loaded {uploaded_file.name}")
                st.dataframe(df.head())
                if st.button("🚀 Go to Dashboard"):
                    # Force a rerun to switch tabs/radio if state was connected
                    st.rerun()
            else:
                st.error(f"Error loading file: {df}")

    with tab2:
        st.subheader("Database Settings")
        col1, col2 = st.columns(2)
        with col1:
            db_type = st.selectbox("Database Type", ["SQLite", "PostgreSQL", "MySQL"])
            host = st.text_input("Host", "localhost")
        with col2:
            db_name = st.text_input("Database Name/Path")
            user = st.text_input("Username") 
            
        password = st.text_input("Password", type="password")
            
        if st.button("Connect DB"):
            status = connector.connect_db(db_type, host, "5432", user, password, db_name)
            if status is True:
                st.success(f"Connected to {db_name}")
            else:
                 st.error(f"Connection Failed: {status}")

# --- PAGE: DASHBOARD ---
elif page == "Dashboard":
    
    # Imports
    from modules.eda import EDA
    from modules.relationships import RelationshipManager
    from modules.ai_insights import AIAnalyst
    import plotly.express as px
    
    # Initialize Objects
    df = st.session_state.data
    eda = EDA(df)
    rel_manager = RelationshipManager(df)
    
    # AI Config Section (Collapsible)
    with st.expander("🤖 AI Configuration (Gemini API)"):
        default_key = st.secrets.get("GEMINI_API_KEY", "")
        api_key = st.text_input("Enter API Key", value=default_key, type="password")
        ai_analyst = AIAnalyst(api_key=api_key)

    # Horizontal Tabs for Analysis Modules
    t_overview, t_corr, t_trends, t_anomalies, t_ai = st.tabs([
        "📊 Overview", 
        "🔗 Correlations", 
        "📈 Trends", 
        "🚨 Anomalies", 
        "🤖 AI Analyst"
    ])

    # --- TAB 1: Overview ---
    with t_overview:
        st.subheader("Dataset Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Rows", df.shape[0])
            st.metric("Total Columns", df.shape[1])
            st.write("**Missing Values:**")
            st.dataframe(eda.get_missing_values())
            
        with col2:
            st.write("**Quick Cleaner:**")
            if api_key:
                if st.button("✨ Generate Cleaning Rules"):
                    with st.spinner("AI analyzing..."):
                        context = ai_analyst.analyze_dataframe_head(df)
                        insight = ai_analyst.generate_insight(context, "cleaning")
                        st.markdown(insight)
            else:
                st.info("Add API Key for AI Cleaning suggestions.")

        st.markdown("---")
        st.subheader("Distributions")
        num_cols, cat_cols = eda.get_columns_by_type()
        selected_col = st.selectbox("Select Variable", df.columns, key="dist_sel")
        
        if selected_col in num_cols:
            fig = px.histogram(df, x=selected_col, marginal="box", title=f"Distribution of {selected_col}", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = px.bar(df[selected_col].value_counts(), title=f"Counts of {selected_col}", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

    # --- TAB 2: Correlations ---
    with t_corr:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Heatmap")
            fig = rel_manager.plot_correlation_heatmap()
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Not enough numerical data.")
        with col2:
            st.subheader("Top Correlated Pairs")
            pairs = rel_manager.find_highly_correlated_pairs()
            if pairs:
                for p in pairs:
                    st.success(f"{p[0]} ↔ {p[1]} ({p[2]:.2f})")
            else:
                st.info("No strong correlations.")
                
            st.markdown("---")
            st.subheader("Driver Analysis")
            target = st.selectbox("Target Metric", df.select_dtypes('number').columns, key="target_sel")
            if target:
                drivers = rel_manager.identify_potential_causes(target)
                st.write(drivers)

    # --- TAB 3: Trends ---
    with t_trends:
        st.subheader("Time Series Analysis")
        date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        
        if date_cols:
            col1, col2 = st.columns(2)
            with col1:
                date_col = st.selectbox("Date Column", df.columns, index=df.columns.get_loc(date_cols[0]))
            with col2:
                value_col = st.selectbox("Value Column", df.select_dtypes('number').columns, key="trend_val")
            
            fig, growth = rel_manager.detect_trends(date_col, value_col)
            if fig:
                st.metric("Growth Rate (Start to End)", f"{growth:.2f}%")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No date column detected. Please ensure your date column has 'date' or 'time' in the name.")

    # --- TAB 4: Anomalies ---
    with t_anomalies:
        st.subheader("Outlier Detection")
        numeric_cols, _ = eda.get_columns_by_type()
        selected_col = st.selectbox("Select Column", numeric_cols, key="out_sel")
        
        outliers = eda.detect_outliers()
        if selected_col in outliers:
            cnt = len(outliers[selected_col])
            st.error(f"Found {cnt} outliers in {selected_col}")
            fig = px.box(df, y=selected_col, points="all", title=f"Outliers: {selected_col}", color_discrete_sequence=['red'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("No outliers detected.")

    # --- TAB 5: AI Insights ---
    with t_ai:
        st.header("🤖 AI Analysis")
        st.caption("Unlock intelligent insights powered by Gemini.")
        
        if not api_key:
            st.warning("⚠️ Please configure API Key in the expander above to use these features.")
        
        context = ai_analyst.analyze_dataframe_head(df)
        
        # Vertical Layout for better readability
        
        # Section 1: Data Story
        st.subheader("📝 Data Storytelling")
        st.write("Turn your data into a compelling narrative.")
        if st.button("Generate Data Story", key="btn_story"):
            with st.spinner("Crafting narrative..."):
                story = ai_analyst.generate_insight(context, "story")
                st.markdown("### 📖 The Story")
                st.markdown(story)
        
        st.divider()
        
        # Section 2: Strategic Insights
        st.subheader("💡 Strategic Insights")
        st.write("Discover key trends and actionable takeaways.")
        if st.button("Generate Strategic Analysis", key="btn_insight"):
            with st.spinner("Analyzing patterns..."):
                summary = ai_analyst.generate_insight(context, "summary")
                st.markdown("### 🔍 Key Findings")
                st.markdown(summary)
                
        st.divider()
        
        # Section 3: KPIs
        st.subheader("🎯 KPI & Metrics")
        st.write("Get recommended performance indicators based on your data.")
        if st.button("Suggest KPIs", key="btn_kpi"):
            with st.spinner("Designing KPIs..."):
                kpis = ai_analyst.generate_insight(context, "kpi")
                st.markdown("### 📊 Recommended KPIs")
                st.markdown(kpis)

# --- PAGE: ADVANCED ANALYSIS / EXPORT ---
elif page == "Export":
    from modules.report_generator import ReportGenerator
    
    st.header("📤 Export Report")
    st.write("Generate a PDF report of the current analysis.")
    
    if st.button("Generate PDF Report"):
        with st.spinner("Generating PDF..."):
            try:
                gen = ReportGenerator(st.session_state.data)
                pdf_path = "data_nudge_report.pdf"
                gen.generate_report(pdf_path)
                
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="Download PDF",
                        data=f,
                        file_name="DataNudge_Report.pdf",
                        mime="application/pdf"
                    )
                st.success("Report generated successfully!")
            except Exception as e:
                st.error(f"Failed to generate report: {e}")



