"""
Project Classifier using Google Gemini API
Classifies project types and provides build guidelines and execution plans
"""

import google.generativeai as genai
import os
import json
from typing import Dict, Any

# Configure Gemini API
# You can add your API key directly or use environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY_HERE')

def configure_gemini(api_key: str = None) -> None:
    """
    Configure Gemini API with the provided API key
    
    Args:
        api_key: Google Gemini API key. If None, uses environment variable
    """
    if api_key:
        genai.configure(api_key=api_key)
    else:
        genai.configure(api_key=GEMINI_API_KEY)


def classify_project(project_name: str, project_description: str = "") -> Dict[str, Any]:
    """
    Classify a project and get build guidelines using Gemini
    
    Args:
        project_name: Name of the project
        project_description: Optional detailed description of the project
        
    Returns:
        Dictionary containing project classification and build guidelines
    """
    
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Analyze the following project and provide:
    1. Project Type Classification (e.g., Web App, Mobile App, API, Desktop App, etc.)
    2. Technology Stack Recommendations
    3. Architecture Recommendations
    4. Step-by-step Build Plan
    5. Deployment Considerations
    6. Time Estimate for Development
    7. Potential Challenges
    
    Project Name: {project_name}
    Project Description: {project_description if project_description else "No description provided"}
    
    Please provide a detailed, structured response.
    """
    
    try:
        response = model.generate_content(prompt)
        
        result = {
            "status": "success",
            "project_name": project_name,
            "classification": response.text,
            "model_used": "gemini-pro"
        }
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "project_name": project_name,
            "error": str(e),
            "message": "Failed to classify project"
        }


def get_build_execution_plan(project_name: str, project_type: str = "") -> Dict[str, Any]:
    """
    Get a detailed execution plan for building the project
    
    Args:
        project_name: Name of the project
        project_type: Type of project (optional)
        
    Returns:
        Dictionary containing detailed execution plan
    """
    
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Create a comprehensive build and execution plan for the following project:
    
    Project Name: {project_name}
    Project Type: {project_type if project_type else "Generic"}
    
    Please provide:
    1. Project Initialization Steps
    2. Environment Setup
    3. Dependency Installation
    4. Core Development Phases (with detailed tasks)
    5. Testing Strategy
    6. Documentation Requirements
    7. Code Review Checklist
    8. Git Workflow and Commit Strategy
    9. Deployment Steps
    10. Post-Launch Monitoring
    
    Format as a structured, actionable plan.
    """
    
    try:
        response = model.generate_content(prompt)
        
        result = {
            "status": "success",
            "project_name": project_name,
            "execution_plan": response.text,
            "model_used": "gemini-pro"
        }
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "project_name": project_name,
            "error": str(e),
            "message": "Failed to generate execution plan"
        }


def analyze_and_save_results(project_name: str, project_description: str = "", output_file: str = None) -> Dict[str, Any]:
    """
    Analyze project, get build plan, and save results to a file
    
    Args:
        project_name: Name of the project
        project_description: Detailed project description
        output_file: Optional file path to save results
        
    Returns:
        Dictionary containing full analysis
    """
    
    print(f"🚀 Analyzing project: {project_name}")
    print("-" * 50)
    
    # Get classification
    print("📊 Classifying project...")
    classification_result = classify_project(project_name, project_description)
    
    if classification_result["status"] == "error":
        print(f"❌ Error: {classification_result['error']}")
        return classification_result
    
    print("✅ Classification complete!")
    print()
    
    # Get execution plan
    print("📋 Generating execution plan...")
    plan_result = get_build_execution_plan(project_name)
    
    if plan_result["status"] == "error":
        print(f"❌ Error: {plan_result['error']}")
        return plan_result
    
    print("✅ Execution plan generated!")
    print()
    
    # Combine results
    full_result = {
        "project_name": project_name,
        "project_description": project_description,
        "classification": classification_result["classification"],
        "execution_plan": plan_result["execution_plan"],
        "status": "success"
    }
    
    # Save to file if specified
    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(f"# Project Analysis: {project_name}\n\n")
                f.write(f"## Project Description\n{project_description}\n\n")
                f.write(f"## Classification and Recommendations\n{classification_result['classification']}\n\n")
                f.write(f"## Execution Plan\n{plan_result['execution_plan']}\n")
            print(f"💾 Results saved to {output_file}")
        except Exception as e:
            print(f"⚠️  Could not save results: {e}")
    
    return full_result


def main():
    """Main function to demonstrate project classification"""
    
    # Configure Gemini - You can pass your API key here
    # Option 1: Set environment variable GEMINI_API_KEY before running
    # Option 2: Pass API key directly:
    # configure_gemini("your-api-key-here")
    
    configure_gemini()
    
    # Example usage
    print("=" * 50)
    print("   Project Classifier - Powered by Gemini AI")
    print("=" * 50)
    print()
    
    # Get project details from user
    project_name = input("Enter project name: ").strip()
    
    if not project_name:
        print("Project name cannot be empty!")
        return
    
    project_description = input("Enter project description (optional): ").strip()
    
    print()
    
    # Analyze and save results
    results = analyze_and_save_results(
        project_name=project_name,
        project_description=project_description,
        output_file=f"{project_name.replace(' ', '_')}_analysis.md"
    )
    
    if results["status"] == "success":
        print()
        print("=" * 50)
        print("   Analysis Complete!")
        print("=" * 50)
        print()
        print("📄 CLASSIFICATION AND RECOMMENDATIONS:")
        print("-" * 50)
        print(results["classification"])
        print()
        print("📋 EXECUTION PLAN:")
        print("-" * 50)
        print(results["execution_plan"])
    else:
        print(f"Analysis failed: {results.get('message', 'Unknown error')}")


if __name__ == "__main__":
    main()
