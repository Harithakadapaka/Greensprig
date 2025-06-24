FROM python:3.8-slim

# Set work directory
WORKDIR /code

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy rest of the project
COPY . /code/

# Start command (adjust as needed)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "greensprig_app.wsgi:application"]
