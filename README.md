# LeadsManager Project

## Overview
The **Leads Manager Project** is a web-based application designed to manage, track, and update leads from various sources. Built using Django, this system allows seamless integration with external APIs, provides robust form submission tracking, and includes a convenient feature for sending bulk emails using Perfit.

This document outlines the structure, features, and usage of the application, focusing on its key components and functionality. For more specific technical documentation please refer to the docs directory.

---

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Key Apps and Their Roles](#key-apps-and-their-roles)
  - [Landing App](#landing-app)
  - [Users App](#users-app)
  - [Forms App](#forms-app)
- [Environment Variables](#environment-variables)
- [Perfit Mail Integration](#perfit-mail-integration)
- [Running the Project](#running-the-project)
- [Management Commands](#management-commands)
- [Planned Features and Roadmap](#Planned-Features-and-Roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- **Lead Management:** Track and manage leads submitted via integrated forms.
- **Dynamic Filtering:** Filter leads by date, status, or assigned user.
- **API Integration:** Automatically fetch leads from external APIs.
- **Manual Lead Submission:** Add leads manually when required.
- **History Tracking:** Maintain a history of lead status updates.
- **Role-Based Access Control:** Restrict functionality based on user roles (Admin, Manager, Employee).
- **Bulk Email Sending:** Easily send emails to contacts via Perfit.

---

## Tech Stack
- **Backend:** Django 5.x
- **Frontend:** HTML, CSS (W3.CSS framework), JavaScript
- **Database:** MySQL
- **Task Queue:** Celery with Redis
- **APIs:** WordPress Custom Plugin for fetching leads
- **Additional Libraries:**
  - `pandas`: For processing Excel files
  - `requests`: For API communication
  - `plotly`: For interactive graphs

---

## Project Structure
leadsmanager/
├── landingapp/ # Homepage and general views
├── usersapp/ # User authentication and management
├── formsapp/ # Form submissions and lead management
├── static/ # Static assets (CSS, JS, images)
├── templates/ # HTML templates
├── manage.py # Django management commands entry point
├── requirements.txt # Python dependencies
├── docs/ # specific technical documentation about the apps, worflows, main features and db schema
└── README.md # Project documentation

---

## Key Apps and Their Roles

### Landing App
**URL Prefix:** `/`

- **Purpose:** Manages public-facing views, login functionality, and a lead summary dashboard.
- **Features:**
  - Home view with lead statistics.
  - Custom login page.
  - Interactive graphs for lead analysis (using Plotly).

### Users App
**URL Prefix:** `/users/`

- **Purpose:** Handles user authentication, profiles, and role-based permissions.
- **Features:**
  - User creation and management (Admins only).
  - Profile editing and password changes.
  - Role-based access to views and actions.
- **Roles:**
  - **Admin:** Full access to all features.
  - **Manager:** Manage users and leads.
  - **Employee:** Limited access to their assigned leads.

### Forms App
**URL Prefix:** `/forms/`

- **Purpose:** Manages form submissions and lead lifecycle.
- **Features:**
  - View and filter form submissions.
  - Update lead statuses manually or via bulk Excel upload.
  - Fetch new submissions from external APIs.
  - Track lead history for status changes.

---

## Environment Variables
The application uses environment variables for sensitive data. These are stored in `authvars.py` and sourced from `.env` or environment secrets.

| Variable             | Description                     |
|----------------------|---------------------------------|
| `DB_NAME`            | Database name                  |
| `DB_USR`             | Database username              |
| `DB_PASS`            | Database password              |
| `DB_HOST`            | Database host                  |
| `DB_PORT`            | Database port                  |
| `SECRET_KEY`         | Django secret key              |
| `WPCUSTOMAPISUBM`    | API base URL for fetching leads|
| `WPUSER`             | WordPress API username         |
| `WPPASS`             | WordPress API password         |
| `PRFTAPIKEY`         | Perfit API key                 |

---

## Perfit Mail Integration
The **Perfit mail functionality** is a secondary feature added to support the operations team. It allows sending bulk emails for specific operations via the Perfit API. 

**Use Cases:**
- Process an uploaded Excel file.
- Send unitary custom claim mails (templates vary depending on the nature of the claim.) for all submissions on the xlsx uploded file, to the Correo Argentino help desk service as requested.

---

## Running the Project

### Prerequisites
1. Install Python (3.8+), MySQL, and Redis.
2. Set up a virtual environment and install dependencies:
   ```
   bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```
3. Set up .env for environment variables:

### Local Setup
1. Apply migrations:
  ```
   bash
   python manage.py migrate
   ```
2. Create a superuser:
  ```
   bash
   python manage.py createsuperuser
   ```
3. Start the server:
  ```
   bash
   python manage.py runserver
   ```
4. Start Celery and Redis for task management (under development and testing):
  ```
   bash
   redis-server
  celery -A leadsmanager worker --loglevel=info
   ```

## Management Commands

### Available Commands:
- python manage.py update_forms: Fetch new form submissions via API.
- python manage.py update_estado_from_excel <path>: Update lead statuses from an Excel file.
- python manage.py export_formsubmission_data: Export form submissions to an Excel file.
- python manage.py clear_formsubmission: Clear all data from the FormSubmission table.
- python manage.py clear_forms_stat_history: Clear lead status history.

## Planned Features and Roadmap

Below are some of the upcoming features and improvements planned for the project. Contributions and feedback are welcome!

- **FastAPI microservice for database access**  
  Transition the current Celery planned implementation to a lighter FastAPI asynchronous microservice for handling systematic database queries, improving speed and scalability.

- **CI/CD Pipeline**  
  Implement GitHub Actions CI/CD to automate the deployment process, allowing for seamless versioning and deployment to Google Cloud Run (via artifact registry).

- **Leads advancement/behavior analysis**  
  The updates on each lead are already being logged, lead configurations and commercial team member performance will be analyzed for insights.

- **Enhanced Lead Management with AI**  
  Integrate a machine learning model to provide lead prioritization based on historical data, enabling more efficient resource allocation.

- **Automated Alerts**  
  Set up email and Slack notifications for lead status changes, submission errors, and other important events. API mail services already configured and waiting for mkt and commercial team feedback on mapped events for notifications.

- **Multi-language Support**  
  Enable multi-language support for international users, starting with Spanish and English.

- **Performance Optimization**  
  Optimize database queries, reduce memory footprint, and enhance the overall speed of the web application, as routine continuous development.

- **public API for data fetching**  
  Generate a public API for main data fetching like submissions, users matirx and their respective log activity and analysis results


---

Feel free to suggest any other features by opening an issue!

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
```
bash
git checkout -b feature/your-feature-name
```
3. Commit changes and submit a pull request.

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 GPLv3 License. See LICENSE for details.