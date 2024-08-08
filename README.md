# EventSync Application

EventSync is a web application designed to facilitate event management. It provides tools for organizing events, tracking RSVPs, managing user interactions, and more. This guide will help you understand the project structure, how to navigate through the codebase, and how to set up the application for both development and production environments.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Setup](#setup)
  - [Development Setup](#development-setup)
  - [Production Setup](#production-setup)
- [Usage](#usage)
- [Testing](#testing)
- [Contact](#contact)

## Project Overview

EventSync is designed to streamline the process of event management. It includes features for creating and managing events, sending and tracking invitations, handling RSVPs, and managing vendor information. Additionally, it provides community features where users can create and join communities, and participate in community discussions.

## Features

- Event Creation and Management
- RSVP Tracking
- Vendor Management
- Community Creation and Participation
- Notifications for Event Updates
- Data Export in CSV and JSON formats

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Bootstrap, Jinja2
- **Database**: SQLite
- **Deployment**: Waitress (for production), Flask's built-in server (for development)
- **Others**: Git, Virtualenv

## Setup

### Development Setup

For setting up the development environment, please refer to [DEV_README.md](DEV_README.md).

### Production Setup

For setting up the production environment, please refer to [PROD_README.md](PROD_README.md).

## Usage

Once the application is set up and running, you can access it via your web browser. Use the navigation bar to access different sections of the application such as the Dashboard, Login, Event Management pages, etc.

## Testing

To run tests, use the following command:
```bash
python -m unittest discover
```

## Contact

For any questions or support, please contact:

Leah Mirch - [lmirch@umich.edu](mailto:lmirch@umich.edu)

GitHub: [https://github.com/leahmirch](https://github.com/leahmirch)