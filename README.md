# CRM Project

## Overview
This Django CRM project is designed for efficient management of tickets and associates. The system accommodates two types of users: organizers and associates. Below is a brief overview of the key features and functionalities.

## Users
- **Organizers:** Organizers have the authority to create tickets, assign them to associates, and manage their own team of associates.
- **Associates:** Associates receive tickets from organizers, work on them, and update their status.

## Ticket Management
- Organizers create tickets and assign them to associates for execution.
- Each ticket is associated with a specific category, created by the organizer.
- Tickets can be categorized as "Assigned," "Work in Progress," "Processed," "Completed," or "Returned."
- Organizers can create follow-ups for tickets, adding extra documents or notes.

## Associate Management
- Organizers create associates, each with a unique email.
- Associates receive a registration email and use it to set their password on the CRM page.
- Associates can update the ticket category from "Assigned" to "Work in Progress."
- After completing a ticket, associates can set the category to "Processed."
- Organizers review completed tickets and set the final category to "Completed" or "Returned" if additional work is needed.

## Apps
The project consists of the following apps:
- **Tickets:** Handles CRUD operations for tickets.
- **Associates:** Manages associates, including their creation and password management.
- **Landing:** Serves as the home and dashboard of the CRM system.
- **Theme:** Integrates Tailwind CSS for a simple but responsive design.

## Setup
Follow these steps to set up and run the project:
1. Clone the repository: `git clone https://github.com/Artem1760/django-crm-project.git`
2. Navigate to the project directory: `cd <project-directory>`
3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```bash
        source venv/Scripts/activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
5. Install dependencies: `pip install -r requirements.txt`
6. Activate the provided PostgreSQL database:
    - Use password for db from .env file:    
    ```bash
    pg_restore --dbname=crm --username=djcrmuser --password=your_password ./crm_db.sql
    ```  
7. Set environment variables in the `.env` file (see below)
8. Apply migrations: `python manage.py migrate`
9. Run the development server: `python manage.py runserver`
10. Create a superuser to access the admin panel: `python manage.py createsuperuser`

### Environment Variables (.env)
Replace environment variables in the `.env` file in the project root with your preferred values.

## Usage
1. Access the CRM system at [http://localhost:8000/](http://localhost:8000/).
2. Log in as an organizer or associate.
3. Explore the dashboard, create tickets, manage associates, and track ticket statuses.

## Contributions
Feel free to contribute to the project by submitting issues or pull requests. Your feedback and improvements are highly appreciated.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Happy CRM managing!**
