# Music Catalogue Microservices

This project consists of three microservices that work together to manage and recognize music tracks. These microservices include:

- **Catalogue Microservice**: Manages the music track catalogue.
- **Audio Recognition Microservice**: Recognizes music track fragments.
- **Database Microservice**: Manages the track data in the database.

## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Microservices Setup](#microservices-setup)
4. [Running the Services](#running-the-services)
5. [API Endpoints](#api-endpoints)
6. [Logging](#logging)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)


## Requirements

- **Python 3.8+** (or your preferred version)
- **Conda** (for managing environments)
- **Requests library**
- **Flask** (web framework for APIs)
- **dotenv** (for environment variable management)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://your-repository-url.git
    cd your-repository-name
    ```

2. **Create a Conda environment**:
    ```bash
    conda create --name music_catalogue_env python=3.8
    conda activate music_catalogue_env
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

    Or, if you are using conda to install dependencies, you can create a `environment.yml` file and run:

    ```bash
    conda env create -f environment.yml
    conda activate music_catalogue_env
    ```

## Microservices Setup

The microservices are structured as follows:

- **Catalogue Microservice**: Handles the addition, deletion, and retrieval of tracks.
- **Database Microservice**: Manages track data in the database.
- **Audio Recognition Microservice**: Uses audio recognition to identify music tracks.

## Running the Services

To run the services in separate terminal windows, follow these steps:

1. Open a new terminal window and run the Catalogue Microservice:
    ```bash
    python catalogue_microservice.py
    ```

2. Open another terminal window and run the Database Microservice:
    ```bash
    python database_microservice.py
    ```

3. Open a final terminal window and run the Audio Recognition Microservice:
    ```bash
    python audio_microservice.py
    ```

If you are using **Anaconda PowerShell**, make sure to activate your Conda environment in each window before running the microservices:
```powershell
conda activate music_catalogue_env
```

Alternatively, you can use a script to launch all services simultaneously.

## API Endpoints
Here are the available endpoints for each service:

### Catalogue Microservice
- **POST /tracks**: Add a new track to the catalogue
- **DELETE /tracks/\<title\>**: Delete a track by title
- **DELETE /tracks/**: Delete track without a title (invalid request)
- **GET /tracks**: Get all tracks in the catalogue
- **GET /tracks/search**: Search for a track by title
### Audio Recognition Microservice
- **POST /recognise**: Recognizes a track from an audio fragment
### Database Microservice
- **POST /db/tracks**: Add a new track to the database
- **DELETE /db/tracks/\<title\>**: Delete a track from the database by title
- **GET /db/tracks**: Get all tracks from the database
- **GET /db/tracks/search**: Search for a track in the database by title
- **POST /db/reset**: Reset the database

## Logging
Each microservice has its own individual log file in the ```/logs``` directory:

- ```catalogue_service.log```
- ```audio_service.log```
- ```database_service.log```

Logs are automatically generated for all incoming requests, errors, and other significant events.

## Testing
To run tests for each microservice:

1. Ensure all services are running.

2. Use **pytest** to run tests:

```
pytest
```

Make sure to configure your test environment, including the required ```.env``` files or database setup, before running tests.

## Troubleshooting
If you encounter any issues, check the individual service logs located in the ```/logs``` directory for detailed error messages and request data.

