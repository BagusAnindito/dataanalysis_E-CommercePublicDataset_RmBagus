import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

#Dissable warning
st.set_option('deprecation.showPyplotGlobalUse', False)

#Title and introduction 
st.title('Proyek Analisis Data: E-Commerce Public Dataset 🌍')
st.write("Dasboard ini akan menampilkan data:")
st.write("1. Data pendapatan produk tiap State")
st.write("2. Tren pendapatan produk tiap State")
st.write("3. Korelasi antara jumlah order dan jumlah produk terjual terhadap State")

#Load data
data2 = pd.read_csv("rev_state.csv")
data3 = pd.read_csv("rev_prod.csv")
data1 = pd.read_csv("main_data.csv")

#Space
st.header("")

#All Function
#Function to plot bar chart
def plot_barchart(selected_option):
    if selected_option == "Top 5 Highest":
        plt.title("Top 5 Highest State Product Revenue ", fontsize=16)
        filtered_data = data2.head(5)
    elif selected_option == "Top 5 Lowest":
        plt.title("Top 5 Lowest State Product Revenue", fontsize=16)
        filtered_data = data2.tail(5)
    else:
        plt.title("All State Product Revenue ", fontsize=16)
        filtered_data = data2

    sns.barplot(data=filtered_data, x="State", y="Revenue", color="skyblue")
    plt.xlabel("State", fontsize=10)
    plt.ylabel("Revenue", fontsize=10)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    st.pyplot()

    return filtered_data
#Function to calculate revenue
def calculate_monthly_revenue(revenue_states, state_column, states=None):
    # Convert order_purchase_timestamp to datetime type
    revenue_states['order_purchase_timestamp'] = pd.to_datetime(revenue_states['order_purchase_timestamp'])

    # Filter DataFrame based on state
    if states:
        revenue_states = revenue_states[revenue_states[state_column].isin(states)]

    # Extract year and month from 'order_purchase_timestamp' column
    revenue_states['year'] = revenue_states['order_purchase_timestamp'].dt.year
    revenue_states['month'] = revenue_states['order_purchase_timestamp'].dt.month

    # Group by year, month, and state and sum revenue
    group_columns = ['year', 'month']
    if state_column in revenue_states.columns:
        group_columns.append(state_column)
    monthly_revenue = revenue_states.groupby(group_columns)['payment_value'].sum().reset_index()

    # Sort results
    monthly_revenue = monthly_revenue.sort_values(by=['customer_state', 'year', 'month']).reset_index(drop=True)

    # Create year-month column
    monthly_revenue['year_month'] = monthly_revenue['year'].astype(str) + '-' + monthly_revenue['month'].astype(str)
    monthly_revenue.columns = ['year', 'month', 'state', 'revenue', 'year_month']
    monthly_revenue = monthly_revenue[monthly_revenue['year_month'] != '2016-12']
    return monthly_revenue
# Function to calculate current revenue for the selected state
def calculate_current_revenue(selected_state):
    if selected_state == "All":
        return latest_revenue_SP, latest_revenue_RJ, latest_revenue_MG, latest_revenue_RS, latest_revenue_PR
    elif selected_state == "SP":
        return latest_revenue_SP
    elif selected_state == "RJ":
        return latest_revenue_RJ
    elif selected_state == "MG":
        return latest_revenue_MG
    elif selected_state == "RS":
        return latest_revenue_RS
    elif selected_state == "PR":
        return latest_revenue_PR
#function to plot line chart
def plot_linechart(state_data=None):
    print("State data:", state_data)  # Debug statement
    if state_data is not None:
        plt.figure(figsize=(15,9))
        sns.lineplot(data=state_data, x='year_month', y='revenue', marker='o', color='black', markerfacecolor='black', markersize=7, label=state_data['state'].unique()[0])
    else:
        print("State data is None")  # Debug statement
        plt.figure(figsize=(15,9))
        sns.lineplot(data=monthly_revenue_SP, x='year_month', y='revenue', marker='o', color='black', markerfacecolor='black', markersize=7, label='SP')
        sns.lineplot(data=monthly_revenue_RJ, x='year_month', y='revenue', marker='o', color='blue', markerfacecolor='blue', markersize=7, label='RJ')
        sns.lineplot(data=monthly_revenue_MG, x='year_month', y='revenue', marker='o', color='green', markerfacecolor='green', markersize=7, label='MG')
        sns.lineplot(data=monthly_revenue_RS, x='year_month', y='revenue', marker='o', color='red', markerfacecolor='red', markersize=7, label='RS')
        sns.lineplot(data=monthly_revenue_PR, x='year_month', y='revenue', marker='o', color='orange', markerfacecolor='orange', markersize=7, label='PR')

    # Adjusting labels and title
        plt.title('REVENUE TREND')
        plt.ylabel('REVENUE')
        plt.xlabel('YEAR-MONTH')
        plt.grid(True)

    # Adding legend
        plt.legend()

    # Adjust layout
        plt.tight_layout()

    # Show plot
        st.pyplot()
    
    return plt

#Sub-title
st.header("Data Pendapatan Produk Tiap State 📊")

#Display the "Data Pendapatan Produk Tiap State 📊"
r1c1, r1c2 = st.columns(2)
with r1c1:
    selected_option = st.selectbox(
        "Pilih Kriteria :", ["Top 5 Highest", "Top 5 Lowest", "All State"])
r2c1, r2c2 = st.columns([3,2])
if selected_option == "Top 5 Highest":
    top_5_revenue = data2.head()["Revenue"]
    for i, revenue in enumerate(top_5_revenue):
        column = r2c1 if i < 3 else r2c2  
        state_index = i if i < len(data2.State) else i - len(data2.State)
        column.metric(label=f"Total Revenue {data2.State[state_index]}", value="BRL " + str(revenue))
elif selected_option == "Top 5 Lowest":
    top_5_revenue = data2.tail()["Revenue"]
    for i, revenue in enumerate(top_5_revenue):
        column = r2c1 if i < 3 else r2c2 
        state_index = i if i < len(data2.State) else i - len(data2.State)
        column.metric(label=f"Total Revenue {data2.State[state_index]}", value="BRL " + str(revenue))
else:
    data2_indexed = data2.set_index('Revenue')
    data_with_state = data2_indexed.reset_index()[['State', 'Revenue']]
    revenue_data = {
        "1-10": data_with_state[data_with_state.index < 10], 
        "11-20": data_with_state[(data_with_state.index >= 10) & (data_with_state.index < 20)], 
        "21-27": data_with_state[data_with_state.index >= 20]
    }
    with r1c2:
        tabs = ["1-10", "11-20", "21-27"]
        selected_tab = st.selectbox("Pilih Urutan State ke- :", tabs)  

        if selected_tab == "1-10":
            top_10_revenue = data2["Revenue"].iloc[:10] 
            for i, revenue in enumerate(top_10_revenue):                
                column = r2c1 if i < 5 else r2c2 
                column.metric(label=f"Total Revenue {data2['State'].iloc[i]}", 
                              value="BRL " + str(revenue))
        elif selected_tab == "11-20":
            top_10_revenue = data2["Revenue"].iloc[10:20]  
            for i, revenue in enumerate(top_10_revenue):
                column = r2c1 if i < 5 else r2c2  
                column.metric(label=f"Total Revenue {data2['State'].iloc[i+10]}", 
                              value="BRL " + str(revenue))
        else:
            top_10_revenue = data2["Revenue"].iloc[20:]  
            for i, revenue in enumerate(top_10_revenue):
                column = r2c1 if i < 5 else r2c2 
                column.metric(label=f"Total Revenue {data2['State'].iloc[i+20]}", 
                              value="BRL " + str(revenue))
plot_barchart(selected_option)

#Space
st.header("")

#Sub-title
st.header("Tren Pendapatan Produk 5 State Tertinggi 📈")

#Display the "Tren Pendapatan Produk 5 State Tertinggi 📈"
r4c1, r4c2 = st.columns(2)
with r4c1:
    selected_option_2 = st.selectbox(
        "Pilih Kriteria :", ["All", "SP", "RJ", "MG", "RS", "PR"])
#Calculate monthly revenue per state
monthly_revenue_SP = calculate_monthly_revenue(data1, 'customer_state', states=['SP'])
monthly_revenue_RJ = calculate_monthly_revenue(data1, 'customer_state', states=['RJ'])
monthly_revenue_MG = calculate_monthly_revenue(data1, 'customer_state', states=['MG'])
monthly_revenue_RS = calculate_monthly_revenue(data1, 'customer_state', states=['RS'])
monthly_revenue_PR = calculate_monthly_revenue(data1, 'customer_state', states=['PR'])
#Get the latest revenue value for each state
latest_revenue_SP = monthly_revenue_SP.iloc[-1]['revenue']
latest_revenue_RJ = monthly_revenue_RJ.iloc[-1]['revenue']
latest_revenue_MG = monthly_revenue_MG.iloc[-1]['revenue']
latest_revenue_RS = monthly_revenue_RS.iloc[-1]['revenue']
latest_revenue_PR = monthly_revenue_PR.iloc[-1]['revenue']
#Get the previous revenue value for each state
previous_month_revenue_SP = monthly_revenue_SP.iloc[-2]['revenue']
previous_month_revenue_RJ = monthly_revenue_RJ.iloc[-2]['revenue']
previous_month_revenue_MG = monthly_revenue_MG.iloc[-2]['revenue']
previous_month_revenue_RS = monthly_revenue_RS.iloc[-2]['revenue']
previous_month_revenue_PR = monthly_revenue_PR.iloc[-2]['revenue']
#Calculate difference revenue
delta_revenue_SP = latest_revenue_SP - previous_month_revenue_SP
delta_revenue_RJ = latest_revenue_RJ - previous_month_revenue_RJ
delta_revenue_MG = latest_revenue_MG - previous_month_revenue_MG
delta_revenue_RS = latest_revenue_RS - previous_month_revenue_RS
delta_revenue_PR = latest_revenue_PR - previous_month_revenue_PR
#Display current revenue metrics
if selected_option_2 == "All":
    r5c1, r5c2 = st.columns(2)
    with r5c1:
        st.write(
            """
            <style>
            [data-testid="stMetricDelta"] svg {
                display:none;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        revenue_SP, revenue_RJ, revenue_MG, revenue_RS, revenue_PR = calculate_current_revenue(selected_option_2)
        st.metric(label=f"Current Revenue SP", value="BRL " + str(revenue_SP), delta=f"↑ BRL {delta_revenue_SP:.2f}")
        st.metric(label=f"Current Revenue RJ", value="BRL " + str(revenue_RJ), delta=f"↓ BRL {delta_revenue_RJ:.2f}", delta_color="inverse")
        st.metric(label=f"Current Revenue MG", value="BRL " + str(revenue_MG), delta=f"↑ BRL {delta_revenue_MG:.2f}")
    with r5c2:
        st.write("")
        st.metric(label=f"Current Revenue RS", value="BRL " + str(revenue_RS), delta=f"↑ BRL {delta_revenue_RS:.2f}")
        st.metric(label=f"Current Revenue PR", value="BRL " + str(revenue_PR), delta=f"↓ BRL {delta_revenue_PR:.2f}", delta_color="inverse")
elif selected_option_2 == "SP":
    r5c1, r5c2 = st.columns(2)
    with r5c1:
        st.write(
            """
            <style>
            [data-testid="stMetricDelta"] svg {
                display:none;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        revenue_SP = calculate_current_revenue(selected_option_2)
        st.metric(label=f"Current Revenue SP", 
                  value="BRL " + str(revenue_SP), 
                  delta=f"↑ BRL {delta_revenue_SP:.2f}")
elif selected_option_2 == "RJ":
    r5c1, r5c2 = st.columns(2)
    with r5c1:
        st.write(
            """
            <style>
            [data-testid="stMetricDelta"] svg {
                display:none;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        revenue_RJ = calculate_current_revenue(selected_option_2)
        st.metric(label=f"Current Revenue RJ", 
                  value="BRL " + str(revenue_RJ), 
                  delta=f"↓ BRL {delta_revenue_RJ:.2f}", 
                  delta_color="inverse")
elif selected_option_2 == "MG":
    r5c1, r5c2 = st.columns(2)
    with r5c1:
        st.write(
            """
            <style>
            [data-testid="stMetricDelta"] svg {
                display:none;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        revenue_MG = calculate_current_revenue(selected_option_2)
        st.metric(label=f"Current Revenue MG", 
                  value="BRL " + str(revenue_MG), 
                  delta=f"↑ BRL {delta_revenue_MG:.2f}")
elif selected_option_2 == "RS":
    r5c1, r5c2 = st.columns(2)
    with r5c1:
        st.write(
            """
            <style>
            [data-testid="stMetricDelta"] svg {
                display:none;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        revenue_RS = calculate_current_revenue(selected_option_2)
        st.metric(label=f"Current Revenue RS", 
                  value="BRL " + str(revenue_RS), 
                  delta=f"↑ BRL {delta_revenue_RS:.2f}")
elif selected_option_2 == "PR":
    r5c1, r5c2 = st.columns(2)
    with r5c1:
        st.write(
            """
            <style>
            [data-testid="stMetricDelta"] svg {
                display:none;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        revenue_PR = calculate_current_revenue(selected_option_2)
        st.metric(label=f"Current Revenue PR", 
                  value="BRL " + str(revenue_PR), 
                  delta=f"↓ BRL {delta_revenue_PR:.2f}", delta_color="inverse")

#Plot the line chart based on selection
if selected_option_2 == "All":
    line_chart = plot_linechart()
elif selected_option_2 == "SP":
    line_chart = plot_linechart(monthly_revenue_SP)
    st.pyplot(line_chart)
elif selected_option_2 == "RJ":
    line_chart = plot_linechart(monthly_revenue_RJ)
    st.pyplot(line_chart)
elif selected_option_2 == "MG":
    line_chart = plot_linechart(monthly_revenue_MG)
    st.pyplot(line_chart)
elif selected_option_2 == "RS":
    line_chart = plot_linechart(monthly_revenue_RS)
    st.pyplot(line_chart)
elif selected_option_2 == "PR":
    line_chart = plot_linechart(monthly_revenue_PR)
    st.pyplot(line_chart)

#Space
st.header("")

#Sub-title
st.header("Korelasi antara Jumlah Order dan Jumlah Produk Terjual Terhadap State 🔎")

#Group data for product revenue info
grouped_data = data3.groupby('customer_state').agg(
    num_orders=pd.NamedAgg(column='order_id', aggfunc='nunique'),
    num_products=pd.NamedAgg(column='product_id', aggfunc='nunique')
).reset_index()
#Filtering using DataFrame.loc[]
top_5_states = ['SP', 'RJ', 'MG', 'RS', 'PR']
group_of_top_5_states = grouped_data.loc[grouped_data['customer_state'].isin(top_5_states)].reset_index(drop=True)
# Calculate the correlation coefficient
num_orders = group_of_top_5_states.loc[:, 'num_orders']
num_products = group_of_top_5_states.loc[:, 'num_products']
correlation_matrix = np.corrcoef(num_products, num_orders)
correlation_top_5_states = correlation_matrix[0, 1]
#Display data and correlation coefficient
st.table(group_of_top_5_states)
st.write("Correlation:", correlation_top_5_states)

#Create a scatter plot + correlation
plt.figure(figsize=(13, 6))
sns.scatterplot(data=group_of_top_5_states, x='num_products', y='num_orders', hue='customer_state')
sns.regplot(data=group_of_top_5_states, x='num_products', y='num_orders', scatter=False, color='blue', line_kws={"linewidth": 1})
plt.title('Correlation between Number of Orders and Total Products Sold for Top 5 States')
plt.xlabel('Total Products Sold')
plt.ylabel('Number of Orders')
plt.legend(title='State')
plt.text(10000, 26500, f'Correlation: {correlation_top_5_states:.3f}', fontsize=9, color='blue')
st.pyplot(plt)

st.caption("© Rm Bagus Anindito Satrio Utomo / m312d4ky2879")
