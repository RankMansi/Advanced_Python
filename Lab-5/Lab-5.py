import os
import json

# Function to read all JSON files in the given directory and its subdirectories
def read_json_files(directory):
    data = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                with open(os.path.join(root, file), 'r') as json_file:
                    data.append(json.load(json_file))
    return data

# Function to calculate statistics for each country
def calculate_statistics(covid_data):
    summary = {}
    for entry in covid_data:
        country = entry["country"]
        confirmed = entry["confirmed_cases"]["total"]
        deaths = entry["deaths"]["total"]
        recovered = entry["recovered"]["total"]
        active_cases = confirmed - deaths - recovered
        
        if country not in summary:
            summary[country] = {
                "total_confirmed": 0,
                "total_deaths": 0,
                "total_recovered": 0,
                "total_active": 0
            }
        
        summary[country]["total_confirmed"] += confirmed
        summary[country]["total_deaths"] += deaths
        summary[country]["total_recovered"] += recovered
        summary[country]["total_active"] += active_cases
    
    return summary

# Function to get top 5 countries by confirmed cases
def get_top_5_countries(summary, lowest=False):
    sorted_countries = sorted(summary.items(), key=lambda x: x[1]["total_confirmed"], reverse=not lowest)
    return sorted_countries[:5]

# Function to save summary report to a JSON file
def save_summary_to_json(summary, filename="covid19_summary.json"):
    with open(filename, 'w') as json_file:
        json.dump(summary, json_file, indent=4)

# Main function
def main():
    # Specify the directory containing the JSON files
    data_directory = 'covid_data/'
    
    # Step 1: Read all JSON files
    covid_data = read_json_files(data_directory)
    
    # Step 2: Calculate statistics for each country
    summary = calculate_statistics(covid_data)
    
    # Step 3: Determine top 5 countries with highest and lowest confirmed cases
    top_5_highest = get_top_5_countries(summary)
    top_5_lowest = get_top_5_countries(summary, lowest=True)
    
    print("Top 5 countries with the highest confirmed cases:")
    for country, stats in top_5_highest:
        print(f"{country}: {stats['total_confirmed']} confirmed cases")
    
    print("\nTop 5 countries with the lowest confirmed cases:")
    for country, stats in top_5_lowest:
        print(f"{country}: {stats['total_confirmed']} confirmed cases")
    
    # Step 4: Save summary report to JSON file
    save_summary_to_json(summary)

if __name__ == "__main__":
    main()
