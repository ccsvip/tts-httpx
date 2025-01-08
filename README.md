好的，我帮你重新整理一下 README.md 文件的格式，使其更清晰易读，并添加一些细节：


# Audio Processing API

This is an audio processing API service built with FastAPI, supporting functionalities like speech-to-text, text-based conversation, and text-to-speech.

## Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/)
- [pyenv-win](https://github.com/pyenv-win/pyenv-win) (for Windows environments)

## Setup

### 1. Install pyenv-win (Windows)

For Windows users, install pyenv-win to manage Python versions:

```powershell
# Run PowerShell as administrator
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

After installation, restart your terminal and verify:
```bash
pyenv --version
```

### 2. Install Poetry

Install Poetry, a tool for managing dependencies and packaging:

```bash
# Windows PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Configure Poetry to create virtual environments within the project directory:

```bash
poetry config virtualenvs.in-project true
```

### 3. Project Setup

1. Clone the repository and navigate to the project directory:

   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Use pyenv to install and set the Python version:

   ```bash
   pyenv install 3.10.0
   pyenv local 3.10.0
   ```

3. Install project dependencies using Poetry:

   ```bash
   poetry install
   ```

4. Configure environment variables:

   Duplicate the `.env.example` file to `.env` and fill in the required environment variables:

   ```bash
   cp .env.example .env
   ```

   Required environment variables include:

   - `API_KEY`: API key for authentication.
   - `BASE_URL`: Base URL for external services.
   - `API_URL`: API URL for the external TTS service.
   - `PORT`: Port on which the service will run.
   - `REFERENCE_ID`: Reference ID for the TTS service.
   - `DOCKER_PORT`: Port mapping for docker.

## Running the Project

### Using Poetry

To run the application using Poetry:

```bash
poetry run python main.py
```

### Using Docker

To run the application using Docker:

```bash
# Build the Docker image
docker-compose build

# Run the service
docker-compose up -d
```

## API Documentation

After starting the service, access the Swagger API documentation at `http://localhost:{PORT}/` (replace `{PORT}` with the actual port number).

### Key Endpoints

- `POST /v1/tts`: Upload an audio file.
- `GET /v1/tts/{file_name}`: Retrieve a specific audio file.
- `GET /v1/tts`: Retrieve a list of all audio files.
- `DELETE /v1/tts/{file_name}`: Delete a specific audio file.
- `DELETE /v1/tts`: Delete all audio files.
- `POST /v1/chat`: Send text and get a model's response.

## Project Structure

```
.
├── api/                    # API-related code
│   ├── endpoints.py       # API endpoint definitions
│   ├── dependencies.py    # Dependency functions
│   └── utils.py          # Utility functions
├── core/                  # Core functionality modules
│   ├── chat.py           # Chat functionalities
│   └── tts.py            # Text-to-speech functionalities
├── config.py             # Configuration file
├── main.py               # Main application entry point
├── Dockerfile            # Docker configuration file
├── docker-compose.yaml   # Docker Compose configuration
└── poetry.toml          # Poetry configuration file
```

## Important Notes

1.  Ensure all necessary environment variables in the `.env` file are correctly configured.
2.  Uploaded audio files are stored in the `uploads` directory.
3.  The service supports Cross-Origin Resource Sharing (CORS).
