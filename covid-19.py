# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Set display options for better output readability
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def load_covid_data():
    """Load COVID-19 data from Our World in Data."""
    print("Loading data... This might take a few moments.")
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    
    try:
        df = pd.read_csv(url)
        df['date'] = pd.to_datetime(df['date'])
        print("Data loaded successfully!")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def get_available_countries(df):
    """Get list of available countries in the dataset."""
    return sorted(df['location'].unique())

def clean_data(df):
    """Clean the dataset by handling missing values."""
    # Remove rows with missing crucial values
    crucial_columns = ['total_cases', 'total_deaths']
    df_cleaned = df.dropna(subset=crucial_columns, how='all')
    
    # Fill remaining NA values with 0
    df_cleaned = df_cleaned.fillna(0)
    
    return df_cleaned

def get_country_data(df, country):
    """Get data for a specific country."""
    return df[df['location'] == country].copy()

def plot_covid_trends(df, country):
    """Create plots for COVID-19 trends in a country."""
    country_data = get_country_data(df, country)
    
    if len(country_data) == 0:
        print(f"No data found for {country}")
        return
    
    # Create a figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot 1: Total Cases and Deaths
    ax1.plot(country_data['date'], country_data['total_cases'], 
            label='Total Cases', color='blue')
    ax1.plot(country_data['date'], country_data['total_deaths'], 
            label='Total Deaths', color='red')
    ax1.set_title(f'COVID-19 Total Cases and Deaths in {country}')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Count')
    ax1.legend()
    ax1.grid(True)
    ax1.tick_params(axis='x', rotation=45)
    
    # Plot 2: Daily New Cases and Deaths
    ax2.bar(country_data['date'], country_data['new_cases'], 
           label='New Cases', alpha=0.5, color='blue')
    ax2.bar(country_data['date'], country_data['new_deaths'], 
           label='New Deaths', alpha=0.5, color='red')
    ax2.set_title(f'COVID-19 Daily New Cases and Deaths in {country}')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Count')
    ax2.legend()
    ax2.grid(True)
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()

def display_country_stats(df, country):
    """Display key statistics for a country."""
    country_data = get_country_data(df, country)
    
    if len(country_data) == 0:
        print(f"No data found for {country}")
        return
    
    latest_data = country_data.iloc[-1]
    
    print(f"\n=== COVID-19 Statistics for {country} ===")
    print(f"Last updated: {latest_data['date'].strftime('%Y-%m-%d')}")
    print(f"Total Cases: {int(latest_data['total_cases']):,}")
    print(f"Total Deaths: {int(latest_data['total_deaths']):,}")
    
    if latest_data['total_vaccinations'] > 0:
        print(f"Total Vaccinations: {int(latest_data['total_vaccinations']):,}")
    
    if latest_data['total_cases'] > 0:
        death_rate = (latest_data['total_deaths'] / latest_data['total_cases']) * 100
        print(f"Case Fatality Rate: {death_rate:.2f}%")

def main():
    """Main function to run the COVID-19 tracker."""
    # Load the data
    df = load_covid_data()
    
    if df is None:
        return
    
    # Clean the data
    df_cleaned = clean_data(df)
    
    while True:
        print("\n=== COVID-19 Data Tracker ===")
        print("1. View data for a specific country")
        print("2. List available countries")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            country = input("\nEnter country name: ")
            if country in df_cleaned['location'].values:
                display_country_stats(df_cleaned, country)
                plot_covid_trends(df_cleaned, country)
            else:
                print(f"\nCountry '{country}' not found. Please check the available countries list.")
                
        elif choice == '2':
            countries = get_available_countries(df_cleaned)
            print("\nAvailable countries:")
            for i, country in enumerate(countries, 1):
                print(f"{i}. {country}")
            
        elif choice == '3':
            print("\nThank you for using the COVID-19 Data Tracker!")
            break
            
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
