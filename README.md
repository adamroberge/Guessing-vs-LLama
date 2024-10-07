
# Guessing-vs-LLama: Pictionary with LLaMA
Welcome to Guessing-vs-LLama, a Pictionary-style web application where you can draw doodles, and a language model (LLaMA) will attempt to guess what you've drawn! This project integrates a Flask backend with a simple frontend and leverages the power of LLaMA models deployed via DeepInfra.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features
- **Interactive Drawing Canvas:** Draw your doodles directly in the browser.
- **AI Guessing:** The LLaMA model attempts to guess your drawing.
- **Flask Backend:** A simple API to handle image processing and communication with the AI model.
- **DeepInfra Integration:** Utilizes DeepInfra's OpenAI-compatible API for model deployment.

## Prerequisites
- Python 3.7 or higher
- Node.js (for frontend development, optional)
- DeepInfra account with a deployed LLaMA model
- Web browser (Chrome, Firefox, etc.)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Guessing-vs-LLama.git
cd Guessing-vs-LLama
```

### 2. Set Up a Python Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scriptsctivate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Set the following environment variables with your DeepInfra credentials:

- `DEEPINFRA_API_KEY`: Your DeepInfra API key.
- `DEEPINFRA_DEPLOYMENT_ID`: Your DeepInfra deployment ID.

For example:
```bash
export DEEPINFRA_API_KEY='your_actual_api_key'
export DEEPINFRA_DEPLOYMENT_ID='your_actual_deployment_id'
```

### 5. Install Frontend Dependencies (Optional)
If you plan to modify the frontend:

```bash
cd frontend
npm install
```

## Usage

### 1. Run the Flask Backend
In the project root directory, run:
```bash
python flask_app.py
```
The backend server will start on http://127.0.0.1:5001.

### 2. Run the Frontend Server
You can serve the frontend using a simple HTTP server:
```bash
cd frontend
python -m http.server 8000
```
The frontend will be available at http://127.0.0.1:8000.

### 3. Play the Game
- Open your web browser and navigate to http://127.0.0.1:8000.
- Click "Start New Game" to begin.
- Use the drawing canvas to create your doodle.
- Click "Predict Drawing" to have the AI guess your drawing.

## Project Structure
```bash
Guessing-vs-LLama/
├── flask_app.py          # Flask backend application
├── llm_api_calls.py      # Functions to interact with the AI model
├── requirements.txt      # Python dependencies
├── README.md             # Project README file
├── frontend/             # Frontend files
│   ├── index.html
│   ├── styles.css
│   └── script.js
└── images/               # Folder to store images
```

## Configuration
- **Model Name:** Ensure the `MODEL_NAME` in `llm_api_calls.py` matches your deployed model on DeepInfra.
- **API Base URL:** The `api_base` is set to use DeepInfra's OpenAI-compatible API.

```python
# llm_api_calls.py

openai.api_key = API_KEY
openai.api_base = 'https://api.deepinfra.com/v1/deployment/openai'
```

## Deployment
To deploy the application to a production environment, consider the following:
- Use a production-ready web server like Gunicorn or uWSGI for the Flask app.
- Serve the frontend using a web server like Nginx or Apache.
- Secure your API keys and environment variables.
- Use HTTPS for secure communication.

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.

2. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

3. Commit your changes:
```bash
git commit -m 'Add some feature'
```

4. Push to the branch:
```bash
git push origin feature/your-feature-name
```

5. Open a pull request.

## License
This project is licensed under the MIT License.

## Acknowledgements
- **DeepInfra** for providing the OpenAI-compatible API and model deployment platform.
- **OpenAI** for the openai Python library.
- **Flask** for the web framework.
- **Node.js** for the frontend development environment.
