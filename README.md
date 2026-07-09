# 🚀 Project Classifier - AI Mentor

A Context-Aware AI Mentor powered by Google Gemini API that transforms project ideas into comprehensive execution plans with build strategies and technical recommendations.

## 📋 Features

✨ **Intelligent Project Classification**
- Analyzes project names and descriptions
- Classifies project types (Web App, Mobile App, API, etc.)
- Recommends appropriate tech stacks

📋 **Comprehensive Build Plans**
- Step-by-step development guides
- Architecture recommendations
- Technology stack suggestions
- Deployment strategies

💬 **Interactive Chatbot Interface**
- Beautiful, responsive HTML UI
- Real-time chat with AI mentor
- Follow-up question support
- Local API key storage

🔐 **Secure API Key Management**
- Environment variable support (.env file)
- Local browser storage option
- Multiple configuration methods

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python Flask
- **AI Engine**: Google Gemini API
- **Environment**: Python-dotenv for configuration

## 📦 Installation

### Prerequisites
- Python 3.8+
- Google Gemini API key (get one from [ai.google.dev](https://ai.google.dev))
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/harikrishnanklcs24-creator/Main_Project_Team_2.git
cd Main_Project_Team_2
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

```bash
# Create .env file from example
cp .env.example .env

# Edit .env and add your Gemini API key
# Open .env and replace:
# GEMINI_API_KEY=your_gemini_api_key_here
```

Or directly in the file:
```
GEMINI_API_KEY=your-actual-api-key-here
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
```

### Step 5: Run the Application

```bash
# Start Flask server
python app.py

# Server will run on http://localhost:5000
```

### Step 6: Access the Application

Open your browser and go to:
```
http://localhost:5000
```

## 🎯 How to Use

1. **Get Gemini API Key**
   - Visit [ai.google.dev](https://ai.google.dev)
   - Create a new API key
   - Copy the key

2. **Configure API Key**
   - Option A: Add to `.env` file
   - Option B: Paste directly in the HTML interface (saved locally)

3. **Enter Project Details**
   - Project Name (required)
   - Project Description (optional)

4. **Click "Analyze Project"**
   - AI will classify your project
   - Provides tech stack recommendations
   - Generates execution plan

5. **Ask Follow-Up Questions**
   - Chat with the AI mentor
   - Get additional insights
   - Ask about specific technologies or strategies

## 📁 Project Structure

```
Main_Project_Team_2/
├── index.html                 # Frontend chatbot interface
├── app.py                      # Flask backend server
├── project_classifier.py       # Standalone CLI tool
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## 🔑 Configuration Options

### Option 1: Environment Variable (.env)
```bash
# .env file
GEMINI_API_KEY=your_api_key_here
FLASK_PORT=5000
FLASK_DEBUG=True
```

### Option 2: Direct in HTML Interface
- Paste your API key in the settings panel
- It will be saved to browser's localStorage
- No file modification needed

### Option 3: Standalone Python Script
```bash
# Set environment variable
export GEMINI_API_KEY=your_api_key_here

# Run Python script
python project_classifier.py
```

## 📝 API Endpoints

### POST /api/classify
Classify a project and get recommendations
```json
{
  "api_key": "your-api-key",
  "project_name": "E-Commerce Platform",
  "project_description": "Online store with payment integration"
}
```

### POST /api/follow-up
Ask follow-up questions about a project
```json
{
  "api_key": "your-api-key",
  "project_name": "E-Commerce Platform",
  "question": "What database should I use?"
}
```

### POST /api/execution-plan
Get detailed execution plan
```json
{
  "api_key": "your-api-key",
  "project_name": "E-Commerce Platform",
  "project_description": "..."
}
```

### GET /health
Health check endpoint

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| GEMINI_API_KEY | - | Your Google Gemini API key (required) |
| FLASK_ENV | development | Flask environment mode |
| FLASK_DEBUG | False | Enable Flask debug mode |
| FLASK_PORT | 5000 | Port to run Flask server |
| SERVER_HOST | 0.0.0.0 | Server host address |

## 🔐 Security Notes

- **Never commit `.env` file** with actual API keys
- Use `.env.example` as template
- API keys are sent over HTTPS in production
- Enable CORS only for trusted domains in production
- Consider using API key rotation in production

## 📚 Using Gemini API Key

### Getting Your API Key
1. Go to [Google AI Studio](https://ai.google.dev)
2. Click "Create API Key"
3. Select or create a Google Cloud project
4. Copy the generated API key

### Safety Tips
- Never share your API key publicly
- Rotate keys periodically
- Set usage limits in Google Cloud Console
- Use environment variables instead of hardcoding

## 🐛 Troubleshooting

### Issue: "API key is required"
- Make sure you've added your API key to .env or the interface
- Check that the key is not empty or malformed

### Issue: "Failed to connect to backend"
- Ensure Flask server is running (`python app.py`)
- Check that port 5000 is not blocked
- Try accessing http://localhost:5000 directly

### Issue: "Invalid API Key"
- Verify your Gemini API key is correct
- Check if the key has expired
- Generate a new key from [ai.google.dev](https://ai.google.dev)

### Issue: CORS Error
- Make sure Flask-CORS is installed (`pip install flask-cors`)
- Restart the Flask server after installing packages

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the [Gemini API documentation](https://ai.google.dev/docs)
3. Open an issue on GitHub

## 📄 License

This project is open source and available under the MIT License.

## 🎉 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📚 Resources

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Dotenv](https://github.com/theskumar/python-dotenv)

---

**Built with ❤️ for developers and teams**
