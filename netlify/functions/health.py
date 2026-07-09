"""
Netlify Serverless Function - Health Check API
"""

import json


def health(event, context):
    """Health check endpoint"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({
            'status': 'ok',
            'message': 'Project Classifier API is running on Netlify'
        })
    }