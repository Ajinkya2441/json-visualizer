# JSON Data Analyzer & Visualizer

A professional tool for analyzing and visualizing JSON data files up to 24MB in size. This application provides comprehensive insights into your JSON data through interactive visualizations and detailed statistical analysis with a modern, clean user interface.

## Features

- **File Size Validation**: Supports JSON files up to 24MB
- **Data Structure Analysis**: Understand the structure of complex JSON data
- **Statistical Summary**: Get detailed statistics for numeric data
- **Missing Data Analysis**: Identify missing values in your dataset
- **Interactive Visualizations**:
  - Histograms for numeric distributions
  - Bar charts for categorical data
  - Scatter plots for relationship analysis
  - Correlation heatmaps
- **Professional UI**: Clean, modern interface with professional styling
- **Dark Mode Support**: Automatic adaptation to system theme preferences
- **Error Handling**: Detailed error messages with solutions
- **Data Export**: View and export full dataset

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser to the URL provided (typically http://localhost:8501)

3. Upload a JSON file (max 24MB)

4. Explore your data through:
   - Data structure analysis
   - Statistical summaries
   - Interactive visualizations
   - Missing data reports

## Supported JSON Formats

- Flat JSON objects
- Nested JSON structures
- JSON arrays
- Mixed data types

## Sample Data

A sample JSON file ([sample_data.json](file:///c:/Users/Ajinkya/Desktop/csv_visualization/sample_data.json)) is included to help you get started with testing the application.

## Requirements

- Python 3.7+
- pandas >= 1.5.0
- plotly >= 5.0.0
- streamlit >= 1.0.0
- jsonschema >= 4.0.0

## Core Modules

- [app.py](file:///c:/Users/Ajinkya/Desktop/csv_visualization/app.py): Main Streamlit application with professional UI
- [json_utils.py](file:///c:/Users/Ajinkya/Desktop/csv_visualization/json_utils.py): JSON loading and validation utilities
- [data_analyzer.py](file:///c:/Users/Ajinkya/Desktop/csv_visualization/data_analyzer.py): Data analysis functionality
- [visualizer.py](file:///c:/Users/Ajinkya/Desktop/csv_visualization/visualizer.py): Data visualization components
- [sample_data.json](file:///c:/Users/Ajinkya/Desktop/csv_visualization/sample_data.json): Sample JSON data for testing

## Professional UI Features

The application features a professionally designed interface with:

- **Custom CSS Styling**: Professional color scheme and typography
- **Metric Cards**: Visually appealing display of key statistics
- **Information Boxes**: Color-coded notifications for different message types
- **Tabbed Navigation**: Organized visualization options
- **Responsive Layout**: Adapts to different screen sizes
- **Dark Mode Support**: Automatic adaptation to system theme preferences

## Error Handling

When issues occur, the application provides:

- **Clear Error Messages**: Specific information about what went wrong
- **Actionable Solutions**: Step-by-step guidance on how to fix problems
- **Context-Specific Help**: Solutions tailored to the type of error encountered
- **Raw Data View**: Access to original data when processing fails

## File Size Limitations

- **Maximum file size**: 24MB
- **Valid JSON format required**
- **Larger files may require more processing time**

## License

This project is open source and available under the MIT License.