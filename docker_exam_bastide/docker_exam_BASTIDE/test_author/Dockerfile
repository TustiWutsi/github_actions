FROM ubuntu:18.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    && apt-get clean

# Upgrade pip and install requests
RUN pip3 install --upgrade pip && pip3 install requests==2.27.1

# Copy your script
ADD test_authorization.py /test/test_authorization.py
WORKDIR /test/

# Run the test
CMD ["python3", "test_authorization.py"]