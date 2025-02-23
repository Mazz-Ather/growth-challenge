import streamlit as st
import pandas as pd
import os
from io import BytesIO
import plotly.express as px

# 

# Setup
st.set_page_config(page_title="InsightFlow", layout='wide')

# Title section with gradient effect
st.markdown("""
    <style>
    .gradient-text {
        background: linear-gradient(45deg, #FFD700, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 42px;
        font-weight: bold;
        text-align: center;
    }
    .subtitle {
        font-size: 20px;
        color: #6c757d;
        text-align: center;
        margin-bottom: 20px;
    }
    .feature-card {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
    .icon-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
# loader
    .loader {
        border: 16px solid #f3f3f3;
        border-radius: 50%;
        border-top: 16px solid #3498db;
        width: 120px;
        height: 120px;
        animation: spin 2s linear infinite;
        margin: auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
  
    </style>
    """, unsafe_allow_html=True)

# Main title with gradient
st.markdown('<h1 class="gradient-text">📊 InsightFlow</h1>', unsafe_allow_html=True)
st.markdown('<p  class="subtitle">Your all-in-one platform for data transformation, cleaning, and interactive visualization</p>', unsafe_allow_html=True)

# Animated divider
st.markdown("""
    <div style='text-align: center; margin: 20px 0;'>
        ⚡️ ━━━━━━━━━━━━━━━━━━━━ ⚡️
    </div>
""", unsafe_allow_html=True)

# What is InsightFlow section
st.header('🎯 What is InsightFlow?')
st.write("""
InsightFlow is a powerful data management tool designed to streamline your data workflow. Whether you're 
analyzing Excel sheets or CSV files, our platform helps you transform raw data into actionable insights.
""")

# Feature cards in columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card" style='color : black'>
        <div class="icon-title">🔄 Data Transformation</div>
        <ul>
        <li>Convert between CSV and Excel formats</li>
        <li>Batch processing capabilities</li>
        <li>Preserve data integrity</li>
        </ul>
    </div>
    
    <div class="feature-card" style='color : black'>
        <div class="icon-title">🧹 Data Cleaning</div>
        <ul>
        <li>Advanced outlier detection</li>
        <li>Missing value handling</li>
        <li>Duplicate removal</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card" style='color : black'>
        <div class="icon-title">📈 Visualization</div>
        <ul>
        <li>Interactive charts and graphs</li>
        <li>Multiple visualization types</li>
        <li>Customizable appearances</li>
        </ul>
    </div>
    
    <div class="feature-card" style='color : black ; hover: scale-110'>
        <div class="icon-title">💾 Export Options</div>
        <ul>
        <li>Multiple export formats</li>
        <li>Customizable output</li>
        <li>Batch export capability</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Get Started section
st.markdown("""
    <div style='text-align: center; margin: 30px 0;'>
        <h2>🚀 Ready to Transform Your Data?</h2>
        <p style='font-size: 18px; color: #666;'>
            Simply upload your files below and let InsightFlow handle the complexity while you focus on what matters most - understanding your data.
        </p>
    </div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type {file_ext}")
            continue

        # Display file info
        st.write(f"**File Name:** {file.name}")
        st.write(f"File Size: {file.size/1024:.2f} KB")

        # Show preview of the DataFrame
        st.write("Preview the head of the DataFrame")
        st.dataframe(df.head())

        # Find and Replace Section
        st.subheader("Find and Replace")
        if st.checkbox(f"Show Find and Replace for {file.name}"):
            # Get all column names
            all_columns = df.columns.tolist()
            
            # Select the column (category) to perform find and replace
            selected_column = st.selectbox("Select Column to Replace Values:", all_columns)
            
            if selected_column:
                # Get unique values from the selected column
                unique_values = df[selected_column].unique().tolist()
                
                # Dropdown to select value to replace
                value_to_replace = st.selectbox("Select Value to Replace:", unique_values)
                
                # Text input for new value
                new_value = st.text_input("Enter New Value:", value_to_replace)
                
                # Replace button
                if st.button("Replace Values"):
                    df[selected_column] = df[selected_column].replace(value_to_replace, new_value)
                    st.success(f"Replaced '{value_to_replace}' with '{new_value}' in column '{selected_column}'")
                    # Show updated preview
                    st.write("Updated DataFrame Preview:")
                    st.dataframe(df.head())

        # Options for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing values have been filled")

            st.subheader("Select Columns to Convert")
            columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=list(df.columns))
            df = df[columns]

        # Create some visualizations
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            numeric_data = df.select_dtypes(include="number")
            if numeric_data.empty:
                st.write("No numeric data available for visualization.")
            else:
                # Let user select plot type
                with st.spinner('Creating visualization...'):
                    plot_type = st.selectbox(
                    "Select Plot Type",
                    ["Bar Plot", "Scatter Plot", "Line Plot", "Box Plot", "Histogram"]
            )
                
            if plot_type == "Histogram":
                    # For histogram, we only need one column
                    x_axis = st.selectbox("Select Column for Histogram", numeric_data.columns)
                    fig = px.histogram(df, x=x_axis, title=f'Histogram of {x_axis}')
                
            elif plot_type == "Box Plot":
                    y_axis = st.selectbox("Select Column for Box Plot", numeric_data.columns)
                    # Optional: Allow grouping by a categorical column
                    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
                    if not categorical_cols.empty:
                        x_axis = st.selectbox("Select Category for Grouping (optional)", 
                                            ['None'] + list(categorical_cols))
                        if x_axis == 'None':
                            fig = px.box(df, y=y_axis, title=f'Box Plot of {y_axis}')
                        else:
                            fig = px.box(df, x=x_axis, y=y_axis, 
                                       title=f'Box Plot of {y_axis} by {x_axis}')
                    else:
                        fig = px.box(df, y=y_axis, title=f'Box Plot of {y_axis}')
                
            else:
                    # For other plots, we need both x and y axes
                    x_axis = st.selectbox("Select X-axis", numeric_data.columns)
                    y_axis = st.selectbox("Select Y-axis", numeric_data.columns)
                    
                    if plot_type == "Bar Plot":
                        fig = px.bar(df, x=x_axis, y=y_axis, 
                                   title=f'{y_axis} vs {x_axis}')
                    elif plot_type == "Scatter Plot":
                        fig = px.scatter(df, x=x_axis, y=y_axis, 
                                       title=f'{y_axis} vs {x_axis}')
                    elif plot_type == "Line Plot":
                        fig = px.line(df, x=x_axis, y=y_axis, 
                                    title=f'{y_axis} vs {x_axis}')

                # Add common layout settings
            fig.update_layout(
                    xaxis_title=x_axis if 'x_axis' in locals() else "",
                    yaxis_title=y_axis if 'y_axis' in locals() else "",
                    height=500,
                    showlegend=True
                )

                # Add optional customization features
                # with st.expander("Customize Plot"):
                #     col1, col2 = st.columns(2)
                #     with col1:
                #         title = st.text_input("Plot Title", fig.layout.title.text)
                #         fig.update_layout(title=title)
                #     with col2:
                #         theme = st.selectbox("Color Theme", 
                #                            ["plotly", "plotly_white", "plotly_dark", 
                #                             "ggplot2", "seaborn"])
                #         fig.update_layout(template=theme)

                # Display the plot
            st.plotly_chart(fig, use_container_width=True)

        # Conversion Options
        st.subheader("Download Converted File")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
            st.success("All files processed!")

# navigation
st.sidebar.success('Select a page above')