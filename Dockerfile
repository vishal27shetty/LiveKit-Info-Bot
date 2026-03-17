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
COPY data.json ./

# Install uv package manager
RUN pip install --no-cache-dir uv

# Install dependencies
RUN uv sync --frozen

# Copy embeddings if they exist, otherwise they'll be built at runtime
COPY employee_embeddings.npy* ./ || true

# Build embeddings if not present (requires GEMINI_API_KEY at build time)
# Note: It's better to pre-build embeddings and commit them to the repo
RUN if [ ! -f employee_embeddings.npy ]; then \
        echo "Warning: employee_embeddings.npy not found. Run build_embeddings.py locally first."; \
    fi

# Expose port (if needed)
EXPOSE 8080

# Run the agent
CMD ["uv", "run", "agent.py", "start"]
