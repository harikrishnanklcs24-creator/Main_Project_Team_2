"""
Netlify Serverless Function - Follow-up Questions API
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


def followup(event, context):
    """
    Handle follow-up question requests
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
        question = body.get('question', '').strip()

        # Validation
        if not api_key:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'status': 'error', 'error': 'API key is required'})
            }

        if not question:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'status': 'error', 'error': 'Question is required'})
            }

        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        # Create prompt with context
        prompt = f"""
        Context: You are helping with a project called "{project_name}".
        Project Description: {project_description if project_description else "No description provided"}
        
        User Question: {question}
        
        Provide a detailed, practical answer to help the user with their project development.
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
                'response': response.text
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 'error', 'error': str(e)})
        }