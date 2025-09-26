# Bug Bounty Hunter Pro - Docker Container
# Multi-stage build for optimized production image

# Build stage
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    DISPLAY=:99

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    # GUI dependencies
    xvfb \
    x11-utils \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-xfixes0 \
    libxcb-shape0 \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libfontconfig1 \
    libxrender1 \
    libdbus-1-3 \
    # Network tools
    curl \
    wget \
    netcat-traditional \
    # Security tools
    nmap \
    # Cleanup
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Create application user
RUN groupadd -r bughunter && \
    useradd -r -g bughunter -d /app -s /bin/bash bughunter && \
    mkdir -p /app && \
    chown -R bughunter:bughunter /app

# Set working directory
WORKDIR /app

# Copy application files
COPY --chown=bughunter:bughunter . .

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/reports /app/temp && \
    chown -R bughunter:bughunter /app/data /app/logs /app/reports /app/temp

# Make scripts executable
RUN chmod +x /app/run.sh /app/install.sh /app/launch_hunter.py /app/quick_test.py

# Switch to application user
USER bughunter

# Create virtual display script
RUN echo '#!/bin/bash\n\
export DISPLAY=:99\n\
Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &\n\
exec "$@"' > /app/start-xvfb.sh && \
chmod +x /app/start-xvfb.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)" || exit 1

# Expose ports (if web interface is added in future)
EXPOSE 8080

# Set default command
CMD ["/app/start-xvfb.sh", "python3", "launch_hunter.py"]

# Labels for metadata
LABEL maintainer="Bug Bounty Hunter Pro Team <support@bughunterpro.com>" \
      version="2.0.0" \
      description="Advanced Bug Bounty Hunting Platform" \
      org.opencontainers.image.title="Bug Bounty Hunter Pro" \
      org.opencontainers.image.description="Professional security testing tool for ethical hackers" \
      org.opencontainers.image.version="2.0.0" \
      org.opencontainers.image.vendor="Bug Bounty Hunter Pro" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/llakterian/BugHunter" \
      org.opencontainers.image.documentation="https://docs.bughunterpro.com"