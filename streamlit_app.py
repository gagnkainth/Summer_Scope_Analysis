import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="SummerScope",
    page_icon="🌞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #FFD700 0%, #FF8C00 50%, #FF6B35 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2E86AB;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #FF6B35;
        padding-bottom: 0.5rem;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .insight-box {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #FF6B35;
    }
    .insight-box p {
        text-align: justify;
    }
    .weather-insight {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #2E86AB;
    }
    .weather-insight p {
        text-align: justify;
    }
    .extreme-weather {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #e74c3c;
    }
    .extreme-weather p {
        text-align: justify;
    }
    .data-summary {
        background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #9b59b6;
    }
    .data-summary p {
        text-align: justify;
    }
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Enhanced Expander Styling */
    div[data-testid="stExpander"] > div:first-child {
        background: linear-gradient(135deg, #ff9a56 0%, #ff6b35 100%) !important;
        color: white !important;
        border-radius: 15px !important;
        border: 3px solid #e55a2b !important;
        padding: 15px 20px !important;
        font-weight: bold !important;
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3) !important;
        transition: all 0.3s ease !important;
        margin: 10px 0 !important;
    }
    
    div[data-testid="stExpander"] > div:first-child:hover {
        background: linear-gradient(135deg, #ff8642 0%, #e55a2b 100%) !important;
        box-shadow: 0 12px 35px rgba(255, 107, 53, 0.4) !important;
        transform: translateY(-3px) scale(1.01) !important;
        border-color: #d44820 !important;
    }
    
    div[data-testid="stExpander"] > div:first-child * {
        color: white !important;
    }
    
    div[data-testid="stExpander"] > div:first-child svg {
        fill: white !important;
        stroke: white !important;
    }
    
    /* Alternative selector for broader compatibility */
    .stExpander > div:first-child {
        background: linear-gradient(135deg, #ff9a56 0%, #ff6b35 100%) !important;
        color: white !important;
        border-radius: 15px !important;
        border: 3px solid #e55a2b !important;
        padding: 15px 20px !important;
        font-weight: bold !important;
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3) !important;
        transition: all 0.3s ease !important;
        margin: 10px 0 !important;
    }
    
    .stExpander > div:first-child:hover {
        background: linear-gradient(135deg, #ff8642 0%, #e55a2b 100%) !important;
        box-shadow: 0 12px 35px rgba(255, 107, 53, 0.4) !important;
        transform: translateY(-3px) scale(1.01) !important;
    }
    
    .stExpander > div:first-child * {
        color: white !important;
        font-weight: bold !important;
    }
    
    /* Universal expander styling - all expanders */
    details summary {
        background: linear-gradient(135deg, #ff9a56 0%, #ff6b35 100%) !important;
        color: white !important;
        border-radius: 15px !important;
        border: 3px solid #e55a2b !important;
        padding: 15px 20px !important;
        font-weight: bold !important;
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3) !important;
        transition: all 0.3s ease !important;
        margin: 10px 0 !important;
        cursor: pointer !important;
    }
    
    details summary:hover {
        background: linear-gradient(135deg, #ff8642 0%, #e55a2b 100%) !important;
        box-shadow: 0 12px 35px rgba(255, 107, 53, 0.4) !important;
        transform: translateY(-3px) scale(1.01) !important;
        border-color: #d44820 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the data"""
    try:
        # Load datasets
        df_main = pd.read_csv("Indian Summers - Over the years-2007-11.csv")
        df_2021 = pd.read_csv("Indian Summers - Over the years.csv")
        
        # Combine datasets
        df_combined = pd.concat([df_main, df_2021], ignore_index=True)
        
        # Remove duplicates
        df_combined.drop_duplicates(inplace=True)
        
        # Convert Date to datetime
        df_combined['Date'] = pd.to_datetime(df_combined['Date'], errors='coerce')
        
        # Extract Year and Month
        df_combined['Year'] = df_combined['Date'].dt.year
        df_combined['Month'] = df_combined['Date'].dt.month
        df_combined['Month_Name'] = df_combined['Date'].dt.month_name()
        
        # Clean data - remove rows with missing important values
        df_combined.dropna(subset=[
            'tempmax', 'tempmin', 'temp',
            'humidity', 'windspeed', 'cloudcover'
        ], inplace=True)
        
        # Remove outliers from temperature
        Q1 = df_combined['temp'].quantile(0.25)
        Q3 = df_combined['temp'].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df_combined = df_combined[(df_combined['temp'] >= lower) & (df_combined['temp'] <= upper)]
        
        df_combined.reset_index(drop=True, inplace=True)
        
        return df_combined
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def main():
    # Main title with enhanced styling
    st.markdown('<h1 class="main-header">🌞 SummerScope</h1>', unsafe_allow_html=True)
    
    # Add a subtitle
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; color: #666;">
        <h3>Comprehensive Weather Data Analysis (2007-2021)</h3>
        <p>Explore temperature trends, weather patterns, and climate insights across Indian cities</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    if df is None:
        st.stop()
    
    # Quick Overview Box
    st.markdown("""
    <div class="insight-box">
        <h3>📊 Dataset Overview</h3>
        <p>This dashboard analyzes weather data from multiple Indian cities during summer months, 
        providing insights into temperature patterns, humidity levels, wind conditions, and more.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar filters with enhanced styling
    st.sidebar.markdown("## 🔍 Interactive Filters")
    st.sidebar.markdown("*Customize your analysis by selecting specific parameters*")
    
    # Kaggle Dataset Link in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Dataset Source")
    st.sidebar.markdown("""
    <div style="text-align: center; margin: 1rem 0;">
        <a href="https://www.kaggle.com/datasets/akashram/indian-summer-over-the-years" target="_blank" style="
            background: linear-gradient(135deg, #20beff 0%, #1a94ff 100%);
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
            box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
            display: inline-block;
            width: 90%;
            text-align: center;
        ">
            📊 Open Dataset on Kaggle
        </a>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    # Add filter control buttons at the top
    col_btn1, col_btn2 = st.sidebar.columns(2)
    
    # Year filter with Select All option
    st.sidebar.markdown("### 📅 Year Selection")
    years = sorted(df['Year'].unique())
    
    col_y1, col_y2 = st.sidebar.columns([3, 1])
    with col_y1:
        select_all_years = st.checkbox("Select All Years", value=True, key="all_years")
    with col_y2:
        if st.button("Clear", key="clear_years"):
            st.session_state.selected_years = []
    
    # Initialize default years if not in session state
    if 'selected_years' not in st.session_state:
        st.session_state.selected_years = years if select_all_years else []
    
    if select_all_years:
        selected_years = st.sidebar.multiselect("Choose Years", years, default=years, key="selected_years",
                                               help="Choose specific years to analyze")
    else:
        selected_years = st.sidebar.multiselect("Choose Years", years, 
                                               default=st.session_state.selected_years, key="selected_years",
                                               help="Choose specific years to analyze")
    
    # City filter with Select All option
    st.sidebar.markdown("### 🏙️ City Selection")
    cities = sorted(df['City'].unique())
    
    col_c1, col_c2 = st.sidebar.columns([3, 1])
    with col_c1:
        select_all_cities = st.checkbox("Select All Cities", value=False, key="all_cities")
    with col_c2:
        if st.button("Clear", key="clear_cities"):
            st.session_state.selected_cities = []
    
    # Initialize default cities if not in session state
    if 'selected_cities' not in st.session_state:
        st.session_state.selected_cities = cities if select_all_cities else (cities[:5] if len(cities) > 5 else cities)
    
    if select_all_cities:
        selected_cities = st.sidebar.multiselect("Choose Cities", cities, default=cities, key="selected_cities",
                                                help="Select cities for comparison")
    else:
        selected_cities = st.sidebar.multiselect("Choose Cities", cities, 
                                                default=st.session_state.selected_cities, key="selected_cities",
                                                help="Select cities for comparison")
    
    # Month filter with Select All option
    st.sidebar.markdown("### 📆 Month Selection")
    months = sorted(df['Month'].unique())
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                   7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    month_display = [f"{month} - {month_names.get(month, 'Unknown')}" for month in months]
    
    col_m1, col_m2 = st.sidebar.columns([3, 1])
    with col_m1:
        select_all_months = st.checkbox("Select All Months", value=True, key="all_months")
    with col_m2:
        if st.button("Clear", key="clear_months"):
            st.session_state.selected_months = []
    
    # Initialize default months if not in session state
    if 'selected_months_display' not in st.session_state:
        st.session_state.selected_months_display = month_display if select_all_months else month_display
    
    if select_all_months:
        selected_months_display = st.sidebar.multiselect("Choose Months", month_display, default=month_display, key="selected_months_display",
                                                        help="Choose specific months to focus on")
        selected_months = [int(item.split(' - ')[0]) for item in selected_months_display]
    else:
        selected_months_display = st.sidebar.multiselect("Choose Months", month_display, 
                                                        default=st.session_state.selected_months_display, key="selected_months_display",
                                                        help="Choose specific months to focus on")
        selected_months = [int(item.split(' - ')[0]) for item in selected_months_display]
    
    # Temperature range filter
    st.sidebar.markdown("### 🌡️ Temperature Range")
    temp_range = st.sidebar.slider("Select temperature range (°C)", 
                                  float(df['temp'].min()), 
                                  float(df['temp'].max()),
                                  (float(df['temp'].min()), float(df['temp'].max())),
                                  help="Filter data by temperature range")
    
    # Weather condition filter
    st.sidebar.markdown("### 🌤️ Weather Conditions")
    conditions = sorted(df['conditions'].dropna().unique())
    
    col_w1, col_w2 = st.sidebar.columns([3, 1])
    with col_w1:
        select_all_conditions = st.checkbox("Select All Conditions", value=True, key="all_conditions")
    with col_w2:
        if st.button("Clear", key="clear_conditions"):
            st.session_state.selected_conditions = []
    
    # Initialize default conditions if not in session state
    if 'selected_conditions' not in st.session_state:
        st.session_state.selected_conditions = conditions if select_all_conditions else (conditions[:5] if len(conditions) > 5 else conditions)
    
    if select_all_conditions:
        selected_conditions = st.sidebar.multiselect("Choose Conditions", conditions, default=conditions, key="selected_conditions",
                                                    help="Filter by weather conditions")
    else:
        selected_conditions = st.sidebar.multiselect("Choose Conditions", conditions, 
                                                    default=st.session_state.selected_conditions, key="selected_conditions",
                                                    help="Filter by weather conditions")
    
    # Filter control buttons
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Filter Controls")
    
    col_btn1, col_btn2 = st.sidebar.columns(2)
    with col_btn1:
        apply_filter = st.button("🔍 Apply Filters", type="primary", use_container_width=True,
                                help="Click to apply selected filters and update charts")
    with col_btn2:
        reset_filter = st.button("🔄 Reset All", use_container_width=True,
                                help="Reset all filters to default values")
    
    # Handle reset filter
    if reset_filter:
        st.session_state.selected_years = years
        st.session_state.selected_cities = cities[:5] if len(cities) > 5 else cities
        st.session_state.selected_months_display = month_display
        st.session_state.selected_conditions = conditions[:5] if len(conditions) > 5 else conditions
        st.rerun()
    
    # Initialize session state for filters if not exists
    if 'filters_applied' not in st.session_state:
        st.session_state.filters_applied = False
        st.session_state.current_filters = {
            'years': years,
            'cities': cities[:5] if len(cities) > 5 else cities,
            'months': months,
            'temp_range': (float(df['temp'].min()), float(df['temp'].max())),
            'conditions': conditions[:5] if len(conditions) > 5 else conditions
        }
    
    # Update filters when Apply is clicked
    if apply_filter:
        st.session_state.filters_applied = True
        st.session_state.current_filters = {
            'years': selected_years,
            'cities': selected_cities,
            'months': selected_months,
            'temp_range': temp_range,
            'conditions': selected_conditions
        }
        st.rerun()
    
    # Use stored filters for data filtering
    if st.session_state.filters_applied:
        filter_years = st.session_state.current_filters['years']
        filter_cities = st.session_state.current_filters['cities']
        filter_months = st.session_state.current_filters['months']
        filter_temp_range = st.session_state.current_filters['temp_range']
        filter_conditions = st.session_state.current_filters['conditions']
    else:
        # Default filters
        filter_years = years
        filter_cities = cities[:5] if len(cities) > 5 else cities
        filter_months = months
        filter_temp_range = (float(df['temp'].min()), float(df['temp'].max()))
        filter_conditions = conditions[:5] if len(conditions) > 5 else conditions
    
    # Show current filter status
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Current Filter Status")
    
    if st.session_state.filters_applied:
        st.sidebar.success("✅ Filters Applied")
        st.sidebar.info(f"""
        **Active Filters:**
        - **Years:** {len(filter_years)} selected
        - **Cities:** {len(filter_cities)} selected  
        - **Months:** {len(filter_months)} selected
        - **Temperature:** {filter_temp_range[0]:.1f}°C - {filter_temp_range[1]:.1f}°C
        - **Conditions:** {len(filter_conditions)} selected
        """)
    else:
        st.sidebar.warning("⚠️ Click 'Apply Filters' to update charts")
    
    # Filter data
    filtered_df = df[
        (df['Year'].isin(filter_years)) &
        (df['City'].isin(filter_cities)) &
        (df['Month'].isin(filter_months)) &
        (df['temp'] >= filter_temp_range[0]) &
        (df['temp'] <= filter_temp_range[1]) &
        (df['conditions'].isin(filter_conditions))
    ]
    
    if filtered_df.empty:
        st.warning("⚠️ No data available for the selected filters. Please adjust your selection.")
        return
    
    # Data Summary Section in Colorful Boxes
    st.markdown('<h2 class="sub-header">📋 Data Overview & Statistics</h2>', unsafe_allow_html=True)
    
    # Quick Data Summary - Full width
    total_records = len(filtered_df)
    date_range = f"{filtered_df['Date'].min().strftime('%Y-%m-%d')} to {filtered_df['Date'].max().strftime('%Y-%m-%d')}"
    unique_cities = filtered_df['City'].nunique()
    unique_years = filtered_df['Year'].nunique()
    
    st.markdown(f"""
    <div class="insight-box" style="min-height: 200px; display: flex; flex-direction: column; justify-content: flex-start;">
        <h3>📊 Dataset Summary</h3>
        <ul>
            <li><strong>Total Records:</strong> {total_records:,} weather observations</li>
            <li><strong>Date Range:</strong> {date_range}</li>
            <li><strong>Cities Covered:</strong> {unique_cities} cities</li>
            <li><strong>Years Analyzed:</strong> {unique_years} years</li>
            <li><strong>Data Quality:</strong> {((1 - filtered_df.isnull().sum().sum() / (len(filtered_df) * len(filtered_df.columns))) * 100):.1f}% complete</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample Data Preview in an expandable section with enhanced styling
    with st.expander("� Preview Sample Data", expanded=False):
        st.markdown("""
        <style>
        .stExpander > div:first-child {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border-radius: 12px !important;
            border: 2px solid #5a67d8 !important;
            padding: 12px 16px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        .stExpander > div:first-child:hover {
            background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
            transform: translateY(-2px) !important;
        }
        .stExpander > div:first-child div {
            color: white !important;
        }
        .stExpander > div:first-child svg {
            fill: white !important;
        }
        .stExpander > div:first-child p {
            color: white !important;
            font-weight: 600 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        display_cols = ['Date', 'City', 'temp', 'tempmax', 'tempmin', 'humidity', 'windspeed', 'conditions']
        sample_data = filtered_df[display_cols].head(10)
        st.dataframe(sample_data, use_container_width=True)
    
    # Key Metrics in Colorful Gradient Boxes
    st.markdown('<h2 class="sub-header">📊 Key Statistics</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_records = len(filtered_df)
        st.markdown(f"""
        <div class="extreme-weather" style="text-align: center; padding: 1rem; min-height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <h4>📋 Total Records</h4>
            <h2 style="color: #2E86AB; margin: 0.5rem 0;">{total_records:,}</h2>
            <p style="margin: 0;"><small>Weather Observations</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_temp = filtered_df['temp'].mean()
        st.markdown(f"""
        <div class="data-summary" style="text-align: center; padding: 1rem; min-height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <h4>🌡️ Avg Temperature</h4>
            <h2 style="color: #FF6B35; margin: 0.5rem 0;">{avg_temp:.1f}°C</h2>
            <p style="margin: 0;"><small>Mean Daily Temperature</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        max_temp = filtered_df['tempmax'].max()
        st.markdown(f"""
        <div class="insight-box" style="text-align: center; padding: 1rem; min-height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <h4>🔥 Highest Temperature</h4>
            <h2 style="color: #e74c3c; margin: 0.5rem 0;">{max_temp:.1f}°C</h2>
            <p style="margin: 0;"><small>Peak Recorded</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_humidity = filtered_df['humidity'].mean()
        st.markdown(f"""
        <div class="weather-insight" style="text-align: center; padding: 1rem; min-height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <h4>💧 Avg Humidity</h4>
            <h2 style="color: #3498db; margin: 0.5rem 0;">{avg_humidity:.1f}%</h2>
            <p style="margin: 0;"><small>Mean Humidity Level</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        cities_count = filtered_df['City'].nunique()
        st.markdown(f"""
        <div class="extreme-weather" style="text-align: center; padding: 1rem; min-height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <h4>🏙️ Cities Analyzed</h4>
            <h2 style="color: #9b59b6; margin: 0.5rem 0;">{cities_count}</h2>
            <p style="margin: 0;"><small>Unique Locations</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Advanced Statistics Row in Gradient Boxes
    st.markdown('<h3 style="color: #2E86AB; margin-top: 2rem; margin-bottom: 1rem;">📈 Advanced Statistical Measures</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        temp_std = filtered_df['temp'].std()
        st.markdown(f"""
        <div class="extreme-weather" style="text-align: center; padding: 1rem; min-height: 160px; display: flex; flex-direction: column; justify-content: center;">
            <h4>🌡️ Temperature Variation</h4>
            <h2 style="color: #e74c3c; margin: 0.5rem 0;">{temp_std:.1f}°C</h2>
            <p style="margin: 0;"><small>Standard Deviation</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        humidity_range = filtered_df['humidity'].max() - filtered_df['humidity'].min()
        st.markdown(f"""
        <div class="data-summary" style="text-align: center; padding: 1rem; min-height: 160px; display: flex; flex-direction: column; justify-content: center;">
            <h4>💧 Humidity Range</h4>
            <h2 style="color: #9b59b6; margin: 0.5rem 0;">{humidity_range:.1f}%</h2>
            <p style="margin: 0;"><small>Max - Min</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pressure_variation = filtered_df['sealevelpressure'].std()
        st.markdown(f"""
        <div class="insight-box" style="text-align: center; padding: 1rem; min-height: 160px; display: flex; flex-direction: column; justify-content: center;">
            <h4>📊 Pressure Variation</h4>
            <h2 style="color: #FF6B35; margin: 0.5rem 0;">{pressure_variation:.1f} mb</h2>
            <p style="margin: 0;"><small>Standard Deviation</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        wind_max = filtered_df['windspeed'].max()
        st.markdown(f"""
        <div class="weather-insight" style="text-align: center; padding: 1rem; min-height: 160px; display: flex; flex-direction: column; justify-content: center;">
            <h4>💨 Max Wind Speed</h4>
            <h2 style="color: #2E86AB; margin: 0.5rem 0;">{wind_max:.1f} km/h</h2>
            <p style="margin: 0;"><small>Peak Recorded</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Outlier Analysis Section
    st.markdown('<h2 class="sub-header">📊 Outlier Analysis & Data Quality</h2>', unsafe_allow_html=True)
    
    # Create violin plot for temperature outlier analysis
    st.markdown('<h3 style="color: #2E86AB; margin-top: 1rem; margin-bottom: 1rem;">🌡️ Temperature Distribution & Outlier Detection</h3>', unsafe_allow_html=True)
    
    # Calculate outlier statistics for insight box
    Q1 = filtered_df['temp'].quantile(0.25)
    Q3 = filtered_df['temp'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Count potential outliers in current filtered data
    outliers_below = len(filtered_df[filtered_df['temp'] < lower_bound])
    outliers_above = len(filtered_df[filtered_df['temp'] > upper_bound])
    total_outliers = outliers_below + outliers_above
    outlier_percentage = (total_outliers / len(filtered_df)) * 100
    
    # Create violin plot showing distribution
    fig_outlier = px.violin(filtered_df, y='temp', box=True,
                           title="Temperature Distribution with Outlier Detection",
                           color_discrete_sequence=['#FF6B35'])
    
    # Add horizontal lines for outlier bounds
    fig_outlier.add_hline(y=lower_bound, line_dash="dash", line_color="red", 
                         annotation_text=f"Lower Bound: {lower_bound:.1f}°C")
    fig_outlier.add_hline(y=upper_bound, line_dash="dash", line_color="red", 
                         annotation_text=f"Upper Bound: {upper_bound:.1f}°C")
    fig_outlier.add_hline(y=Q1, line_dash="dot", line_color="blue", 
                         annotation_text=f"Q1: {Q1:.1f}°C")
    fig_outlier.add_hline(y=Q3, line_dash="dot", line_color="blue", 
                         annotation_text=f"Q3: {Q3:.1f}°C")
    
    fig_outlier.update_layout(height=500, showlegend=False, width=800)
    fig_outlier.update_yaxes(title_text="Temperature (°C)")
    
    # Center the chart using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.plotly_chart(fig_outlier, use_container_width=True)
    
    # Outlier Analysis Insight Box
    st.markdown(f"""
    <div class="data-summary">
        <h4>📊 Outlier Analysis Insights:</h4>
        <p>The violin plot reveals the temperature distribution and outlier detection boundaries using the Interquartile Range (IQR) method. The data shows Q1 = <strong>{Q1:.1f}°C</strong>, Q3 = <strong>{Q3:.1f}°C</strong>, and IQR = <strong>{IQR:.1f}°C</strong>. Outlier boundaries are set at <strong>{lower_bound:.1f}°C (lower)</strong> and <strong>{upper_bound:.1f}°C (upper)</strong>. In the current filtered dataset, there are <strong>{total_outliers} potential outliers</strong> ({outlier_percentage:.2f}% of data), with <strong>{outliers_below} values below</strong> and <strong>{outliers_above} values above</strong> the normal range. The violin shape shows the density distribution, while the box plot overlay displays quartiles and outliers. During preprocessing, extreme outliers were removed to ensure data quality and reliable analysis results.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Additional Data Quality Metrics
    st.markdown('<h3 style="color: #2E86AB; margin-top: 2rem; margin-bottom: 1rem;">🔍 Data Quality Overview</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        temp_range_current = filtered_df['temp'].max() - filtered_df['temp'].min()
        st.markdown(f"""
        <div class="insight-box" style="text-align: center; padding: 1rem; min-height: 160px; display: flex; flex-direction: column; justify-content: center;">
            <h4>📏 Temperature Range</h4>
            <h2 style="color: #FF6B35; margin: 0.5rem 0;">{temp_range_current:.1f}°C</h2>
            <p style="margin: 0;"><small>Current Data Range</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        temp_std_current = filtered_df['temp'].std()
        st.markdown(f"""
        <div class="weather-insight" style="text-align: center; padding: 1rem; min-height: 160px; display: flex; flex-direction: column; justify-content: center;">
            <h4>📊 Standard Deviation</h4>
            <h2 style="color: #2E86AB; margin: 0.5rem 0;">{temp_std_current:.1f}°C</h2>
            <p style="margin: 0;"><small>Temperature Variability</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        data_completeness = ((1 - filtered_df.isnull().sum().sum() / (len(filtered_df) * len(filtered_df.columns))) * 100)
        st.markdown(f"""
        <div class="extreme-weather" style="text-align: center; padding: 1rem; min-height: 160px; display: flex; flex-direction: column; justify-content: center;">
            <h4>✅ Data Completeness</h4>
            <h2 style="color: #27ae60; margin: 0.5rem 0;">{data_completeness:.1f}%</h2>
            <p style="margin: 0;"><small>Non-null Values</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        duplicate_count = len(filtered_df) - len(filtered_df.drop_duplicates())
        st.markdown(f"""
        <div class="data-summary" style="text-align: center; padding: 1rem; min-height: 160px; display: flex; flex-direction: column; justify-content: center;">
            <h4>🔄 Duplicate Records</h4>
            <h2 style="color: #9b59b6; margin: 0.5rem 0;">{duplicate_count}</h2>
            <p style="margin: 0;"><small>Identified & Cleaned</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Correlation Analysis in Beautiful Boxes
    st.markdown('<h3 style="color: #2E86AB; margin-top: 2rem; margin-bottom: 1rem;">🔗 Correlation Analysis</h3>', unsafe_allow_html=True)
    
    # Calculate correlations
    temp_humidity_corr = filtered_df['temp'].corr(filtered_df['humidity'])
    temp_pressure_corr = filtered_df['temp'].corr(filtered_df['sealevelpressure'])
    temp_wind_corr = filtered_df['temp'].corr(filtered_df['windspeed'])
    humidity_pressure_corr = filtered_df['humidity'].corr(filtered_df['sealevelpressure'])
    
    corr_col1, corr_col2, corr_col3, corr_col4 = st.columns(4)
    
    with corr_col1:
        corr_color = "#e74c3c" if temp_humidity_corr < -0.3 else "#f39c12" if abs(temp_humidity_corr) < 0.3 else "#27ae60"
        corr_strength = "Strong" if abs(temp_humidity_corr) > 0.5 else "Moderate" if abs(temp_humidity_corr) > 0.3 else "Weak"
        st.markdown(f"""
        <div class="extreme-weather" style="text-align: center; padding: 1rem; min-height: 160px; display: flex; flex-direction: column; justify-content: center;">
            <h4>🌡️💧 Temp-Humidity</h4>
            <h2 style="color: {corr_color}; margin: 0.5rem 0;">{temp_humidity_corr:.3f}</h2>
            <p style="margin: 0;"><small>{corr_strength} Correlation</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with corr_col2:
        corr_color = "#e74c3c" if temp_pressure_corr < -0.3 else "#f39c12" if abs(temp_pressure_corr) < 0.3 else "#27ae60"
        corr_strength = "Strong" if abs(temp_pressure_corr) > 0.5 else "Moderate" if abs(temp_pressure_corr) > 0.3 else "Weak"
        st.markdown(f"""
        <div class="data-summary" style="text-align: center; padding: 1rem; min-height: 160px; display: flex; flex-direction: column; justify-content: center;">
            <h4>🌡️📊 Temp-Pressure</h4>
            <h2 style="color: {corr_color}; margin: 0.5rem 0;">{temp_pressure_corr:.3f}</h2>
            <p style="margin: 0;"><small>{corr_strength} Correlation</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with corr_col3:
        corr_color = "#e74c3c" if temp_wind_corr < -0.3 else "#f39c12" if abs(temp_wind_corr) < 0.3 else "#27ae60"
        corr_strength = "Strong" if abs(temp_wind_corr) > 0.5 else "Moderate" if abs(temp_wind_corr) > 0.3 else "Weak"
        st.markdown(f"""
        <div class="insight-box" style="text-align: center; padding: 1rem; min-height: 160px; display: flex; flex-direction: column; justify-content: center;">
            <h4>🌡️💨 Temp-Wind</h4>
            <h2 style="color: {corr_color}; margin: 0.5rem 0;">{temp_wind_corr:.3f}</h2>
            <p style="margin: 0;"><small>{corr_strength} Correlation</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with corr_col4:
        corr_color = "#e74c3c" if humidity_pressure_corr < -0.3 else "#f39c12" if abs(humidity_pressure_corr) < 0.3 else "#27ae60"
        corr_strength = "Strong" if abs(humidity_pressure_corr) > 0.5 else "Moderate" if abs(humidity_pressure_corr) > 0.3 else "Weak"
        st.markdown(f"""
        <div class="weather-insight" style="text-align: center; padding: 1rem; min-height: 160px; display: flex; flex-direction: column; justify-content: center;">
            <h4>💧📊 Humidity-Pressure</h4>
            <h2 style="color: {corr_color}; margin: 0.5rem 0;">{humidity_pressure_corr:.3f}</h2>
            <p style="margin: 0;"><small>{corr_strength} Correlation</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Visualization Section
    st.markdown('<h2 class="sub-header">📊 Interactive Charts & Visualizations</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <h3>📈 Visualization Overview</h3>
        <p>The following section presents 14 comprehensive charts analyzing various aspects of Indian summer weather patterns. Each visualization is accompanied by detailed insights and statistical analysis to help understand temperature trends, weather relationships, and climate patterns across different cities and time periods.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chart 1: Temperature Trend Over Years
    st.markdown('<h2 class="sub-header">📈 Chart 1: Temperature Trends Over Years</h2>', unsafe_allow_html=True)
    
    yearly_temp = filtered_df.groupby('Year').agg({
        'tempmax': 'mean',
        'tempmin': 'mean',
        'temp': 'mean'
    }).reset_index()
    
    fig1 = px.line(yearly_temp, x='Year', y=['tempmax', 'tempmin', 'temp'],
                   title="Average Temperature Trends Over Years",
                   labels={'value': 'Temperature (°C)', 'variable': 'Temperature Type'})
    fig1.update_layout(height=500)
    st.plotly_chart(fig1, use_container_width=True)
    
    # Chart 1 Insight
    temp_trend_slope = (yearly_temp['temp'].iloc[-1] - yearly_temp['temp'].iloc[0]) / len(yearly_temp)
    max_year = yearly_temp.loc[yearly_temp['temp'].idxmax(), 'Year']
    min_year = yearly_temp.loc[yearly_temp['temp'].idxmin(), 'Year']
    
    st.markdown(f"""
    <div class="insight-box">
        <h4>📈 Chart Insights:</h4>
        <p>This trend analysis shows temperature evolution over time. The average temperature trend is {'increasing' if temp_trend_slope > 0 else 'decreasing'} by approximately <strong>{abs(temp_trend_slope):.2f}°C per year</strong>. The warmest year on average was <strong>{max_year}</strong> ({yearly_temp['temp'].max():.1f}°C), while the coolest was <strong>{min_year}</strong> ({yearly_temp['temp'].min():.1f}°C). This long-term view helps identify climate patterns and potential warming or cooling trends in the region.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chart 2: City-wise Temperature Comparison (Box Plot)
    st.markdown('<h2 class="sub-header">🏙️ Chart 2: City-wise Temperature Distribution</h2>', unsafe_allow_html=True)
    
    fig2 = px.box(filtered_df, x='City', y='temp', 
                  title="Temperature Distribution by City",
                  color='City')
    fig2.update_xaxes(tickangle=45)
    fig2.update_layout(height=500)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Chart 2 Insight
    city_temps = filtered_df.groupby('City')['temp'].agg(['mean', 'std', 'min', 'max']).round(1)
    hottest_city = city_temps['mean'].idxmax()
    coolest_city = city_temps['mean'].idxmin()
    most_variable_city = city_temps['std'].idxmax()
    
    st.markdown(f"""
    <div class="weather-insight">
        <h4>🏙️ Chart Insights:</h4>
        <p>City-wise temperature comparison reveals significant regional variations. <strong>{hottest_city}</strong> has the highest average temperature ({city_temps.loc[hottest_city, 'mean']:.1f}°C), while <strong>{coolest_city}</strong> is the coolest ({city_temps.loc[coolest_city, 'mean']:.1f}°C). <strong>{most_variable_city}</strong> shows the most temperature variability (std: {city_temps.loc[most_variable_city, 'std']:.1f}°C). The box plots show the median, quartiles, and outliers, helping identify cities with consistent vs. variable temperature patterns.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chart 3: Monthly Temperature Patterns
    st.markdown('<h2 class="sub-header">📅 Chart 3: Monthly Temperature Patterns</h2>', unsafe_allow_html=True)
    
    monthly_temp = filtered_df.groupby('Month_Name')['temp'].mean().reset_index()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_temp['Month_Name'] = pd.Categorical(monthly_temp['Month_Name'], categories=month_order, ordered=True)
    monthly_temp = monthly_temp.sort_values('Month_Name')
    
    fig3 = px.bar(monthly_temp, x='Month_Name', y='temp',
                  title="Average Temperature by Month",
                  color='temp', color_continuous_scale='plasma')
    fig3.update_layout(height=500)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Chart 3 Insight
    hottest_month = monthly_temp.loc[monthly_temp['temp'].idxmax(), 'Month_Name']
    coolest_month = monthly_temp.loc[monthly_temp['temp'].idxmin(), 'Month_Name']
    temp_variation = monthly_temp['temp'].max() - monthly_temp['temp'].min()
    
    st.markdown(f"""
    <div class="insight-box">
        <h4>📊 Chart Insights:</h4>
        <p>This chart reveals the seasonal temperature patterns across different months. <strong>{hottest_month}</strong> shows the highest average temperature ({monthly_temp['temp'].max():.1f}°C), while <strong>{coolest_month}</strong> has the lowest ({monthly_temp['temp'].min():.1f}°C). The temperature variation across months is <strong>{temp_variation:.1f}°C</strong>, indicating clear seasonal differences. This pattern helps identify peak summer months and cooler periods for planning and analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chart 4: Temperature vs Humidity Scatter Plot
    st.markdown('<h2 class="sub-header">🌡️ Chart 4: Temperature vs Humidity Relationship</h2>', unsafe_allow_html=True)
    
    fig4 = px.scatter(filtered_df, x='temp', y='humidity', color='City',
                      title="Temperature vs Humidity Relationship",
                      size='windspeed', hover_data=['Date'])
    fig4.update_layout(height=500)
    st.plotly_chart(fig4, use_container_width=True)
    
    # Chart 4 Insight
    temp_humidity_corr = filtered_df['temp'].corr(filtered_df['humidity'])
    high_temp_low_humidity = len(filtered_df[(filtered_df['temp'] > filtered_df['temp'].quantile(0.75)) & 
                                            (filtered_df['humidity'] < filtered_df['humidity'].quantile(0.25))])
    
    st.markdown(f"""
    <div class="extreme-weather">
        <h4>🌡️ Chart Insights:</h4>
        <p>This scatter plot reveals the relationship between temperature and humidity across cities. The correlation coefficient is <strong>{temp_humidity_corr:.3f}</strong>, indicating a {'strong negative' if temp_humidity_corr < -0.5 else 'moderate negative' if temp_humidity_corr < -0.3 else 'weak' if abs(temp_humidity_corr) < 0.3 else 'positive'} relationship. There are <strong>{high_temp_low_humidity} instances</strong> of high temperature with low humidity, which typically indicates dry heat conditions. The bubble size represents wind speed, showing how air movement varies with temperature and humidity combinations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chart 5: Heatmap - Monthly Temperature by City
    st.markdown('<h2 class="sub-header">🔥 Chart 5: Temperature Heatmap (City vs Month)</h2>', unsafe_allow_html=True)
    
    pivot_data = filtered_df.groupby(['City', 'Month_Name'])['temp'].mean().unstack(fill_value=0)
    
    fig5, ax5 = plt.subplots(figsize=(12, 8))
    sns.heatmap(pivot_data, annot=True, cmap='Reds', fmt='.1f', ax=ax5)
    ax5.set_title("Average Temperature Heatmap (City vs Month)")
    st.pyplot(fig5)
    plt.close()
    
    # Chart 5 Insight
    if not pivot_data.empty:
        hottest_combo = pivot_data.stack().idxmax()
        coolest_combo = pivot_data.stack().idxmin()
        hottest_city_overall = pivot_data.mean(axis=1).idxmax()
        coolest_city_overall = pivot_data.mean(axis=1).idxmin()
        
        st.markdown(f"""
        <div class="data-summary">
            <h4>🔥 Chart Insights:</h4>
            <p>This heatmap provides a comprehensive view of temperature patterns across cities and months. The hottest combination is <strong>{hottest_combo[0]} in {hottest_combo[1]}</strong> ({pivot_data.stack().max():.1f}°C), while the coolest is <strong>{coolest_combo[0]} in {coolest_combo[1]}</strong> ({pivot_data.stack().min():.1f}°C). Overall, <strong>{hottest_city_overall}</strong> shows consistently high temperatures across months, while <strong>{coolest_city_overall}</strong> remains relatively cooler. This visualization helps identify regional climate patterns and seasonal variations simultaneously.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Chart 6: Wind Speed Distribution
    st.markdown('<h2 class="sub-header">💨 Chart 6: Wind Speed Distribution</h2>', unsafe_allow_html=True)
    
    fig6 = px.histogram(filtered_df, x='windspeed', nbins=30,
                        title="Wind Speed Distribution",
                        color_discrete_sequence=['#3498db'])
    fig6.update_layout(height=500)
    st.plotly_chart(fig6, use_container_width=True)
    
    # Chart 6 Insight
    avg_wind = filtered_df['windspeed'].mean()
    max_wind = filtered_df['windspeed'].max()
    wind_std = filtered_df['windspeed'].std()
    calm_days = len(filtered_df[filtered_df['windspeed'] < 5])
    windy_days = len(filtered_df[filtered_df['windspeed'] > 20])
    
    st.markdown(f"""
    <div class="weather-insight">
        <h4>💨 Chart Insights:</h4>
        <p>Wind speed distribution shows the frequency of different wind conditions. The average wind speed is <strong>{avg_wind:.1f} km/h</strong> with a maximum of <strong>{max_wind:.1f} km/h</strong>. There were <strong>{calm_days} calm days</strong> (wind speed < 5 km/h) and <strong>{windy_days} windy days</strong> (wind speed > 20 km/h). The standard deviation of <strong>{wind_std:.1f} km/h</strong> indicates moderate variability in wind conditions, which is important for understanding local weather patterns and their impact on comfort and activities.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chart 7: Cloud Cover Analysis
    st.markdown('<h2 class="sub-header">☁️ Chart 7: Cloud Cover Analysis</h2>', unsafe_allow_html=True)
    
    cloud_bins = pd.cut(filtered_df['cloudcover'], bins=[0, 25, 50, 75, 100], 
                        labels=['Clear', 'Partly Cloudy', 'Mostly Cloudy', 'Overcast'])
    cloud_counts = cloud_bins.value_counts()
    
    fig7 = px.pie(values=cloud_counts.values, names=cloud_counts.index,
                  title="Cloud Cover Distribution")
    fig7.update_layout(height=500)
    st.plotly_chart(fig7, use_container_width=True)
    
    # Chart 7 Insight
    most_common_cloud = cloud_counts.index[0]
    most_common_cloud_pct = (cloud_counts.values[0] / cloud_counts.sum()) * 100
    clear_days = cloud_counts.get('Clear', 0)
    overcast_days = cloud_counts.get('Overcast', 0)
    avg_cloud_cover = filtered_df['cloudcover'].mean()
    
    st.markdown(f"""
    <div class="weather-insight">
        <h4>☁️ Chart Insights:</h4>
        <p>Cloud cover analysis reveals sky condition patterns throughout the dataset. <strong>{most_common_cloud}</strong> conditions dominate, representing <strong>{most_common_cloud_pct:.1f}%</strong> of all observations. There were <strong>{clear_days} clear days</strong> and <strong>{overcast_days} completely overcast days</strong>. The average cloud cover is <strong>{avg_cloud_cover:.1f}%</strong>, indicating {'predominantly clear' if avg_cloud_cover < 25 else 'partly cloudy' if avg_cloud_cover < 50 else 'mostly cloudy' if avg_cloud_cover < 75 else 'heavily overcast'} conditions overall. This distribution affects solar radiation, temperature variations, and weather comfort levels.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chart 8: Temperature Range Analysis
    st.markdown('<h2 class="sub-header">📊 Chart 8: Daily Temperature Range by City</h2>', unsafe_allow_html=True)
    
    filtered_df['temp_range'] = filtered_df['tempmax'] - filtered_df['tempmin']
    
    fig8 = px.violin(filtered_df, x='City', y='temp_range',
                     title="Daily Temperature Range Distribution by City")
    fig8.update_xaxes(tickangle=45)
    fig8.update_layout(height=500)
    st.plotly_chart(fig8, use_container_width=True)
    
    # Chart 8 Insight
    city_temp_ranges = filtered_df.groupby('City')['temp_range'].agg(['mean', 'std', 'max']).round(1)
    highest_range_city = city_temp_ranges['mean'].idxmax()
    lowest_range_city = city_temp_ranges['mean'].idxmin()
    most_variable_range_city = city_temp_ranges['std'].idxmax()
    avg_temp_range = filtered_df['temp_range'].mean()
    
    st.markdown(f"""
    <div class="extreme-weather">
        <h4>📊 Chart Insights:</h4>
        <p>Daily temperature range analysis shows climate stability across cities. <strong>{highest_range_city}</strong> has the largest average daily temperature swing ({city_temp_ranges.loc[highest_range_city, 'mean']:.1f}°C), indicating more continental climate characteristics, while <strong>{lowest_range_city}</strong> shows the smallest range ({city_temp_ranges.loc[lowest_range_city, 'mean']:.1f}°C), suggesting more stable, maritime-influenced conditions. <strong>{most_variable_range_city}</strong> shows the most inconsistent daily ranges. The overall average daily range is <strong>{avg_temp_range:.1f}°C</strong>, reflecting typical diurnal temperature variations in the region.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chart 9: Feels Like vs Actual Temperature
    st.markdown('<h2 class="sub-header">🌡️ Chart 9: Feels Like vs Actual Temperature</h2>', unsafe_allow_html=True)
    
    fig9 = px.scatter(filtered_df, x='temp', y='feelslike', color='humidity',
                      title="Feels Like Temperature vs Actual Temperature",
                      color_continuous_scale='viridis')
    fig9.add_trace(go.Scatter(x=[filtered_df['temp'].min(), filtered_df['temp'].max()],
                              y=[filtered_df['temp'].min(), filtered_df['temp'].max()],
                              mode='lines', name='Perfect Match', line=dict(dash='dash')))
    fig9.update_layout(height=500)
    st.plotly_chart(fig9, use_container_width=True)
    
    # Chart 9 Insight
    temp_feelslike_diff = filtered_df['feelslike'] - filtered_df['temp']
    avg_difference = temp_feelslike_diff.mean()
    max_difference = temp_feelslike_diff.max()
    min_difference = temp_feelslike_diff.min()
    feels_hotter_days = len(filtered_df[filtered_df['feelslike'] > filtered_df['temp']])
    feels_cooler_days = len(filtered_df[filtered_df['feelslike'] < filtered_df['temp']])
    
    st.markdown(f"""
    <div class="insight-box">
        <h4>🌡️ Chart Insights:</h4>
        <p>The relationship between actual and perceived temperature reveals how humidity affects comfort. On average, it feels <strong>{abs(avg_difference):.1f}°C {'hotter' if avg_difference > 0 else 'cooler'}</strong> than the actual temperature. The maximum difference was <strong>{max_difference:.1f}°C hotter</strong> and <strong>{abs(min_difference):.1f}°C cooler</strong> than actual. There were <strong>{feels_hotter_days} days</strong> when it felt hotter and <strong>{feels_cooler_days} days</strong> when it felt cooler than actual temperature. The color intensity shows humidity levels - higher humidity typically makes temperatures feel hotter than they are.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chart 10: Weather Conditions Distribution
    st.markdown('<h2 class="sub-header">🌤️ Chart 10: Weather Conditions Distribution</h2>', unsafe_allow_html=True)
    
    conditions_count = filtered_df['conditions'].value_counts().head(10)
    
    fig10 = px.bar(x=conditions_count.values, y=conditions_count.index, orientation='h',
                   title="Top 10 Weather Conditions",
                   color=conditions_count.values, color_continuous_scale='viridis')
    fig10.update_layout(height=500)
    st.plotly_chart(fig10, use_container_width=True)
    
    # Chart 10 Insight
    most_common = conditions_count.index[0]
    most_common_count = conditions_count.values[0]
    total_observations = len(filtered_df)
    most_common_percentage = (most_common_count / total_observations) * 100
    conditions_variety = len(conditions_count)
    
    st.markdown(f"""
    <div class="extreme-weather">
        <h4>🌤️ Chart Insights:</h4>
        <p>Weather conditions analysis reveals the most frequent weather patterns in the dataset. <strong>"{most_common}"</strong> is the most common condition, occurring <strong>{most_common_count:,} times ({most_common_percentage:.1f}%)</strong> of all observations. The top 10 conditions represent the primary weather patterns experienced across the analyzed cities and time period. This diversity of <strong>{conditions_variety} different conditions</strong> shows the varied climatic experiences, helping understand typical weather expectations and planning for different scenarios.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chart 11: Pressure vs Temperature Correlation
    st.markdown('<h2 class="sub-header">📊 Chart 11: Sea Level Pressure vs Temperature</h2>', unsafe_allow_html=True)
    
    fig11 = px.scatter(filtered_df, x='sealevelpressure', y='temp', color='City',
                       title="Sea Level Pressure vs Temperature")
    fig11.update_layout(height=500)
    st.plotly_chart(fig11, use_container_width=True)
    
    # Chart 11 Insight
    pressure_temp_corr = filtered_df['sealevelpressure'].corr(filtered_df['temp'])
    avg_pressure = filtered_df['sealevelpressure'].mean()
    pressure_range = filtered_df['sealevelpressure'].max() - filtered_df['sealevelpressure'].min()
    high_pressure_days = len(filtered_df[filtered_df['sealevelpressure'] > avg_pressure + filtered_df['sealevelpressure'].std()])
    low_pressure_days = len(filtered_df[filtered_df['sealevelpressure'] < avg_pressure - filtered_df['sealevelpressure'].std()])
    
    st.markdown(f"""
    <div class="data-summary">
        <h4>📊 Chart Insights:</h4>
        <p>Sea level pressure and temperature relationship shows atmospheric dynamics. The correlation coefficient is <strong>{pressure_temp_corr:.3f}</strong>, indicating a {'strong' if abs(pressure_temp_corr) > 0.5 else 'moderate' if abs(pressure_temp_corr) > 0.3 else 'weak'} {'negative' if pressure_temp_corr < 0 else 'positive'} relationship. Average pressure is <strong>{avg_pressure:.1f} mb</strong> with a range of <strong>{pressure_range:.1f} mb</strong>. There were <strong>{high_pressure_days} high pressure days</strong> and <strong>{low_pressure_days} low pressure days</strong>, which typically correlate with different weather patterns and temperature stability.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chart 12: Visibility Analysis
    st.markdown('<h2 class="sub-header">👁️ Chart 12: Visibility Analysis</h2>', unsafe_allow_html=True)
    
    fig12 = px.histogram(filtered_df, x='visibility', nbins=25,
                         title="Visibility Distribution",
                         color_discrete_sequence=['green'])
    fig12.update_layout(height=500)
    st.plotly_chart(fig12, use_container_width=True)
    
    # Chart 12 Insight
    avg_visibility = filtered_df['visibility'].mean()
    max_visibility = filtered_df['visibility'].max()
    min_visibility = filtered_df['visibility'].min()
    good_visibility_days = len(filtered_df[filtered_df['visibility'] > 10])
    poor_visibility_days = len(filtered_df[filtered_df['visibility'] < 5])
    excellent_visibility_days = len(filtered_df[filtered_df['visibility'] >= 15])
    
    st.markdown(f"""
    <div class="weather-insight">
        <h4>👁️ Chart Insights:</h4>
        <p>Visibility analysis reveals air quality and atmospheric clarity patterns. Average visibility is <strong>{avg_visibility:.1f} km</strong>, ranging from <strong>{min_visibility:.1f} km</strong> to <strong>{max_visibility:.1f} km</strong>. There were <strong>{excellent_visibility_days} days</strong> with excellent visibility (≥15 km), <strong>{good_visibility_days} days</strong> with good visibility (>10 km), and <strong>{poor_visibility_days} days</strong> with poor visibility (<5 km). Good visibility indicates clear atmospheric conditions, while reduced visibility may suggest fog, pollution, or atmospheric haze affecting air quality and weather clarity.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chart 13: Correlation Matrix
    st.markdown('<h2 class="sub-header">🔗 Chart 13: Correlation Matrix</h2>', unsafe_allow_html=True)
    
    numeric_cols = ['tempmax', 'tempmin', 'temp', 'feelslike', 'humidity', 
                    'windspeed', 'sealevelpressure', 'cloudcover', 'visibility']
    corr_matrix = filtered_df[numeric_cols].corr()
    
    fig13, ax13 = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax13)
    ax13.set_title("Correlation Matrix of Weather Variables")
    st.pyplot(fig13)
    plt.close()
    
    # Chart 13 Insight
    strongest_positive_corr = corr_matrix.where(np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)).stack().max()
    strongest_negative_corr = corr_matrix.where(np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)).stack().min()
    strongest_pos_pair = corr_matrix.where(np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)).stack().idxmax()
    strongest_neg_pair = corr_matrix.where(np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)).stack().idxmin()
    
    st.markdown(f"""
    <div class="extreme-weather">
        <h4>🔗 Chart Insights:</h4>
        <p>The correlation matrix reveals relationships between weather variables. The strongest positive correlation is between <strong>{strongest_pos_pair[0]} and {strongest_pos_pair[1]}</strong> ({strongest_positive_corr:.3f}), indicating these variables tend to increase together. The strongest negative correlation is between <strong>{strongest_neg_pair[0]} and {strongest_neg_pair[1]}</strong> ({strongest_negative_corr:.3f}), showing they move in opposite directions. Colors represent correlation strength: red indicates positive relationships, blue shows negative correlations, and white represents no correlation. This matrix helps identify which weather factors influence each other.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chart 14: Time Series Analysis
    st.markdown('<h2 class="sub-header">📈 Chart 14: Time Series Temperature Analysis</h2>', unsafe_allow_html=True)
    
    # Daily average temperature over time
    daily_temp = filtered_df.groupby('Date')['temp'].mean().reset_index()
    
    fig14 = px.line(daily_temp, x='Date', y='temp',
                    title="Daily Average Temperature Over Time")
    fig14.update_layout(height=500)
    st.plotly_chart(fig14, use_container_width=True)
    
    # Chart 14 Insight
    temp_trend = daily_temp['temp'].diff().mean()
    max_temp_date = daily_temp.loc[daily_temp['temp'].idxmax(), 'Date'].strftime('%Y-%m-%d')
    min_temp_date = daily_temp.loc[daily_temp['temp'].idxmin(), 'Date'].strftime('%Y-%m-%d')
    max_daily_temp = daily_temp['temp'].max()
    min_daily_temp = daily_temp['temp'].min()
    seasonal_variation = daily_temp['temp'].std()
    
    st.markdown(f"""
    <div class="insight-box">
        <h4>📈 Chart Insights:</h4>
        <p>Time series analysis shows temperature evolution over the entire period. The daily trend shows {'a slight warming pattern' if temp_trend > 0.01 else 'a slight cooling pattern' if temp_trend < -0.01 else 'relatively stable temperatures'} over time. The hottest day was <strong>{max_temp_date}</strong> ({max_daily_temp:.1f}°C) and the coolest was <strong>{min_temp_date}</strong> ({min_daily_temp:.1f}°C). The temperature standard deviation of <strong>{seasonal_variation:.1f}°C</strong> indicates {'high' if seasonal_variation > 5 else 'moderate' if seasonal_variation > 3 else 'low'} seasonal variability. This time series helps identify long-term climate trends, seasonal cycles, and extreme weather events across the analyzed period.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chart 15: Sunburst Chart - Weather Patterns by City and Season
    st.markdown('<h2 class="sub-header">🌞 Chart 15: Weather Patterns Sunburst Visualization</h2>', unsafe_allow_html=True)
    
    # Prepare data for sunburst chart
    # Create season column
    filtered_df['Season'] = filtered_df['Month'].map({
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
    })
    
    # Create temperature categories
    temp_quantiles = filtered_df['temp'].quantile([0.25, 0.5, 0.75])
    filtered_df['Temp_Category'] = pd.cut(
        filtered_df['temp'], 
        bins=[-float('inf'), temp_quantiles[0.25], temp_quantiles[0.5], temp_quantiles[0.75], float('inf')],
        labels=['Cool', 'Moderate', 'Warm', 'Hot']
    )
    
    # Aggregate data for sunburst
    sunburst_data = filtered_df.groupby(['Season', 'City', 'Temp_Category']).agg({
        'temp': 'mean',
        'humidity': 'mean'
    }).reset_index()
    
    # Add count for sizing
    count_data = filtered_df.groupby(['Season', 'City', 'Temp_Category']).size().reset_index(name='Count')
    sunburst_data = sunburst_data.merge(count_data, on=['Season', 'City', 'Temp_Category'])
    
    # Create the sunburst chart
    fig15 = px.sunburst(
        sunburst_data,
        path=['Season', 'City', 'Temp_Category'],
        values='Count',
        color='temp',
        color_continuous_scale='RdYlBu_r',
        title="Weather Patterns: Season → City → Temperature Category",
        hover_data={'humidity': ':.1f', 'temp': ':.1f'},
        labels={'temp': 'Avg Temperature (°C)', 'humidity': 'Avg Humidity (%)'}
    )
    
    fig15.update_layout(
        height=700,
        width=None,  # Let it use full width
        font_size=14,
        title_font_size=18,
        margin=dict(t=50, b=20, l=20, r=20),
        showlegend=True
    )
    
    # Display the sunburst chart using full width
    st.plotly_chart(fig15, use_container_width=True)
    
    # Chart 15 Insight
    most_data_season = count_data.groupby('Season')['Count'].sum().idxmax()
    most_data_city = count_data.groupby('City')['Count'].sum().idxmax()
    most_common_temp_cat = count_data.groupby('Temp_Category')['Count'].sum().idxmax()
    total_combinations = len(sunburst_data)
    
    # Calculate seasonal averages
    seasonal_temps = filtered_df.groupby('Season')['temp'].mean()
    hottest_season = seasonal_temps.idxmax()
    coolest_season = seasonal_temps.idxmin()
    
    st.markdown(f"""
    <div class="data-summary">
        <h4>🌞 Chart Insights:</h4>
        <p>This interactive sunburst chart visualizes the hierarchical relationship between seasons, cities, and temperature categories. <strong>{most_data_season}</strong> has the most weather observations, while <strong>{most_data_city}</strong> contributes the most data points overall. The most common temperature category is <strong>{most_common_temp_cat}</strong> conditions. The chart reveals <strong>{total_combinations} unique combinations</strong> of season-city-temperature patterns. <strong>{hottest_season}</strong> shows the highest average temperatures ({seasonal_temps[hottest_season]:.1f}°C), while <strong>{coolest_season}</strong> is the coolest ({seasonal_temps[coolest_season]:.1f}°C). The color intensity represents temperature levels - red indicates hotter conditions, blue shows cooler temperatures. This multi-layered visualization helps understand how temperature patterns vary across seasons and cities simultaneously.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Additional Insights Section
    st.markdown('<h2 class="sub-header">💡 Comprehensive Weather Insights</h2>', unsafe_allow_html=True)
    
    # Create multiple insight boxes with different styling
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature Analysis Box
        hottest_city = filtered_df.loc[filtered_df['tempmax'].idxmax(), 'City']
        hottest_temp = filtered_df['tempmax'].max()
        coolest_temp = filtered_df['tempmin'].min()
        temp_range = hottest_temp - coolest_temp
        
        st.markdown(f"""
        <div class="insight-box">
            <h3>🌡️ Temperature Analysis</h3>
            <ul>
                <li><strong>Hottest City:</strong> {hottest_city}</li>
                <li><strong>Highest Temperature:</strong> {hottest_temp:.1f}°C</li>
                <li><strong>Lowest Temperature:</strong> {coolest_temp:.1f}°C</li>
                <li><strong>Temperature Range:</strong> {temp_range:.1f}°C</li>
                <li><strong>Average Summer Temp:</strong> {filtered_df['temp'].mean():.1f}°C</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Extreme Weather Events Box
        high_temp_days = len(filtered_df[filtered_df['tempmax'] > 40])
        high_humidity_days = len(filtered_df[filtered_df['humidity'] > 80])
        high_wind_days = len(filtered_df[filtered_df['windspeed'] > 30])
        
        st.markdown(f"""
        <div class="extreme-weather">
            <h3>⚠️ Extreme Weather Events</h3>
            <ul>
                <li><strong>Days > 40°C:</strong> {high_temp_days} days</li>
                <li><strong>High Humidity Days (>80%):</strong> {high_humidity_days} days</li>
                <li><strong>Windy Days (>30 km/h):</strong> {high_wind_days} days</li>
                <li><strong>Clear Sky Days:</strong> {len(filtered_df[filtered_df['cloudcover'] < 20])} days</li>
                <li><strong>Overcast Days:</strong> {len(filtered_df[filtered_df['cloudcover'] > 80])} days</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Weather Patterns Box
        most_common_condition = filtered_df['conditions'].mode().iloc[0]
        avg_humidity = filtered_df['humidity'].mean()
        avg_wind = filtered_df['windspeed'].mean()
        avg_pressure = filtered_df['sealevelpressure'].mean()
        avg_visibility = filtered_df['visibility'].mean()
        
        st.markdown(f"""
        <div class="weather-insight">
            <h3>🌤️ Weather Patterns</h3>
            <ul>
                <li><strong>Most Common Condition:</strong> {most_common_condition}</li>
                <li><strong>Average Humidity:</strong> {avg_humidity:.1f}%</li>
                <li><strong>Average Wind Speed:</strong> {avg_wind:.1f} km/h</li>
                <li><strong>Average Pressure:</strong> {avg_pressure:.1f} mb</li>
                <li><strong>Average Visibility:</strong> {avg_visibility:.1f} km</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # City Comparison Box
        city_temps = filtered_df.groupby('City')['temp'].mean().sort_values(ascending=False)
        top_3_hottest = city_temps.head(3)
        
        # Monthly insights
        monthly_avg = filtered_df.groupby('Month_Name')['temp'].mean()
        hottest_month = monthly_avg.idxmax()
        coolest_month = monthly_avg.idxmin()
        
        # Create the city rankings box with all content inside
        cities_list = ""
        for i, (city, temp) in enumerate(top_3_hottest.items()):
            cities_list += f"<li><strong>{city}:</strong> {temp:.1f}°C</li>"
        
        st.markdown(f"""
        <div class="data-summary">
            <h3>🏙️ City Rankings</h3>
            <h4>🔥 Hottest Cities:</h4>
            <ol>
                {cities_list}
            </ol>
    
        </div>
        """, unsafe_allow_html=True)
    
    # Project Conclusion Section
    st.markdown('<h2 class="sub-header">🎯 Project Conclusion</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box" style="background: linear-gradient(135deg, #e3f2fd 0%, #f8f9fa 50%, #fff3e0 100%); color: #2c3e50; padding: 1.5rem; margin: 1rem 0; border: 2px solid #81c784;">
        <p style="font-size: 1.2rem; line-height: 1.6; text-align: center; margin: 0;">
            <strong>This comprehensive analysis of Indian summer weather patterns (2007-2021) reveals significant regional temperature variations and climate relationships across multiple cities. The dashboard provides essential insights for urban planning, agriculture, and climate adaptation through 15 interactive visualizations that demonstrate India's diverse climatic conditions and their practical applications for sustainable development.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
