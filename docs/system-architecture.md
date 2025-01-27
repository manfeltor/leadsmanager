# System Architecture

## 1. Overview

The LeadsManager project is a comprehensive web-based lead management system. 
It integrates various components to provide a seamless experience for tracking, managing, and analyzing leads. 
The architecture is designed for scalability, modularity, and ease of integration with external services such as APIs and bulk email systems.

<!-- ![System Architecture Diagram](path/to/diagram.png) -->

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

## High-Level Architecture

                       +---------------------+
                       |  External Systems  |
                       |  (WordPress API,   |
                       |   Perfit, etc.)    |
                       +---------+----------+
                                 |
                                 v
+-------------------------------+-------------------------------+
|                               |                               |
|       Backend Services        |           Frontend            |
|  (Django Framework)           |  (HTML, CSS, JS, W3.CSS)     |
|                               |                               |
+-------------------------------+-------------------------------+
                                 |
                                 v
                      +-------------------------+
                      |     Database Layer      |
                      |       (MySQL)          |
                      +-------------------------+
                                 |
                                 v
                      +-------------------------+
                      |     Task Management     |
                      | (Celery + Redis Queue)  |
                      +-------------------------+

---

## Components

### Frontend

**Frameworks/Libraries:**
- HTML
- W3.CSS for styling
- JavaScript for interactivity

**Responsibilities:**
- Render user interfaces for dashboard, forms, and reports.
- Display interactive graphs for lead analysis (via Plotly).
- Enable dynamic filtering of leads and other data.

---

## Backend

**Framework:** Django 5.x

**Structure:**
- Modular apps: landingapp, usersapp, formsapp
- RESTful API endpoints for data interaction (future planned feature)

**Responsibilities:**
- Process user requests and serve appropriate views.
- Handle role-based access control for secure operations.
- Integrate with external APIs for lead data and email services.
- Implement business logic for lead tracking, submission, and updates.

## Components

### Frontend

**Frameworks/Libraries:**
- HTML
- W3.CSS for styling
- JavaScript for interactivity

**Responsibilities:**
- Render user interfaces for dashboard, forms, and reports.
- Display interactive graphs for lead analysis (via Plotly).
- Enable dynamic filtering of leads and other data.

### Backend

**Framework:** Django 5.x

**Structure:**
- Modular apps: landingapp, usersapp, formsapp
- RESTful API endpoints for data interaction (future planned feature)

**Responsibilities:**
- Process user requests and serve appropriate views.
- Handle role-based access control for secure operations.
- Integrate with external APIs for lead data and email services.
- Implement business logic for lead tracking, submission, and updates.

### Database

**Database Management System:** MySQL

**Schema Overview:**
- Users Table: Handles user data and role management.
- Form Submissions Table: Stores lead data and history.
- Lead History Table: Tracks status changes for leads.
- Campaigns Table: Stores campaign-related metadata.

### External Integrations

**WordPress API:**
- Fetches lead submissions from a custom WordPress plugin.
- Authenticated via WPUSER and WPPASS environment variables.

**Perfit Mail API:**
- Sends bulk emails for operations teams.
- Integrated via PRFTAPIKEY.

---

## Data Flow

