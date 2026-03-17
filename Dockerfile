# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml uv.lock* ./
COPY agent.py custom_llm.py build_embeddings.py ./
COPY data.json employee_embeddings.npy* ./

# Install uv package manager
RUN pip install --no-cache-dir uv

# Install dependencies
RUN uv sync --frozen

# Expose port (if needed)
EXPOSE 8080

# Run the agent
CMD ["uv", "run", "agent.py", "start"]
