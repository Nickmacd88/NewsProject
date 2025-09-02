FROM python:3.11-slim

# Set working directory
WORKDIR /NewsProject

# Copy all of the files and install Python dependencies
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your FastAPI app uses
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "backend.backend:app", "--host", "0.0.0.0", "--port", "8000"]
