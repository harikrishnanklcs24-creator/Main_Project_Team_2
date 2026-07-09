"""
Netlify Serverless Function - Project Classifier Classification API
"""

import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import google.generativeai as genai
except ImportError:
    print("Warning: google-generativeai not installed")


def classify(event, context):
    """
    Handle project classification requests
    Netlify Functions wrapper
    """
    try:
        # Handle preflight requests
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type',
                },
                'body': ''
            }

        if event['httpMethod'] != 'POST':
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Method not allowed'})
            }

        body = json.loads(event['body'])
        api_key = body.get('api_key', '').strip()
        project_name = body.get('project_name', '').strip()
        project_description = body.get('project_description', '').strip()

        # Validation
        if not api_key:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'status': 'error', 'error': 'API key is required'})
            }

        if not project_name:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'status': 'error', 'error': 'Project name is required'})
            }

        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        # Create prompt
        prompt = f"""
        Analyze the following project and provide a comprehensive analysis:
        
        Project Name: {project_name}
        Project Description: {project_description if project_description else "No description provided"}
        
        Please provide:
        1. **Project Type Classification** (e.g., Web App, Mobile App, API, Desktop App, etc.)
        2. **Technology Stack Recommendations**
        3. **Architecture Recommendations**
        4. **Step-by-step Build Plan**
        5. **Deployment Considerations**
        6. **Time Estimate for Development**
        7. **Potential Challenges & Solutions**
        8. **Key Features to Prioritize**
        
        Format your response clearly with headers and bullet points.
        """

        # Generate content
        response = model.generate_content(prompt)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'status': 'success',
                'project_name': project_name,
                'classification': response.text
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 'error', 'error': str(e)})
        }