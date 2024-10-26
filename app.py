from flask import Flask, request,jsonify
import numpy as np
from statistics import mode
from flask_cors import CORS,  cross_origin 
import pandas as pd  # Add this import
import requests
import anthropic
import os
from flask import jsonify, request
import io
import logging

# Initialize Claude client
client = anthropic.Anthropic(api_key='api-key')

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST','GET'])
@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def process_data():
    try:
        # Initialize Anthropic client
        client = anthropic.Anthropic()
        
        # Read the input CSV file
        df = pd.read_csv('employee_tasks_dataset.csv')
        
        # Create the prompt
        prompt = f"""
Please analyze the following CSV data and reorganize the tasks based on similarity. 
Group similar tasks together and update the GroupNumber column accordingly.
Return only the modified CSV data without any additional explanation.

Here is the CSV data:
{df.to_csv(index=False)}
"""

        # Create message for Claude
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        # Get Claude's response
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4000,  # Increased token limit to handle larger CSV
            temperature=0,
            messages=messages
        )

        # Extract CSV content from Claude's response
        csv_content = response.content[0].text.strip()
        
        # Convert CSV string back to DataFrame
        updated_df = pd.read_csv(io.StringIO(csv_content))
        
        # Save the updated DataFrame to a new CSV file
        output_filename = 'updated_employee_tasks.csv'
        updated_df.to_csv(output_filename, index=False)
        
        return jsonify({
            'status': 'success',
            'message': 'CSV file updated successfully',
            'data': updated_df.to_dict('records'),
            'filename': output_filename
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error processing data: {str(e)}'
        }), 500

@app.route('/grouping', methods=['POST','GET'])
@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def grouping():
    try:
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
       
        # Read the CSV file
        logger.info("Reading input CSV file...")
        with open("employee_tasks_dataset.csv", 'r') as file:
            csv_content = file.read()
        
        # Prepare the message for Claude
        system_prompt = """Analyze the following CSV data of employee performance.
        Identify struggling employees based on:
        1. Task quality scores below 0.3
        2. Multiple incomplete tasks
        3. Consistently poor performance in specific task types
        
        Return the analysis in two separate CSV formats:
        1. Struggling employees with their performance issues
        2. High-performing employees (scores > 0.8)
        
        Include additional columns for performance categorization."""
        
        # Create the message
        message = f"{system_prompt}\n\nHere's the CSV data:\n{csv_content}"
        
        # Call Claude API
        logger.info("Calling Claude API for analysis...")
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4096,
            temperature=0,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        
        # Extract CSV data from response
        logger.info("Processing Claude's response...")
        response_content = response.content[0].text
        
        # Function to extract CSV content between specific markers
        def extract_csv_content(text: str, start_marker: str, end_marker: str) -> str:
            start_idx = text.find(start_marker)
            end_idx = text.find(end_marker, start_idx)
            if start_idx == -1 or end_idx == -1:
                raise ValueError(f"Couldn't find CSV content between {start_marker} and {end_marker}")
            return text[start_idx:end_idx].strip()
        
        # Extract both CSVs from response
        struggling_csv = extract_csv_content(
            response_content,
            "EmployeeId,ManagerId,Task,Completed,GroupNumber,Time_taken,task_quality_score,Performance_Issue",
            "EmployeeId,ManagerId,Task,Completed,GroupNumber,Time_taken,task_quality_score,Performance_Level"
        )
        # Convert to DataFrames
        struggling_df = pd.read_csv(pd.StringIO(struggling_csv))
        
        # Save to CSV files
        output_dir = "performance_analysis"
        os.makedirs(output_dir, exist_ok=True)
        
        struggling_path = os.path.join(output_dir, "struggling_employees.csv")
        high_performers_path = os.path.join(output_dir, "high_performers.csv")
        
        struggling_df.to_csv(struggling_path, index=False)
        
        logger.info(f"Analysis complete. Files saved in {output_dir}/")
        
        return struggling_df
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise
           
@app.route('/task-complete', methods=['POST','GET'])
@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def task_complete():
    input_value = request.json['input']
    print("Input value")
    print(input_value)
    # Read the CSV file
    df = pd.read_csv('employee_tasks_dataset.csv')
    # Update a column based on a condition in another column
    df.loc[df['EmployeeId'] == input_value, 'Completed'] = 'Task Completed'
    df.loc[df['EmployeeId'] == input_value, 'Time_taken'] = 'Task Completed'
    df.loc[df['EmployeeId'] == input_value, 'task_quality_score'] = 'Task Completed'
    # Save the updated DataFrame back to the CSV
    df.to_csv('employee_tasks_dataset.csv', index=False)
    print("Task completed")
    response = requests.post('http://localhost:5000/process', json={'input': input_value})
    print("Response from /process:", response.json())
    return jsonify("Task completed")

@app.route('/task-assign', methods=['POST','GET'])
@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def task_assign():
    input_value = request.json['input']
    print("Input value")
    print(input_value)
    # Read the CSV file
    df = pd.read_csv('employee_tasks_dataset.csv')
    # Update a column based on a condition in another column
    df.loc[df['EmployeeId'] == input_value, 'Task'] = 'Task Completed'
    df.loc[df['EmployeeId'] == input_value, 'Manager'] = 'Task Completed'
    # Save the updated DataFrame back to the CSV
    df.to_csv('employee_tasks_dataset.csv', index=False)
    print("Task Assigned")

    response = requests.post('http://localhost:5000/grouping', json={'input': input_value})
    print("Response from /grouping:", response.json())
    return jsonify("Task Assigned")

# Upload form functionality remain
@app.route('/upload-form', methods=['POST','GET'])
@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def upload_form():
    return jsonify("Form uploaded")

if __name__ == '__main__':
    app.run(debug=True)
