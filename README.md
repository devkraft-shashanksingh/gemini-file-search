# Gemini File Search PPT Assistant

This project is a simple web application that allows you to upload PowerPoint presentations (`.ppt`, `.pptx`), index them using Google's Gemini File Search API, and ask questions about the content.

## Prerequisites

- Python 3.12+
- A Google Cloud Project with the Gemini API enabled and an API Key.
- `pip`

## Setup

1.  **Clone/Open the repository**
    ```bash
    cd /home/dev/gemini-file-search
    ```

2.  **Set up the Virtual Environment**
    If you haven't already:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r backend/requirements.txt
    ```

## Running the Application

### 1. Start the Backend Server

Open a terminal and run:

```bash
# From the project root
./venv/bin/uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
*Note: Ensure your `GEMINI_API_KEY` is set in `backend/main.py`.*

### 2. Open the Frontend

You can simply open the `index.html` file in your browser.

- **Option A (File System):**
  Locate `frontend/index.html` in your file explorer and double-click it.

- **Option B (Simple HTTP Server):**
  Run this in a separate terminal to serve the frontend on `http://localhost:5500`:
  ```bash
  cd frontend
  python3 -m http.server 5500
  ```
  Then open `http://localhost:5500` in your browser.

## Usage

1.  **Upload**: Click the upload area or drag and drop a `.pptx` file. Click "Upload & Index". Wait for the success message.
2.  **Ask**: Type a question in the text box (e.g., "Summarize slide 3") and click "Ask".
3.  **View**: Read the answer and check the citations below.
