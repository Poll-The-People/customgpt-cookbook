FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies including jq for JSON processing
RUN apt-get update && apt-get install -y \
    jq \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install -e .

# Note: The actual code will be mounted at runtime
CMD ["/bin/bash"]