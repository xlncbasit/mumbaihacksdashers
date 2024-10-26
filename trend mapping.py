import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def analyze_employee_trends(employee_id):
    """
    Analyzes and plots performance trends for a specific employee.
    
    Parameters:
    employee_id (str): The ID of the employee to analyze
    """
    # Read the CSV file
    try:
        df = pd.read_csv('employee_reviewstrend.csv')
    except FileNotFoundError:
        print("Error: employee_reviewstrend.csv not found.")
        return
    
    # Filter data for the specific employee and create a copy
    emp_data = df[df['Employee ID'] == employee_id].copy()
    
    if emp_data.empty:
        print(f"No data found for Employee ID: {employee_id}")
        return
    
    # Create datetime for proper time series plotting using loc
    emp_data.loc[:, 'Review Date'] = pd.to_datetime(emp_data['Review Month'] + ' ' + emp_data['Review Year'].astype(str))
    emp_data = emp_data.sort_values('Review Date')

    
    # Get employee name for plot titles
    employee_name = emp_data['Employee Name'].iloc[0]
    
    # Set the style using seaborn
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle(f'Performance Trends for {employee_name} ({employee_id})', fontsize=16)
    
    # 1. Overall Ratings Trend
    ax1 = plt.subplot(2, 2, 1)
    sns.lineplot(data=emp_data, x='Review Date', y='Overall rating', marker='o', label='Manager Rating', ax=ax1)
    sns.lineplot(data=emp_data, x='Review Date', y='Overall rating.1', marker='o', label='Self Rating', ax=ax1)
    ax1.set_title('Overall Ratings Trend')
    ax1.set_xlabel('Review Date')
    ax1.set_ylabel('Rating')
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    # 2. Key Performance Metrics
    ax2 = plt.subplot(2, 2, 2)
    metrics = ['Quality of Work', 'Communication Skills', 'Initiative & Flexibility', 'Knowledge of Position']
    for metric in metrics:
        sns.lineplot(data=emp_data, x='Review Date', y=metric, marker='o', label=metric, ax=ax2)
    ax2.set_title('Key Performance Metrics (Manager Rating)')
    ax2.set_xlabel('Review Date')
    ax2.set_ylabel('Rating')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    # 3. Radar Chart
    ax3 = plt.subplot(2, 2, 3, projection='polar')
    latest_review = emp_data.iloc[-1]
    categories = ['Quality of Work', 'Attendance', 'Reliability', 
                 'Communication', 'Judgment', 'Initiative',
                 'Teamwork', 'Knowledge', 'Training']
    
    # Get scores
    manager_scores = [latest_review['Quality of Work'],
                     latest_review['Attendance & Punctuality'],
                     latest_review['Reliability/Dependability'],
                     latest_review['Communication Skills'],
                     latest_review['Judgment & Decision-Making'],
                     latest_review['Initiative & Flexibility'],
                     latest_review['Cooperation & Teamwork'],
                     latest_review['Knowledge of Position'],
                     latest_review['Training & Development']]
    
    self_scores = [latest_review['Quality of Work.1'],
                  latest_review['Attendance & Punctuality.1'],
                  latest_review['Reliability/Dependability.1'],
                  latest_review['Communication Skills.1'],
                  latest_review['Judgment & Decision-Making.1'],
                  latest_review['Initiative & Flexibility.1'],
                  latest_review['Cooperation & Teamwork.1'],
                  latest_review['Knowledge of Position.1'],
                  latest_review['Training & Development.1']]
    
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))
    manager_scores = np.concatenate((manager_scores, [manager_scores[0]]))
    self_scores = np.concatenate((self_scores, [self_scores[0]]))
    
    ax3.plot(angles, manager_scores, 'b-', label='Manager Rating', marker='o')
    ax3.plot(angles, self_scores, 'r-', label='Self Rating', marker='o')
    ax3.set_xticks(angles[:-1])
    ax3.set_xticklabels(categories, size=8)
    ax3.set_title('Latest Review Comparison')
    ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 4. Rating Differences
    ax4 = plt.subplot(2, 2, 4)
    differences = emp_data['Overall rating'] - emp_data['Overall rating.1']
    sns.barplot(x=emp_data['Review Date'], y=differences, ax=ax4)
    ax4.axhline(y=0, color='r', linestyle='-', alpha=0.3)
    ax4.set_title('Rating Differences (Manager - Self)')
    ax4.set_xlabel('Review Date')
    ax4.set_ylabel('Difference')
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Print summary statistics
    print(f"\nPerformance Summary for {employee_name}")
    print("-" * 50)
    print(f"Number of Reviews: {len(emp_data)}")
    print(f"Average Manager Rating: {emp_data['Overall rating'].mean():.2f}")
    print(f"Average Self Rating: {emp_data['Overall rating.1'].mean():.2f}")
    print(f"Highest Manager Rating: {emp_data['Overall rating'].max():.2f}")
    print(f"Lowest Manager Rating: {emp_data['Overall rating'].min():.2f}")
    
    if len(emp_data) > 1:
        print("\nTrend Analysis:")
        print("-" * 50)
        overall_trend = emp_data['Overall rating'].iloc[-1] - emp_data['Overall rating'].iloc[0]
        trend_direction = "improved" if overall_trend > 0 else "declined" if overall_trend < 0 else "remained stable"
        print(f"Overall performance has {trend_direction} by {abs(overall_trend):.2f} points")
        
        # Identify top improving and declining areas
        metrics = [col for col in emp_data.columns if col not in ['Employee ID', 'Employee Name', 'Review Month', 'Review Year', 'Review Date', 'Overall rating', 'Overall rating.1'] 
                  and not col.endswith('.1')]
        changes = {metric: emp_data[metric].iloc[-1] - emp_data[metric].iloc[0] for metric in metrics}
        top_improvement = max(changes.items(), key=lambda x: x[1])
        top_decline = min(changes.items(), key=lambda x: x[1])
        
        print(f"Most improved area: {top_improvement[0]} ({top_improvement[1]:.2f} points)")
        print(f"Most declined area: {top_decline[0]} ({top_decline[1]:.2f} points)")
    
    plt.show()

def list_employees():
    """Lists all available employees in the dataset."""
    try:
        df = pd.read_csv('employee_reviewstrend.csv')
        unique_employees = df[['Employee ID', 'Employee Name']].drop_duplicates()
        print("\nAvailable Employees:")
        print("-" * 50)
        for _, row in unique_employees.iterrows():
            print(f"{row['Employee ID']}: {row['Employee Name']}")
    except FileNotFoundError:
        print("Error: employee_reviews.csv not found.")
        return None
    return unique_employees

# Usage example
if __name__ == "__main__":
    # List all employees
    employees = list_employees()
    if employees is not None:
        # Get employee ID from user
        employee_id = input("\nEnter Employee ID to analyze: ")
        # Generate analysis
        analyze_employee_trends(employee_id)