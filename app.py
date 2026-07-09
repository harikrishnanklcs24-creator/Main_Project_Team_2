"""
Flask Backend API for Project Classifier
Handles requests from the HTML frontend and communicates with Gemini API
Optimized for Vercel Deployment
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Configure Gemini API
def configure_gemini(api_key):
    """Configure Gemini with provided API key"""
    genai.configure(api_key=api_key)

@app.route('/', methods=['GET'])
def serve_index():
    """Serve the index.html file"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except FileNotFoundError:
        return jsonify({"error": "index.html not found"}), 404

@app.route('/api/classify', methods=['POST', 'OPTIONS'])
def classify_project():
    """
    Classify a project and get recommendations
    Expected JSON: {
        "api_key": "...",
        "project_name": "...",
        "project_description": "..."
    }
    """
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        api_key = data.get('api_key', '').strip()
        project_name = data.get('project_name', '').strip()
        project_description = data.get('project_description', '').strip()

        # Validation
        if not api_key:
            return jsonify({
                "status": "error",
                "error": "API key is required"
            }), 400

        if not project_name:
            return jsonify({
                "status": "error",
                "error": "Project name is required"
            }), 400

        # Configure Gemini
        configure_gemini(api_key)

        # Create the model
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

        return jsonify({
            "status": "success",
            "project_name": project_name,
            "classification": response.text
        }), 200

    except Exception as e:
        print(f"Error in classify_project: {str(e)}", file=sys.stderr)
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/api/follow-up', methods=['POST', 'OPTIONS'])
def follow_up_question():
    """
    Handle follow-up questions about a project
    Expected JSON: {
        "api_key": "...",
        "project_name": "...",
        "project_description": "...",
        "question": "..."
    }
    """
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        api_key = data.get('api_key', '').strip()
        project_name = data.get('project_name', '').strip()
        project_description = data.get('project_description', '').strip()
        question = data.get('question', '').strip()

        # Validation
        if not api_key:
            return jsonify({
                "status": "error",
                "error": "API key is required"
            }), 400

        if not question:
            return jsonify({
                "status": "error",
                "error": "Question is required"
            }), 400

        # Configure Gemini
        configure_gemini(api_key)

        # Create the model
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

        return jsonify({
            "status": "success",
            "response": response.text
        }), 200

    except Exception as e:
        print(f"Error in follow_up_question: {str(e)}", file=sys.stderr)
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/api/execution-plan', methods=['POST', 'OPTIONS'])
def get_execution_plan():
    """
    Get detailed execution plan for a project
    Expected JSON: {
        "api_key": "...",
        "project_name": "...",
        "project_description": "..."
    }
    """
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        api_key = data.get('api_key', '').strip()
        project_name = data.get('project_name', '').strip()
        project_description = data.get('project_description', '').strip()

        # Validation
        if not api_key:
            return jsonify({
                "status": "error",
                "error": "API key is required"
            }), 400

        if not project_name:
            return jsonify({
                "status": "error",
                "error": "Project name is required"
            }), 400

        # Configure Gemini
        configure_gemini(api_key)

        # Create the model
        model = genai.GenerativeModel('gemini-pro')

        # Create prompt
        prompt = f"""
        Create a comprehensive, detailed execution plan for building the following project:
        
        Project Name: {project_name}
        Project Description: {project_description if project_description else "No description provided"}
        
        Provide a week-by-week execution plan including:
        1. **Week 1-2: Planning & Setup**
        2. **Week 3-4: Core Development Phase 1**
        3. **Week 5-6: Core Development Phase 2**
        4. **Week 7: Testing & Bug Fixes**
        5. **Week 8: Documentation & Deployment**
        
        For each phase, include:
        - Specific tasks
        - Deliverables
        - Testing strategy
        - Risk mitigation
        
        Also include Git commit strategy and code review guidelines.
        """

        # Generate content
        response = model.generate_content(prompt)

        return jsonify({
            "status": "success",
            "execution_plan": response.text
        }), 200

    except Exception as e:
        print(f"Error in get_execution_plan: {str(e)}", file=sys.stderr)
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "message": "Project Classifier API is running"
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors - serve index.html for SPA routing"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except FileNotFoundError:
        return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        "status": "error",
        "error": "Internal server error"
    }), 500


# WSGI entry point for Vercel
if __name__ == '__main__':
    # Get debug mode from environment
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('FLASK_PORT', 5000))
    
    # In Vercel, Flask runs behind gunicorn, so debug is not used
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
