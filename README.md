# Audio Recognition Microservices

## Table of Contents
1. [Project Overview](#project-overview)
2. [File Structure](#file-structure)
3. [Microservices Overview](#microservices-overview)
4. [Prerequisits](#prerequisits)
5. [Setup Instructions](#setup-instructions)
6. [Testing](#testing)
7. [Logging](#logging)
8. [Music Files](#music-files)

## Project Overview
This project consists of three microservices that enable audio recognition and catalogue management using Flask and SQLite. The system allows administrators and users to:


- Add a music track to the catalogue, so that a user can listen to it.
- Remove a music track from the catalogue, so that a user cannot listen to it.
- List the names of the music tracks in the catalogue, to know what it contains.
- Convert a music fragment to a music track in the catalogue, to listen to it.

The project follows a microservices architecture, with separate services handling database management, catalogue management, and audio recognition.

## File Structure
```
│──src/
│   │──Catalogue_management_microservice/
│   |   │──catalogue_management_microservice.py
│   |   └──catalogue.log (Note: Generated on microservice execution)
|   |
│   │──Database_management_microservice/
|   |   │──database_management_microservice.py
│   |   └──database.log (Note: Generated on microservice execution)
|   |
│   │──Audio_recognition_microservice/
│   |   │──audio_recognition_microservice.py
│   |   │──audio.log (Note: Generated on microservice execution)
│   |   └──.env (to be added my user and should contain their own AUDD.io API KEY)
|   |
│   └──database_helper.py
│
│──tests/
│   │──user_story_1_tests.py
│   │──user_story_2_tests.py
│   │──user_story_3_tests.py
│   └──user_story_4_tests.py
│
│──Music/  (Note: Empty in submission, users should add music files here for testing)
│   │──Fragments/
│   |   └──[INSERT FRAGMENT .WAV FILES HERE]
│   └──Tracks/
│       └──[INSERT TRACK .WAV FILES HERE]
│
│──data/
│   └──data.db (Note: Generated on database microservice execution)
│
│──requirements.txt
│──README.md
│──Design_Document.pdf
└──Gen_AI_Declaration.pdf
```

## Microservices Overview

### 1. **Database Management Microservice** (Port: 3001)
Handles storage and retrieval of music tracks using an SQLite database.
- **POST /db/tracks** – Add a new track
- **DELETE /db/tracks/\<title\>** – Remove a track
- **GET /db/tracks** – Retrieve all tracks
- **GET /db/tracks/search?title=\<title\>** – Search for a track by title
- **POST /db/reset** – Reset the database (for testing)

### 2. **Catalogue Management Microservice** (Port: 3000)
Interacts with the database service to manage the music catalogue.
- **POST /tracks** – Add a track to the catalogue
- **DELETE /tracks/\<title\>** – Delete a track
- **GET /tracks** – Get all tracks
- **GET /tracks/search?title=\<title\>** – Search for a track

### 3. **Audio Recognition Microservice** (Port: 3002)
Recognizes audio fragments using the AudD.io API and checks if they exist in the catalogue.
- **POST /recognise** – Identify an audio fragment and check the catalogue

## Prerequisites
Ensure you have the following installed:
- Python 3.8+
- `pip`

## Setup Instructions

1. **Extract the submission ZIP file**
```sh
unzip submission.zip
cd submission
```

2. **Install dependencies**
```sh
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file inside `src/Audio_recognition_microservice/` and add:
```
AUDDIO_TOKEN=<your_audd_io_api_key>
```

4. **Run the microservices**
Start each microservice in a separate terminal:

- **Database Service**
  ```sh
  python src/Database_management_microservice/database_management_microservice.py
  ```

- **Catalogue Service**
  ```sh
  python src/Catalogue_management_microservice/catalogue_management_microservice.py
  ```

- **Audio Recognition Service**
  ```sh
  python src/Audio_recognition_microservice/audio_recognition_microservice.py
  ```

## Testing
Tests are organized under `tests/`. To run them:
```sh
pytest tests/test_name.py
```

## Logging
Log files will be generated in the directory for each microservice.

## Music Files
For testing, users should add relevant .wav files to the `Music/Fragments/` and `Music/Tracks/` directories respectively before running the services.

---
For microservice enpoint diagrams refer to the `Design_Document.pdf`.