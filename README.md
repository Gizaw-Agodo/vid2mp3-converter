# Video to MP3 Converter Microservice

A scalable microservice-based application for converting video files to MP3 format, built with FastAPI, MongoDB, MySQL, and RabbitMQ. The system consists of multiple microservices: Gateway, Converter, Authentication (Auth), Notification, and RabbitMQ for message queuing.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Microservices](#microservices)
- [Technologies](#technologies)


## Overview
This project provides a microservice architecture for converting video files to MP3 audio. Users can upload videos through a gateway, authenticate their requests, and receive notifications upon conversion completion. The system leverages RabbitMQ for asynchronous task processing and supports MongoDB for file metadata storage and MySQL for user data.

## Architecture
The application is divided into the following microservices:
- **Gateway**: Handles incoming requests, routes them to appropriate services, and manages API orchestration.
- **Auth**: Manages user authentication and authorization using JWT tokens.
- **Converter**: Processes video-to-MP3 conversion tasks asynchronously using FFmpeg.
- **Notification**: Sends notifications (e.g., email or in-app) upon task completion.
- **RabbitMQ**: Message broker for asynchronous communication between services.

Data storage:
- **MongoDB**: Stores metadata for uploaded videos and converted MP3 files.
- **MySQL**: Stores user information and authentication data.

## Microservices
1. **Gateway Service**
   - Built with FastAPI.
   - Acts as the entry point for client requests.
   - Routes requests to Auth, Converter, or Notification services.
   - Handles load balancing and request validation.

2. **Auth Service**
   - Manages user registration, login, and token generation.
   - Uses MySQL to store user credentials.
   - Secures endpoints with JWT-based authentication.

3. **Converter Service**
   - Converts uploaded video files to MP3 using FFmpeg.
   - Consumes tasks from RabbitMQ queues.
   - Stores metadata (e.g., file size, duration) in MongoDB.

4. **Notification Service**
   - Sends notifications to users via email or in-app messages.
   - Listens to RabbitMQ for conversion completion events.

5. **RabbitMQ**
   - Facilitates asynchronous communication between microservices.
   - Queues conversion tasks and notification events.

## Technologies
- **FastAPI**: High-performance Python framework for building APIs.
- **MongoDB**: NoSQL database for storing file metadata.
- **MySQL**: Relational database for user data.
- **RabbitMQ**: Message broker for task queuing and event-driven communication.
- **FFmpeg**: Tool for video-to-MP3 conversion.
- **Docker**: Containerization for microservices.
- **Python**: Primary programming language.
