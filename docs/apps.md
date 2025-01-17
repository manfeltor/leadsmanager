# Apps documentation

---

## Table of Contents
- [LandingApp](#LandingApp-Technical-Documentation)
- [UsersApp](#UsersApp-Technical-Documentation)
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

## LandingApp Technical Documentation

## Overview
The landingapp is the entry point of the Leads Manager system. It serves as the home page and provides a dashboard with key lead statistics and insights. It includes authentication views and interactive visualizations for lead breakdowns, aiding users in analyzing lead data over time.

---

## Features

   ### Home Page:
        Displays a summary of lead data.
        Interactive graphs for lead analysis (e.g., bar plots and line plots).
   ### Custom Login:
        Custom user authentication page.
   ### Category Breakdown:
        Detailed lead breakdown view with trends and performance insights.

---

## Architecture and Workflow

   ### Home Page:

        Fetches and processes lead data from the database using Django ORM.
        Categorizes leads based on predefined mappings (group1_mapping and group2_mapping).
        Sends data to templates for visualization using Plotly.

   ### Login View:

        Authenticates users using Django's built-in authenticate() and login() functions.
        Redirects authenticated users to the home page.

   ### Category Breakdown:

        Provides a detailed view of leads filtered by customizable date ranges.
        Displays breakdowns by category and trends over time.

---

## Models

The landingapp does not define its own models. Instead, it relies on the FormSubmission model from the formsapp for fetching and processing lead data.

---

## Key Views/Functions

   ### base

    Description: Generates the home page with a summary of lead data.
    URL: /
    Key Logic:
        Fetches leads from the last 60 days by default.
        Categorizes leads into groups (e.g., "Contactos iniciales," "Leads activos") and calculates percentages.
        Prepares data for bar and pie charts displayed on the home page.

   ### custom_login_view

    Description: Custom login page for user authentication.
    URL: /customlogin
    Key Logic:
        Processes POST requests to authenticate users.
        Displays error messages for invalid login attempts.

   ### category_breakdown_view

    Description: Displays a detailed breakdown of lead categories with trends over time.
    URL: /category-breakdown/
    Key Logic:
        Filters leads by a configurable date range (default: last 60 days).
        Categorizes leads into groups and subcategories.
        Generates interactive bar and line plots using Plotly.

---

## Templates

   ### landing.html
        Displays the home page with lead statistics and interactive charts.
        Passes data for bar plots, pie charts, and percentages from the context.

   ### custom_login.html
        Renders the login page with a form and error messages.

   ### category_breakdown.html
        Provides a breakdown of lead categories with graphs and detailed insights.
        Includes modal windows for trend analysis and regression information.

---

## Integration Points

   ### FormsApp:
        Pulls lead data using the FormSubmission model for display on dashboards and breakdown views.
   ### UsersApp:
        Relies on user authentication for accessing views (e.g., @login_required).

---

## Custom Filters

 ### get_item

    Purpose: Fetches a value from a dictionary using a key.
    Usage: Used in templates to dynamically fetch data for graphs and percentages.

---

## Interactive Graphs

   ### Bar Plot (interactive_bar_plot):
        Visualizes lead percentages by category.
        Used in the home page and category breakdown views.

   ### Line Plot (interactive_line_plot):
        Shows trends in lead counts over time.
        Includes regression analysis for trendlines and R² values.

---

## Customization Points

   ### Date Range Configuration:
        Default date range for lead analysis is 60 days. This can be modified via the days_period parameter in views.
   ### Lead Mappings:
        group1_mapping and group2_mapping define how lead statuses are grouped. These mappings can be customized as needed.

---

## Known Issues and Limitations

    Graph Performance: Rendering large datasets in Plotly may impact performance. Consider server-side processing for larger datasets.
    Hardcoded Mappings: Lead mappings are defined statically in the views, which may require frequent updates if lead statuses change.
    Last entries pictures: The "last entries" section is trying to display null images, the picture rendering was an idea that migth end up deprecated.
    Undefined footer variables: management is still deciding on the links and text of this section.

---

## UsersApp Technical Documentation

### Overview

The usersapp is responsible for user authentication, profile management, and role-based access control. It enables administrators to manage users, assign roles, and define access permissions within the Leads Manager system.

---

## Features

   ### Authentication:

        Custom login/logout views.
        Role-based access control for different user types.

   ### User Management:

        Admins can create, edit, and delete users.
        Staff can assign roles and permissions.

   ### Profile Management:

        Users can update their profiles and change their passwords.

   ### Custom Roles:

        Supports hierarchical roles:
            Admin: Full access to all features.
            Manager: Manage users and leads.
            Employee: Restricted to assigned leads and basic features.

---

## Architecture and Workflow

   ### Authentication:

        Users log in via the custom login view.
        Django’s session framework is used to maintain user sessions.

   ### Role-Based Access:

        Permissions are enforced using decorators like @login_required, @staff_member_required, and custom role checks.

   ### Profile and Password Management:

        Profile updates and password changes are handled via forms with validation.
        User sessions are maintained after a password change using update_session_auth_hash.

   ### User Administration:

        Admins can view, create, edit, and delete users via dedicated views and forms.

---

## Models

   ### CustomUser

        Description: Extends Django’s AbstractUser to include additional fields and roles.
        Fields:
            phone_number: Stores the user’s phone number.
            role: Defines the user’s role (Admin, Manager, or Employee).
            company: Links the user to a company (ForeignKey to the Company model).
        Methods:
            is_management: Property that returns True if the user is a Manager or Admin.

   ### Company

        Description: Represents a company associated with users.
        Fields:
            name: Name of the company (unique).
            address: Address of the company.
            contact_email: Email for company contact.
            contact_phone: Phone number for the company.

   ### UserAttribute

        Description: Associates users with additional attributes.
        Fields:
            relacion: Defines the user’s relationship (Empleado or Cliente).
            comp: Links the user to a company (ForeignKey to the Company model).

---

## Key Views/Functions

   ### login_view

    Description: Custom login view for user authentication.
    URL: /users/login/
    Key Logic:
        Processes POST requests to authenticate users.
        Redirects authenticated users to the home page.
        Displays error messages for invalid credentials.

   ### user_list_view

    Description: Displays a list of all users.
    URL: /users/listusers/
    Key Logic:
        Retrieves all users using CustomUser.objects.all().
        Restricts access to authenticated users only.

   ### create_user_view

    Description: Allows Admin users to create new users.
    URL: /users/create_user/
    Key Logic:
        Uses CustomUserCreationForm for user creation.
        Validates input and saves new users to the database.

   ### update_profile_view

    Description: Allows users to update their profile information.
    URL: /users/updateprofile/
    Key Logic:
        Uses UserProfileUpdateForm to edit profile details.
        Displays success or error messages based on validation.

   ### change_password_view

    Description: Allows users to change their passwords.
    URL: /users/profile/change_password/
    Key Logic:
        Uses CustomPasswordChangeForm for password changes.
        Updates the session after a successful password change.

   ### delete_user

    Description: Allows Admin users to delete a user.
    URL: /users/delete-user/<int:user_id>/
    Key Logic:
        Requires staff permissions using @staff_member_required.
        Deletes the user from the database upon confirmation.

   ### functions_view

    Description: Renders a utility page for additional user functions.
    URL: /users/usersfuncs/

   ### send_mail_view

    Description: Processes bulk email sending via the Perfit API.
    URL: /users/usersfuncs/reclamosmailcorreoarg/
    Key Logic:
        Validates and processes an uploaded Excel file.
        Sends emails using mailfunc.main_func().

---

## Forms

   ### CustomUserCreationForm:
        Used for creating new users.
        Includes fields for username, role, company, and more.

   ### UserProfileUpdateForm:
        Used for editing user profile details.
        Includes fields like first_name, last_name, email, and phone_number.

   ### CustomPasswordChangeForm:
        Used for changing user passwords.
        Includes validation for new and old passwords.

   ### UserEditForm:
        Allows editing of user roles.
        Used in the user_edit_view.

---