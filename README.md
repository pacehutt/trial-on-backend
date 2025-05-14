# FastAPI Backend

This is a FastAPI backend for applying designs to clothing in images.

## Prerequisites

- Python 3.10 or higher
- `pip` (Python package manager)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd fyp-backend
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the FastAPI server:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. Open your browser or API client (e.g., Postman) and navigate to:
   ```
   http://127.0.0.1:8000/docs
   ```
   This will open the interactive API documentation.

## Notes

- Ensure that you have all required system libraries installed for `opencv-python` and `torch`. On some systems, you may need to install additional libraries like `libGL` for OpenCV.
- If you encounter the error `ImportError: libGL.so.1: cannot open shared object file`, install the missing library:
  ```bash
  sudo apt-get update && sudo apt-get install -y libgl1-mesa-glx
  ```

## Project Structure

```
app/
├── main.py               # Entry point of the application
├── routes/
│   └── process.py        # API routes
├── services/
│   ├── image_processor.py # Image processing logic
│   └── segmentation.py    # Segmentation logic
├── utils/
│   └── io_utils.py       # Utility functions for file I/O
```

## License

This project is licensed under the MIT License.
