FROM node:16 AS base

# Install Python and other dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Create challenge directory with restricted permissions
RUN mkdir /challenge && chmod 700 /challenge

# Set working directory to /challenge
WORKDIR /challenge

# Copy package files
COPY package.json package-lock.json ./

# Install Node dependencies
RUN npm install

# Copy requirements.txt and install Python dependencies
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy challenge files to /challenge
COPY app /challenge/app/
COPY config.py run.py tailwind.config.js setup-challenge.py ./

# Build CSS with verbose output
RUN npm run build || (cat npm-debug.log && exit 1)

FROM base AS challenge
ARG FLAG

# Run the setup script
RUN python3 /challenge/setup-challenge.py

EXPOSE 5000 18739

# The comment below is parsed by cmgr. You can reference the port by the name
# given, but if there is only one port published, you don't have to use the name
# PUBLISH 5000 AS web
# PUBLISH 18739 AS crypto

CMD ["python3", "/challenge/run.py"]
