import streamlit as st
import pandas as pd
import json
import os
from json_utils import load_json_file, json_to_dataframe, get_json_structure, validate_json_format
from data_analyzer import JSONDataAnalyzer
from visualizer import JSONVisualizer
import plotly.graph_objects as go
import tempfile


# Set page configuration
st.set_page_config(
    page_title="JSON Data Analyzer & Visualizer",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for professional styling with dark mode support
st.markdown("""
<style>
    /* Light mode styles */
    @media (prefers-color-scheme: light) {
        :root {
            --header-color: #1f3a5f;
            --subheader-color: #2c5282;
            --section-color: #2d3748;
            --text-color: #2d3748;
            --bg-color: #ffffff;
            --card-bg: #f7fafc;
            --border-color: #e2e8f0;
            --info-bg: #ebf8ff;
            --info-border: #4299e1;
            --warning-bg: #fffbeb;
            --warning-border: #f6ad55;
            --success-bg: #f0fff4;
            --success-border: #48bb78;
            --error-bg: #fed7d7;
            --error-border: #e53e3e;
            --metric-value: #2b6cb0;
            --metric-label: #4a5568;
            --sidebar-bg: #ffffff;
            --sidebar-text: #2d3748;
        }
    }
    
    /* Dark mode styles */
    @media (prefers-color-scheme: dark) {
        :root {
            --header-color: #90cdf4;
            --subheader-color: #63b3ed;
            --section-color: #e2e8f0;
            --text-color: #e2e8f0;
            --bg-color: #1a202c;
            --card-bg: #2d3748;
            --border-color: #4a5568;
            --info-bg: #2b6cb0;
            --info-border: #4299e1;
            --warning-bg: #975a16;
            --warning-border: #f6ad55;
            --success-bg: #38a169;
            --success-border: #48bb78;
            --error-bg: #c53030;
            --error-border: #e53e3e;
            --metric-value: #90cdf4;
            --metric-label: #cbd5e0;
            --sidebar-bg: #2d3748;
            --sidebar-text: #e2e8f0;
        }
        
        .stDataFrame {
            color: #e2e8f0 !important;
        }
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--header-color);
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem 0;
    }
    
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--subheader-color);
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid var(--border-color);
        padding-bottom: 0.5rem;
    }
    
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--section-color);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background-color: var(--card-bg);
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
        height: 100%;
        border: 1px solid var(--border-color);
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--metric-value);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--metric-label);
        margin-top: 0.5rem;
    }
    
    .info-box {
        background-color: var(--info-bg);
        border-left: 4px solid var(--info-border);
        padding: 1rem;
        border-radius: 0 4px 4px 0;
        margin: 1rem 0;
        color: var(--text-color);
    }
    
    .warning-box {
        background-color: var(--warning-bg);
        border-left: 4px solid var(--warning-border);
        padding: 1rem;
        border-radius: 0 4px 4px 0;
        margin: 1rem 0;
        color: var(--text-color);
    }
    
    .success-box {
        background-color: var(--success-bg);
        border-left: 4px solid var(--success-border);
        padding: 1rem;
        border-radius: 0 4px 4px 0;
        margin: 1rem 0;
        color: var(--text-color);
    }
    
    .error-box {
        background-color: var(--error-bg);
        border-left: 4px solid var(--error-border);
        padding: 1rem;
        border-radius: 0 4px 4px 0;
        margin: 1rem 0;
        color: var(--text-color);
    }
    
    .solution-box {
        background-color: var(--info-bg);
        border-left: 4px solid var(--success-border);
        padding: 1rem;
        border-radius: 0 4px 4px 0;
        margin: 1rem 0;
        color: var(--text-color);
    }
    
    .stDataFrame {
        border: 1px solid var(--border-color);
        border-radius: 4px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        padding: 0.5rem;
        background-color: var(--card-bg);
        border-radius: 8px;
        border: 1px solid var(--border-color);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: var(--border-color);
        border-radius: 4px;
        padding: 0.5rem 1rem;
        color: var(--text-color);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--info-border);
        color: white;
    }
    
    .sidebar-content {
        padding: 1rem;
        background-color: var(--sidebar-bg);
        color: var(--sidebar-text);
        height: 100%;
    }
    
    .sidebar-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--subheader-color);
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .sidebar-item {
        margin-bottom: 0.75rem;
        font-size: 0.95rem;
        line-height: 1.4;
        color: var(--sidebar-text);
    }
    
    /* Fix for code elements in dark mode */
    code {
        background-color: var(--card-bg);
        color: var(--text-color);
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
    }
    
    /* Ensure text is visible in all modes */
    .stMarkdown, .stText {
        color: var(--text-color);
    }
    
    .problem-title {
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--error-border);
    }
    
    .solution-title {
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--success-border);
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">📊 JSON Data Analyzer & Visualizer</h1>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; max-width: 800px; margin: 0 auto 2rem auto; font-size: 1.1rem;">
    A professional tool for comprehensive analysis and visualization of JSON data files up to 24MB in size. 
    Upload your JSON file to explore its structure, analyze statistics, and create interactive visualizations.
</div>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Choose a JSON file (max 24MB)", type="json")

if uploaded_file is not None:
    # Create a temporary file to store the uploaded content
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        temp_file_path = tmp_file.name
    
    try:
        # Validate JSON format
        if not validate_json_format(temp_file_path):
            st.markdown('<div class="error-box">Invalid JSON format. Please upload a valid JSON file.</div>', unsafe_allow_html=True)
            st.markdown('<div class="solution-box"><div class="solution-title">How to fix JSON format issues:</div><ul><li>Ensure your file contains valid JSON syntax</li><li>Check for missing commas, brackets, or quotes</li><li>Use a JSON validator to identify syntax errors</li><li>Ensure the file encoding is UTF-8</li></ul></div>', unsafe_allow_html=True)
        else:
            # Load JSON data
            json_data = load_json_file(temp_file_path)
            
            # Display basic information
            st.markdown('<h2 class="sub-header">File Information</h2>', unsafe_allow_html=True)
            file_size = os.path.getsize(temp_file_path)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="info-box"><strong>File name:</strong> {uploaded_file.name}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="info-box"><strong>File size:</strong> {file_size / (1024*1024):.2f} MB</div>', unsafe_allow_html=True)
            
            # Display JSON structure
            st.markdown('<h2 class="sub-header">Data Structure</h2>', unsafe_allow_html=True)
            with st.expander("View JSON structure details", expanded=False):
                structure = get_json_structure(json_data)
                st.json(structure)
            
            # Convert to DataFrame
            try:
                df = json_to_dataframe(json_data)
                
                # Display data preview
                st.markdown('<h2 class="sub-header">Data Preview</h2>', unsafe_allow_html=True)
                st.dataframe(df.head(10), width='stretch')
                
                # Initialize analyzer and visualizer
                analyzer = JSONDataAnalyzer(json_data)
                visualizer = JSONVisualizer(df)
                
                # Display basic info
                info = analyzer.get_basic_info()
                st.markdown('<h2 class="sub-header">Dataset Overview</h2>', unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-value">{info['shape'][0]}</div>
                        <div class="metric-label">ROWS</div>
                    </div>
                    ''', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-value">{info['shape'][1]}</div>
                        <div class="metric-label">COLUMNS</div>
                    </div>
                    ''', unsafe_allow_html=True)
                with col3:
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-value">{len(info['numeric_columns'])}</div>
                        <div class="metric-label">NUMERIC COLS</div>
                    </div>
                    ''', unsafe_allow_html=True)
                with col4:
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-value">{len(info['categorical_columns'])}</div>
                        <div class="metric-label">CATEGORY COLS</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Summary statistics
                st.markdown('<h2 class="sub-header">Statistical Summary</h2>', unsafe_allow_html=True)
                summary_stats = analyzer.get_summary_statistics()
                if not summary_stats.empty:
                    st.dataframe(summary_stats, width='stretch')
                else:
                    st.markdown('<div class="warning-box">No numeric columns found for summary statistics.</div>', unsafe_allow_html=True)
                
                # Missing data
                st.markdown('<h2 class="sub-header">Missing Data Analysis</h2>', unsafe_allow_html=True)
                missing_data = analyzer.get_missing_data_info()
                if not missing_data.empty:
                    st.dataframe(missing_data, width='stretch')
                else:
                    st.markdown('<div class="success-box">No missing data found in the dataset.</div>', unsafe_allow_html=True)
                
                # Visualization section
                st.markdown('<h2 class="sub-header">Data Visualization</h2>', unsafe_allow_html=True)
                
                # Get column lists
                numeric_columns = analyzer.numeric_columns
                categorical_columns = analyzer.categorical_columns
                
                # Tabs for different visualizations
                tab1, tab2, tab3, tab4 = st.tabs(["📊 Histograms", "📊 Bar Charts", "📊 Scatter Plots", "📊 Correlation"])
                
                with tab1:
                    if numeric_columns:
                        selected_col = st.selectbox("Select a numeric column for histogram", numeric_columns, key="hist")
                        if st.button("Generate Histogram", key="hist_btn"):
                            try:
                                fig = visualizer.create_histogram(selected_col)
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception as e:
                                st.markdown(f'<div class="error-box">Error generating histogram: {str(e)}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="warning-box">No numeric columns available for histograms.</div>', unsafe_allow_html=True)
                
                with tab2:
                    if categorical_columns:
                        selected_col = st.selectbox("Select a categorical column for bar chart", categorical_columns, key="bar")
                        if st.button("Generate Bar Chart", key="bar_btn"):
                            try:
                                fig = visualizer.create_bar_chart(selected_col)
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception as e:
                                st.markdown(f'<div class="error-box">Error generating bar chart: {str(e)}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="warning-box">No categorical columns available for bar charts.</div>', unsafe_allow_html=True)
                
                with tab3:
                    if len(numeric_columns) >= 2:
                        col1, col2 = st.columns(2)
                        x_col = col1.selectbox("X-axis", numeric_columns, key="scatter_x")
                        y_col = col2.selectbox("Y-axis", [col for col in numeric_columns if col != x_col], key="scatter_y")
                        
                        color_col = st.selectbox("Color (optional)", [None] + categorical_columns + numeric_columns, key="scatter_color")
                        if color_col == "None":
                            color_col = None
                        
                        if st.button("Generate Scatter Plot", key="scatter_btn"):
                            try:
                                if color_col:
                                    fig = visualizer.create_scatter_plot(x_col, y_col, color_col)
                                else:
                                    fig = visualizer.create_scatter_plot(x_col, y_col)
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception as e:
                                st.markdown(f'<div class="error-box">Error generating scatter plot: {str(e)}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="warning-box">Need at least 2 numeric columns for scatter plots.</div>', unsafe_allow_html=True)
                
                with tab4:
                    if len(numeric_columns) >= 2:
                        if st.button("Generate Correlation Heatmap", key="corr_btn"):
                            try:
                                fig = visualizer.create_correlation_heatmap()
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception as e:
                                st.markdown(f'<div class="error-box">Error generating correlation heatmap: {str(e)}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="warning-box">Need at least 2 numeric columns for correlation analysis.</div>', unsafe_allow_html=True)
                
                # Show full dataset
                st.markdown('<h2 class="sub-header">Complete Dataset</h2>', unsafe_allow_html=True)
                st.dataframe(df, width='stretch')
                
            except Exception as e:
                st.markdown(f'<div class="error-box"><div class="problem-title">Data Processing Error:</div>{str(e)}</div>', unsafe_allow_html=True)
                
                # Provide specific solutions based on error type
                error_msg = str(e).lower()
                if "arrow" in error_msg and "serialization" in error_msg:
                    st.markdown('''
                    <div class="solution-box">
                        <div class="solution-title">How to resolve DataFrame serialization issues:</div>
                        <ul>
                            <li><strong>Complex data types:</strong> Your JSON contains complex nested structures or mixed data types that are difficult to represent in a tabular format</li>
                            <li><strong>Unsupported objects:</strong> Some columns contain objects (like lists or dictionaries) that cannot be directly displayed in a table</li>
                            <li><strong>Solutions:</strong>
                                <ul>
                                    <li>Try flattening your JSON structure before uploading</li>
                                    <li>Convert complex objects to strings before analysis</li>
                                    <li>Use the "Raw JSON Data" view below to see your data structure</li>
                                    <li>Consider preprocessing your data to simplify nested structures</li>
                                </ul>
                            </li>
                        </ul>
                    </div>
                    ''', unsafe_allow_html=True)
                elif "unhashable type" in error_msg:
                    st.markdown('''
                    <div class="solution-box">
                        <div class="solution-title">How to resolve unhashable type issues:</div>
                        <ul>
                            <li><strong>Lists in data:</strong> Your JSON contains arrays or lists as values, which cannot be used for categorical analysis</li>
                            <li><strong>Nested objects:</strong> Complex nested structures may cause processing issues</li>
                            <li><strong>Solutions:</strong>
                                <ul>
                                    <li>Flatten nested arrays into separate columns</li>
                                    <li>Convert lists to comma-separated strings</li>
                                    <li>Extract specific elements from arrays for analysis</li>
                                </ul>
                            </li>
                        </ul>
                    </div>
                    ''', unsafe_allow_html=True)
                elif "expected bytes" in error_msg:
                    st.markdown('''
                    <div class="solution-box">
                        <div class="solution-title">How to resolve data type conflicts:</div>
                        <ul>
                            <li><strong>Mixed data types:</strong> Some columns contain different data types (e.g., numbers and strings)</li>
                            <li><strong>Encoding issues:</strong> Special characters or encoding problems in your data</li>
                            <li><strong>Solutions:</strong>
                                <ul>
                                    <li>Ensure consistent data types in each column</li>
                                    <li>Check for special characters or encoding issues</li>
                                    <li>Preprocess data to standardize formats</li>
                                </ul>
                            </li>
                        </ul>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown('''
                    <div class="solution-box">
                        <div class="solution-title">General troubleshooting steps:</div>
                        <ul>
                            <li><strong>Check data structure:</strong> Review your JSON structure using the "Data Structure" section above</li>
                            <li><strong>Simplify complexity:</strong> Flatten nested structures if possible</li>
                            <li><strong>Validate data types:</strong> Ensure consistent data types in arrays and objects</li>
                            <li><strong>Reduce file size:</strong> If the file is very large, try with a smaller sample</li>
                            <li><strong>Contact support:</strong> If issues persist, please share the error details with the development team</li>
                        </ul>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Still show the raw JSON structure
                st.markdown('<h3 class="section-header">Raw JSON Data</h3>', unsafe_allow_html=True)
                st.json(json_data)
            
    except Exception as e:
        st.markdown(f'<div class="error-box"><div class="problem-title">File Processing Error:</div>{str(e)}</div>', unsafe_allow_html=True)
        st.markdown('''
        <div class="solution-box">
            <div class="solution-title">How to resolve file processing issues:</div>
            <ul>
                <li><strong>File format:</strong> Ensure your file is in valid JSON format</li>
                <li><strong>File size:</strong> Check that your file is under 24MB</li>
                <li><strong>Encoding:</strong> Make sure the file is saved with UTF-8 encoding</li>
                <li><strong>Permissions:</strong> Ensure the file is not open in another application</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
else:
    st.markdown('<div class="info-box" style="text-align: center; padding: 2rem;">Please upload a JSON file to begin analysis.</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Sample Data</h2>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">To get started, you can use the sample data provided in <code>sample_data.json</code> in this directory.</div>', unsafe_allow_html=True)

# Sidebar with instructions
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown('<h3 class="sidebar-header">📘 How to Use</h3>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">1. Upload a JSON file (max 24MB)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">2. Explore the data structure</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">3. View summary statistics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">4. Create visualizations</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">5. Analyze missing data</div>', unsafe_allow_html=True)
    
    st.markdown('<h3 class="sidebar-header">📁 Supported JSON Formats</h3>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">• Flat JSON objects</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">• Nested JSON structures</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">• JSON arrays</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">• Mixed data types</div>', unsafe_allow_html=True)
    
    st.markdown('<h3 class="sidebar-header">📏 File Limitations</h3>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">• Maximum file size: 24MB</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">• Valid JSON format required</div>', unsafe_allow_html=True)
    
    st.markdown('<h3 class="sidebar-header">⚠️ Common Issues & Solutions</h3>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item"><strong>Data Processing Errors:</strong> Flatten complex nested structures</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item"><strong>Format Errors:</strong> Validate JSON syntax</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item"><strong>Size Errors:</strong> Reduce file size or split data</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)