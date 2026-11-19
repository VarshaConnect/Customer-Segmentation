# Customer Segmentation Project

## 1. Project Overview

The Customer Segmentation Project focuses on dividing customers into different groups based on their demographic information and purchasing behavior.

This project uses Python and Machine Learning techniques, particularly the K-Means Clustering algorithm, to identify customer segments and understand their characteristics.

An interactive dashboard is developed using Streamlit to visualize customer demographics, purchasing patterns, customer preferences and business insights.

## 2. Project Objectives

- Segment customers based on their behavior and demographic information.
- Apply K-Means clustering using Scikit-learn.
- Analyze customer purchasing patterns and spending habits.
- Understand customer preferences and shopping channels.
- Visualize customer segments through interactive charts.
- Generate targeted marketing recommendations for different customer groups.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations and sample data generation |
| Scikit-learn | Machine Learning and K-Means clustering |
| Streamlit | Interactive dashboard development |
| Plotly | Interactive data visualization |

## 4. Dataset Description

The project uses a synthetically generated dataset containing 1,000 customer records.

The dataset includes the following attributes:

- Customer ID
- Gender
- Age
- Annual Income
- Purchase Frequency
- Average Order Value
- Total Spending
- Days Since Last Purchase
- Preferred Category
- Shopping Channel

The dataset is generated using Python and NumPy for educational and demonstration purposes.

## 5. Project Features

### Customer Overview
Displays key customer metrics, including total customers, average age, average annual income and total customer spending.

### Customer Segmentation
Uses the K-Means clustering algorithm to group customers based on selected demographic and purchasing behavior features.

### Demographic Analysis
Visualizes customer age distribution and gender information.

### Purchase Behavior Analysis
Analyzes purchase frequency and average spending across different customer segments.

### Customer Cluster Visualization
Displays the relationship between annual income and total customer spending using a scatter plot.

### Customer Preferences
Analyzes preferred product categories and shopping channels across customer segments.

### Customer Segment Characteristics
Provides a comparison of customer groups based on average age, income, purchase frequency, order value, spending and days since last purchase.

### Targeted Marketing Recommendations
Provides marketing suggestions for different customer segments, including loyalty rewards, repeat-purchase offers, re-engagement campaigns and budget-friendly promotions.

### Automated Business Insights
Highlights important findings, including:
- Highest-spending customer segment.
- Most frequent shoppers.
- Largest customer group.
- Segment with the longest average time since purchase.

### Customer Details and Report Download
Displays customer records and allows users to download the filtered customer segmentation report in CSV format.

### Interactive Dashboard Filters
Allows users to filter customer records by:
- Gender
- Preferred Category
- Shopping Channel

Users can also select the number of customer segments between 2 and 8.

## 6. Machine Learning Methodology

The project uses the **K-Means Clustering Algorithm**, an unsupervised machine learning technique.

The clustering process involves:

1. Selecting relevant customer features.
2. Standardizing numerical data using StandardScaler.
3. Applying the K-Means clustering algorithm.
4. Grouping customers into the selected number of clusters.
5. Analyzing the characteristics of each cluster.
6. Assigning meaningful descriptive names based on cluster profiles.

The numerical features used for clustering are:

- Age
- Annual Income
- Purchase Frequency
- Average Order Value
- Days Since Last Purchase

The number of clusters can be adjusted through the dashboard.

## 7. Customer Segments

The dashboard assigns descriptive names to customer groups based on their characteristics:

- **High-Value Customers:** Customers with the highest average spending.
- **Frequent Shoppers:** Customers with the highest average purchase frequency among the remaining groups.
- **At-Risk Customers:** Customers with the longest average time since their last purchase among the remaining groups.
- **Budget-Conscious Customers:** Customers with the lowest average income among the remaining groups.
- **Other Customer Groups:** Additional clusters that do not receive one of the above labels.

## 8. Project Structure

```text
Customer-Segmentation/
│
├── app.py
├── data.py
├── customer_data.csv
├── requirements.txt
└── README.md
```

## 9. Installation and Execution

Follow these steps to run the project locally.

### Step 1: Install Required Libraries

Open the terminal in the project folder and execute:

```bash
pip install -r requirements.txt
```

### Step 2: Generate the Customer Dataset

Run the following command:

```bash
python data.py
```

This generates the `customer_data.csv` file containing 1,000 customer records.

### Step 3: Run the Streamlit Application

Execute:

```bash
streamlit run app.py
```

### Step 4: Open the Dashboard

Open the local URL displayed in the terminal to access the Customer Segmentation Dashboard.

## 10. Expected Outcome

The project provides practical experience in:

- Customer analytics and segmentation.
- Data preprocessing and analysis.
- Machine Learning and clustering.
- Customer purchasing behavior analysis.
- Interactive data visualization.
- Business insights and interpretation.
- Targeted marketing recommendations.

## 11. Conclusion

The Customer Segmentation Project demonstrates how data analytics and machine learning can be used to understand customer characteristics and purchasing behavior.

By grouping customers into meaningful segments and visualizing their patterns through an interactive dashboard, businesses can better understand different customer groups and develop targeted marketing strategies.

The project combines Python, Machine Learning, data analysis and visualization to demonstrate the practical application of customer analytics.

## 12. Disclaimer

This project uses synthetically generated sample customer data. The results are intended for educational and demonstration purposes and do not represent actual customer purchasing records.