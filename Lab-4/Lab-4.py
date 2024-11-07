import os
import pandas as pd

def read_files(directory):
    data = []
    for file in os.listdir(directory):
        if file.endswith('.csv') and file != 'product_names.csv':
            path = os.path.join(directory, file)
            df = pd.read_csv(path)
            data.append(df)
    if not data:
        raise ValueError("No CSV files found in the specified directory.")
    return pd.concat(data, ignore_index=True)

def sum_sales(data):
    return data.groupby('Product ID')['Quantity sold'].sum().reset_index(name='Total Quantity Sold')

def average_sales(sales, data):
    data['Date'] = pd.to_datetime(data['Date'])
    data['Month-Year'] = data['Date'].dt.to_period('M')
    monthly_sales = data.groupby(['Product ID', 'Month-Year'])['Quantity sold'].sum().reset_index()
    monthly_avg_sales = monthly_sales.groupby('Product ID')['Quantity sold'].mean().reset_index(name='Average Sold Per Month')
    return sales.merge(monthly_avg_sales, on='Product ID')

def top_products(sales):
    return sales.sort_values(by='Total Quantity Sold', ascending=False).head(5)

def add_names(sales, product_file):
    names = pd.read_csv(product_file)
    return sales.merge(names, on='Product ID')

def save_summary(final_data, output_file):
    final_data.to_csv(output_file, index=False)

def main():
    directory = 'Lab-4'
    product_file = os.path.join(directory, 'product_names.csv')
    output_file = os.path.join(directory, 'sales_summary.csv')
    
    try:
        data = read_files(directory)
        
        sales = sum_sales(data)
        
        sales = average_sales(sales, data)
        
        top_sales = top_products(sales)
        
        final_data = add_names(top_sales, product_file)
        
        save_summary(final_data, output_file)
        
        print("Sales summary saved successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
