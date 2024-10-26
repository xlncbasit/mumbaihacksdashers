import anthropic
import pandas as pd
import json
from pdf2image import convert_from_path
import base64
import io
from PIL import Image

# Initialize Claude client
client = anthropic.Anthropic(
    api_key=''  # Should be stored in environment variable
)

def convert_pdf_to_base64(pdf_path):
    """Convert PDF to images and encode first page as base64"""
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path)
        if not images:
            raise Exception("No pages found in PDF")
        
        # Take first page and convert to base64
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        return base64.b64encode(img_byte_arr).decode('utf-8')
    except Exception as e:
        print(f"Error converting PDF: {e}")
        return None

def process_evaluation_with_claude(file_path):
    # Read CSV headers
    df = pd.read_csv('trend mapping.csv', skiprows=1)
    headers = df.columns.tolist()
    
    if not file_path.lower().endswith('.pdf'):
        print("Only PDF files are supported")
        return None
    
    # Convert PDF to base64
    base64_image = convert_pdf_to_base64(file_path)
    if not base64_image:
        return None
        
    prompt = f"""Analyze this employee evaluation form.

Using these form fields:
{json.dumps(headers, indent=2)}

Please extract:
1. Employee ID and Name
2. Review Month and Year
3. Ratings for all evaluation criteria in both Employee Review Form and Self Review Form sections
4. Convert text ratings to numerical scores (0-1 scale) where:
   - Exceeds expectations = 1.0
   - Meets expectations = 0.75
   - Needs improvement = 0.4
   - Unacceptable = 0.0

Return the results as a CSV row matching exactly these columns: {','.join(headers)}
Include only the CSV row, no other text.
"""
    # Create message with converted PDF image
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": base64_image
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]

    try:
        # Get Claude's analysis
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0,
            messages=messages
        )

        # Extract CSV row from Claude's response
        csv_row = response.content[0].text.strip()
        # Convert CSV string to dictionary
        values = csv_row.split(',')
        row_dict = dict(zip(headers, values))
        return row_dict
    except Exception as e:
        print(f"Error processing with Claude: {e}")
        return None

def write_to_csv(row_dict):
    try:
        # Read existing CSV file
        df = pd.read_csv('trend mapping.csv')
        
        # Append new row
        df = pd.concat([df, pd.DataFrame([row_dict])], ignore_index=True)
        
        # Write back to CSV
        df.to_csv('trend mapping.csv', index=False)
        return True
    except Exception as e:
        print(f"Error writing to CSV: {e}")
        return False

def process_form_document(file_path):
    # Process with Claude
    row_dict = process_evaluation_with_claude(file_path)
    if not row_dict:
        return False
        
    # Write to CSV
    success = write_to_csv(row_dict)
    return success

if __name__ == "__main__":
    # Example usage
    form_file = "EmployeeEvaluationForm(1).pdf"
    if process_form_document(form_file):
        print("Form processed and written to CSV successfully!")
    else:
        print("Error processing form")