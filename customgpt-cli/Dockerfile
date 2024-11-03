FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install -e .

# Note: The actual code will be mounted at runtime
CMD ["/bin/bash"]