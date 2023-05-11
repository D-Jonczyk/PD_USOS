# PD_USOS
Projekt USOS, Programowanie Defensywne

The University System for Managing Students is a web application developed to facilitate the management of students in a university setting. It provides various functionalities for administrators, faculty members, and students.

## Technologies Used

The project is built using the following technologies:

- **Django**: A Python web framework used for the backend development. Django provides a robust and scalable foundation for building web applications.
- **Django REST framework**: An extension of Django that simplifies the creation of RESTful APIs. It enables communication between the frontend and backend through API endpoints.
- **MySQL**: A popular relational database management system used for storing and managing the application's data.
- **Angular**: A powerful frontend framework based on TypeScript. Angular allows for the development of dynamic and interactive user interfaces.
- **Bootstrap**: A CSS framework used for designing responsive and visually appealing UI components. Bootstrap provides pre-built styles and components to enhance the application's user interface.

## Functionalities

The University System for Managing Students currently includes the following functionalities:

1. **User Authentication and Authorization**:
    - Users can create accounts, log in, and log out of the system securely.
    - Authentication and authorization are implemented using Auth0, ensuring secure access to the application.

2. **Student Management**:
    - Administrators can view, add, edit, and delete student records.
    - Students' information such as name, email, major, date of birth, and profile picture can be managed.

3. **Faculty Management**:
    - Administrators can manage faculty members' information, including their names, email addresses, departments, and contact details.

4. **Course Management**:
    - Faculty members can create, edit, and delete course records.
    - Courses can be assigned to specific faculty members.

5. **Admin Dashboard**:
    - Administrators have access to a dashboard that provides an overview of student and faculty information.
    - Various statistics and metrics are displayed to help administrators monitor and manage the university system effectively.

## Project Structure and Integration

The project follows a client-server architecture, with the Django backend serving as the RESTful API provider and the Angular frontend handling the user interface. The technologies are integrated as follows:

1. **Backend (Django)**:
    - Django handles the server-side logic and data management.
    - Django models define the database structure and provide an interface for interacting with the database.
    - The Django REST framework is used to create API endpoints that expose the application's data to the frontend.
    - API views and serializers handle the processing of requests and responses, ensuring data integrity and security.

2. **Frontend (Angular)**:
    - Angular is responsible for the presentation layer and user interface of the application.
    - Angular components render the UI elements and interact with the backend through API calls.
    - Services in Angular handle the communication with the backend API endpoints and provide data to the components.
    - Routing in Angular enables navigation between different views and components within the application.

The integration between Django and Angular allows for a scalable and modular approach to building the university management system. The separation of concerns enables efficient development, maintenance, and future enhancements of the application.

## Installation and Setup
**Backend (Django)**

1. Clone the repository:


   `git clone https://github.com/D-Jonczyk/PD_USOS.git`

2. Create and activate a virtual environment:


    `python3 -m venv env`

    `source env/bin/activate`

3. Install the Python dependencies:


    `pip install -r requirements.txt`

4. Create a MySQL database and update the database configuration in *APP_USOS/settings.py*

5. Apply database migrations:


    `python manage.py migrate`

6. Start the Django development server:


    `python manage.py runserver`

7. Django REST server is now running.

**Frontend (Angular)**

1. Navigate to the student-management-angular directory:


    `cd student-management-angular`

2. Install the required dependencies:


    `npm install`

3. Start the Angular development server:


    `ng serve`

4. Access the application at http://localhost:4200.
