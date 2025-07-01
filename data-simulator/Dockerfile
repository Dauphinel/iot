FROM python:3.9-slim

# Install required packages
RUN pip install --no-cache-dir \
    kafka-python==2.0.2 \
    requests==2.31.0

# Create app directory
WORKDIR /app

# Copy the simulator script
COPY data_simulator.py /app/

# Make script executable
RUN chmod +x /app/data_simulator.py

# Run the simulator
CMD ["python3", "data_simulator.py"]