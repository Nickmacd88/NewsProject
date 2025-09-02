FROM python:3.11-slim

# Set working directory
WORKDIR /NewsProject

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code AND SQLite database
COPY ./NewsProject ./NewsProject
# Expose the port your FastAPI app uses
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "backend.backend:app", "--host", "0.0.0.0", "--port", "8000"]
