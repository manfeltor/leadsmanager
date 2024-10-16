# System Architecture

## 1. Overview of the Architecture

The LeadsManager system is built using a microservices-oriented architecture, leveraging Django as the core backend, Celery for task automation, and a MySQL database for data persistence. The entire system is containerized using Docker and deployed on **Google Cloud Run**, with Redis acting as a message broker for Celery tasks.

![System Architecture Diagram](path/to/diagram.png) <!-- Add your Visio or draw.io diagram here -->

### Key Components:
- **Django (Backend)**: Core logic and request handling.
- **MySQL (Database)**: Stores leads, users, form submissions, and status updates.
- **Redis (Task Queue)**: Manages Celery tasks.
- **Celery (Task Manager)**: Automates background processes like sending emails and lead status updates.
- **Google Cloud Run**: Manages containerized deployment for the web and worker services.

---

## 2. Component Breakdown

### 2.1 Frontend (UI)

LeadsManager relies on Django templates and the Django admin interface for its frontend user interface. The frontend is not a complex, single-page application but a traditional server-rendered interface using Django’s templating engine.

#### Key User Interactions:

- **Form Submissions:**
  - Users can submit data via web forms, integrated from external sources, or manually through a dedicated submission page.
  - These forms capture key information such as customer details, service inquiries, and contact information.
  - The captured data is processed and stored in the database, where it can be viewed and managed by authorized users (e.g., managers and admins).

- **Admin/management features on Interface:**
  - The Django admin panel allows administrators to view, edit, and manage users and roles.
  - Role-based access ensures that only users with the appropriate permissions (e.g., admins or managers) can modify critical data.
  - Through this interface, users can filter leads, update statuses, and monitor progress.

- **Django Templates:**
  - The application utilizes Django’s templating system to render HTML pages.
  - Each lead submission form is rendered as a template, with user input fields for lead details such as name, email, phone number, service, etc.
  - The templates are styled using basic CSS frameworks (e.g., W3CSS) and rendered dynamically based on user interactions and form submissions.

- **Error Handling and Feedback:**
  - If a form submission fails (e.g., validation errors), the user receives feedback within the same interface, prompting corrections.
  - Success and error messages are displayed using Django’s built-in messaging framework.

#### Future Considerations:

- The UI could be further enhanced by integrating a more dynamic, JavaScript-driven frontend to improve user experience, such as real-time form validation or dashboard analytics for lead performance. This evaluations will come as a next step once the project is stabilized with the last required modifications.

### 2.2 **Backend (Django)**

The backend of **LeadsManager** is built using the **Django framework**. It handles the core functionality of the application, such as managing leads, handling form submissions, user authentication, and task automation with Celery.

#### 2.2.1 **Key Django Components**

- **Models**: 
  Django models represent the data structure of the application. The main models include:
  - `FormSubmission`: Stores information about each lead submission, such as customer details, service inquiries, status, and the assigned user.
  - `CustomUser`: Extends Django’s default user model to include additional fields such as phone number and role (e.g., employee, manager).
  - `LeadHistory`: Tracks changes in the status of leads, allowing the system to maintain an audit trail of lead progress.

- **Views**:
  - The views in the application handle HTTP requests and return appropriate HTTP responses. There are several types of views, including:
    - `forms_list_view`: Displays a list of all form submissions for admin users.
    - `form_edit_view`: Allows managers or admins to edit the details of a lead, such as updating the status or assigning a user.
    - `manual_form_submission_view`: A dedicated view for manually submitting lead data into the system.

- **Templates**:
  - The application uses Django's templating engine to render HTML pages. Each view is tied to a corresponding template (e.g., `form_detail.html`, `list_forms_submissions.html`), allowing dynamic content rendering based on the data passed from views mainly using inheritance and block mutations from a base template.
  
#### 2.2.2 **Task Management (Celery)**

LeadsManager uses **Celery** for background task processing. Key tasks include:
- **Automated Follow-ups**: Background tasks can be scheduled to send email reminders for pending leads.
- **Data Synchronization**: Periodic tasks fetch new lead submissions from external sources (e.g., web forms) and update the local database.

Celery integrates with **Redis** as the message broker to queue tasks for asynchronous execution.

**Note**: The Celery workers are currently tested in the development environment but not yet deployed to production. Stakeholders may still request changes to the task automation, so full implementation will occur after approval.

#### 2.2.3 **Database Management**

- The application uses **MySQL** as the relational database to store lead and user data.
- Django's **ORM** (Object-Relational Mapping) is used to interact with the database. This simplifies data retrieval, insertion, and updates without requiring raw SQL queries.
- Migrations are handled using Django’s built-in migration framework, allowing seamless updates to the database schema as the project evolves.

#### 2.2.4 **APIs**

LeadsManager includes a set of **RESTful APIs** for interacting with external systems. These APIs allow:
- Submission of lead data from external forms.
- Retrieval of lead data for integration with reporting or external CRM systems.
- User authentication and permission validation through Django’s built-in authentication system.

#### 2.2.5 **Security & Authentication**

- User authentication is handled by **Django's authentication system**, which supports role-based access control (RBAC). Users are categorized into different roles:
  - **Admin**: Full access to all features and management of the system.
  - **Manager**: Can manage leads and view reports but has limited access to system settings.
  - **Employee**: Restricted to managing personal leads and viewing limited data.

All sensitive data such as API keys and database credentials are securely managed using **Google Cloud Secrets Manager** and injected into the application as environment variables, or env files for development.
  
### 2.3 **Task Queue (Celery)**:
- Celery is responsible for handling background tasks, reducing load on the web app by processing long-running tasks asynchronously.
  - **Tasks**: Automated emails, status updates, and database consistency checks.
  - **Integration**: Celery integrates with Redis to queue and manage tasks.
  
  **Note**: The Celery workers are currently tested in the development environment but not yet deployed to production. Stakeholders may still request changes to the task automation, so full implementation will occur after approval.
  
### 2.4 **Database (MySQL)**:
- **Schema**: Relational database with key models:
  - `CustomUser`: Stores user data and permissions.
  - `FormSubmission`: Tracks all leads submitted via forms.
  - `LeadHistory`: Logs updates to lead status over time.
  
### 2.5 **Message Broker (Redis)**:
- Redis acts as the intermediary between Django and Celery, allowing tasks to be queued and processed in the background.
  - **Queue Management**: Redis stores tasks and passes them to Celery workers for processing.

  **Note**: The Celery workers are currently tested in the development environment but not yet deployed to production. Stakeholders may still request changes to the task automation, so full implementation will occur after approval.
  
### 2.6 **Containerization (Docker)**:
- Docker is used to containerize the Django web app, Celery workers, and Redis for easy deployment and scalability.
- **Docker Services**:
  - Web (Django + Gunicorn)
  - Celery Worker
  - Celery Beat (for periodic tasks)

---

## 3. Data Flow

### 3.1 **Form Submission**:
1. A INTRALOG pages visitor submits a lead via a web form on the main INTRALOG page, or the sales/mkt team member submits via leadsmanager interface.
2. Django processes the submission:
    - Fetches the new form from a custom plugin developed specifically to retrieve form submissions by form id (various forms across pages).
    - Validates the form data.
    - Normalize, consolidate and store data in the `FormSubmission` table, a single forms database to centralize info.
    - Logs any status or change of assigned user modifications..
3. Celery is triggered to:
    - Send a confirmation email to the user. (this feature is under evaluation by upper management)
    - Notify the sales team via Slack or email (email API already developed. Waiting for MKT and commercial teams to define triggers and nature of notifications).
4. The submission appears in the lead management dashboard and/or in the logged users assigned leads page.

### 3.2 **Lead Management**:
1. A manager or admin accesses the lead via the Django Admin dashboard.
2. Updates the lead status and assigns the lead to a team member.
3. Lead updates are logged in the `LeadHistory` table.
4. Task automation (via Celery) updates the status or sends notifications as necessary. (this feature is under evaluation by upper management)

---

## 4. External Integrations

### 4.1 **Email API**:
- The application integrates with Perfit external email service to send notifications and updates to internal users.
- Email notifications are triggered by Celery tasks (e.g., upon lead submission, status change).

### 4.2 **WP custom API**:
- To solve the differences across forms from different pages, a custom plugin was developed on WP panel to retrieve submissions by form id

### 4.3 **Google Cloud SQL**:
- In production, MySQL is hosted on **Google Cloud SQL**, with native integration to **Google Cloud Run** for secure access.
- Django ORM handles migrations and interactions with the database.

### 4.4 **Google Cloud Secrets**:
- **Environment Variables**: All sensitive data (e.g., database credentials, API keys) is stored in **Google Cloud Secrets** and injected as environment variables into the Google Cloud Run container.

---

## 5. Scaling and Performance

### 5.1 **Horizontal Scaling**:
- **Google Cloud Run**: Scales horizontally based on traffic demand. Each service (web, Celery worker) can be scaled independently based on load.
- **Celery Workers**: More Celery workers can be added to handle increased background tasks without affecting the web performance.

### 5.2 **CI/CD Pipeline**:
- Future versions will leverage GitLab CI/CD (or GitHub Actions) for automated testing and deployment.
- Each push to the `main` branch will trigger a new Docker image build and redeployment to Google Cloud Run.

### 5.3 **Monitoring**:
- **Google Cloud Logging**: Application logs are monitored using Google Cloud’s integrated logging service.
- **Celery Monitoring**: Track task completion, failures, and worker status via the Celery monitoring tools with custom critical log in.

---

## 6. Security Considerations

### 6.1 **Environment Variables**:
- All sensitive data (such as API keys, database credentials) is stored securely in **Google Cloud Secrets Manager** and accessed as environment variables.

### 6.2 **IAM Roles**:
- **Google Cloud IAM**: Role-based access control ensures that only authorized users and services can access critical resources (e.g., Cloud SQL, Redis).
- **Celery Security**: Only authenticated users with proper roles (managers, admins) can trigger certain Celery tasks.

### 6.3 **Data Encryption**:
- **Database Encryption**: Google Cloud SQL ensures that all data at rest is encrypted.
- **HTTPS/SSL**: All web traffic to the application is encrypted via HTTPS.

### 6.4 **User Authentication**
- **Django Authentication System**: Manages user logins and sessions, ensuring secure access to the application.
- **Role-Based Access Control**: Permissions are assigned based on user roles (Admin, Manager, Employee), limiting access to sensitive data.

---

## 7. Future Enhancements / Roadmap
- Implement advanced lead analytics with machine learning models.
- Optimize sales rep XP with personalized workbench interfaces and self/self-leads performance and status dashboards.
- Transition Celery to a FastAPI-based microservice.
- Optimize real-time task management with enhanced dashboards.
- Enhance UI for better UX with modern front-end architecture (possibly using a React microservice fed by API interactions with the main engine).
- Manage microservices orchestration and app health management with Google Kubernetes Engine.

---

## Diagrams

Under construction.