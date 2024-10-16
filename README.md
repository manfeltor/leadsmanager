# LeadsManager

A Django-based web application for managing leads, tracking form submissions, and automating tasks using Celery.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Deployment](#deployment)
- [Setup (Development)](#setup-development)
- [Usage](#usage)
- [Planned features](#planned-features)
- [Contributing](#contributing)

## Project Overview

LeadsManager is a lead management system designed to streamline the process of capturing, organizing, and managing customer inquiries. The platform integrates with external forms, processes leads into a centralized database, and allows users to manage, track, and follow up on these leads efficiently.

The application architecture is built using Django, with Celery handling background task automation, MySQL for database management, and Redis for Celery task queuing. It’s deployed on **Google Cloud Run** for scalable and containerized service management.

### Key Components:
- **Forms Integration**: Captures customer information from multiple form sources and normalizes it into a unified lead management interface.
- **Lead Management**: Enables team members to manage the lifecycle of a lead from inquiry to closure, including follow-up actions and status updates.
- **Task Automation**: Uses Celery to automate routine tasks such as sending emails, performing follow-ups, and updating lead statuses.
- **Role-Based Access Control**: Assigns different levels of permissions based on user roles, such as employee, manager, and admin.
  
## Features

- **Lead Capture**: Integration with web forms for capturing lead data.
- **Task Automation**: Automate tasks like email notifications and status updates using Celery.
- **Lead Management Dashboard**: An intuitive interface for viewing, filtering, and managing leads.
- **Analytics**: Real-time reporting and insights into lead conversions and performance.
- **Role-Based Permissions**: Fine-grained control over user permissions and actions.
- **Customizable Workflows**: Adaptable lead states and task automation workflows.

## Tech Stack

- **Django 5.1.1**: Web framework for the core application.
- **Celery 5.4.0**: Distributed task queue for background processing.
- **MySQL**: Relational database used for storing lead data.
- **Redis**: Task broker for Celery.
- **Google Cloud Run**: Used for scalable, containerized deployment.
- **Docker**: For containerizing the application for local development and production.

## Deployment

To deploy this application on **Google Cloud Run**, follow the steps outlined in the [Deployment Documentation](docs/deployment.md). Here's a brief summary of the process:

1. Build the Docker image and push it to Google Container Registry.
2. Deploy the image using Google Cloud Run and configure environment variables from Google Secrets.
3. Set up MySQL using Google Cloud SQL and manage database migrations using Django.

For more details, check the deployment instructions in the linked documentation.

## Setup (Development)

To run the LeadsManager project in your local environment, follow these steps:

### Prerequisites:
- Python 3.10 or later.
- Docker (optional but recommended).
- MySQL (or use a local database).

### Steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourrepo/leadsmanager.git
    cd leadsmanager
    ```

2. **Install dependencies:**

    You can install Python dependencies using `pip` (recommended use a virtual env):

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up the database:**

    Apply migrations to set up the local database:

    ```bash
    python manage.py migrate
    ```

4. **Run the development server:**

    Start the Django development server as insecure for static acces:

    ```bash
    python manage.py runserver --insecure
    ```

5. **Run Celery worker (in a new terminal):**

    Start the Celery worker:

    ```bash
    celery -A leadsmanager worker --loglevel=info
    ```

6. **Run Celery beat (optional for periodic tasks):**

    ```bash
    celery -A leadsmanager beat --loglevel=info
    ```

## Usage

### Access the Admin Panel:
Once your development server is up and running, you can access the admin panel:

- URL: `http://localhost:8000/admin`
- Use the superuser credentials created during setup.

### Test Lead Submission:
To test lead submissions, you can go to:

- URL: `http://localhost:8000/forms/`

You can manually submit forms here, and leads will be processed and stored in the database.

## 🚀 Planned Features / Roadmap

Below are some of the upcoming features and improvements planned for the project. Contributions and feedback are welcome!

- **FastAPI microservice for database access**  
  Transition the current Celery implementation to a lighter FastAPI service for handling database queries, improving speed and scalability.

- **CI/CD Pipeline**  
  Implement GitLab CI/CD (or GitHub Actions) to automate the deployment process, allowing for seamless versioning and deployment to Google Cloud Run.

- **Leads advancement analysis**  
  The updates on each lead are already being logged. leads config behavior and commercial team members performance will be analyzed for upper management reporting.

- **Enhanced Lead Management with AI**  
  Integrate a machine learning model to provide lead prioritization based on historical data, enabling more efficient resource allocation.

- **Automated Alerts**  
  Set up email and Slack notifications for lead status changes, submission errors, and other important events. API mail services already configured and waiting for mkt and commercial team feedback on mapped events for notifications.

- **GraphQL API**  
  Add a GraphQL API alongside the current REST API to provide more flexible queries for frontend applications.

- **Multi-language Support**  
  Enable multi-language support for international users, starting with Spanish and English.

- **Performance Optimization**  
  Optimize database queries, reduce memory footprint, and enhance the overall speed of the web application, as routine continuous development.

---

Feel free to suggest any other features by opening an issue!

## Contributing

We welcome contributions to improve LeadsManager! To get started, please follow these steps:

1. Fork the repository and create your feature branch:

    ```bash
    git checkout -b feature/your-feature-name
    ```

2. Make your changes and ensure all tests pass.
3. Push your feature branch:

    ```bash
    git push origin feature/your-feature-name
    ```

4. Create a Pull Request.

For more detailed guidelines, please refer to [contributing.md](docs/contributing.md).

