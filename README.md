# SoftUni - Django Web Framework - Final Project

## Project Requrements:
Your Web application should use the following technologies, frameworks, and development techniques:
### General:
<ul>The application must be implemented using **Django Framework**
  -	The application must have at least **10 web pages**:
    -	Can be created using **function-based views** or/and **class based-views**;
    - At least **5 of them must be class-based views**.
  -	The application must have at least **5 independent models** (models created by extending, inheritance, and one-to-one relation is considered one model).
  -	The application must have at least **5 forms**.
  -	The application must have at least **5 templates**.
</ul>

2.	Use **PostgreSQL** as a **Database Service**.
  -	Optionally, you can use **multiple storages** (including PostgreSQL), e.g., files, other Web services, databases (e.g., **MySQL/MariaDB/Oracle** / etc.)

3.	Use **Django Template Engine** or make the **Front-End** using **JavaScript**.
4.	**Templates** (your views must return HTML files) - **the same template could be re-used/ used multiple times** (with the according to adjustments, if such needed).
5.	Implement **Web Page Design** based on **Bootstrap / Google Material Design**, or **design your own**.

-	The application must have login/register/logout functionality.
-	The application must have a public part (A part of the website, which is accessible by everyone - un/authenticated users and admins).
-	The application must have a private part (accessible only by authenticated users and admins).
-	The application must have a customized admin site (accessible only by admins):
  -	Add at least 5 custom options (in total) to the admin interface (e.g., filters, list display, ordering, etc.).

-	Unauthenticated users (public part) have only 'get' permissions, e.g., landing page, details, about page, and login/ register 'post' permissions.
-	Authenticated users (private part) have full CRUD for all their created content.
-	Admins - at least 2 groups of admins:
  -	One must have permission to do full CRUD functionalities (superusers); 
  -	The other/s have permission to do limited CRUD functionalities (staff).
  -	User roles could be manageable from the admin site.
  -	Make sure the role management is secured and error-safe.

-	Implement Exception Handling and Data Validation to avoid crashes when invalid data is entered 
(both client-side and server-side)
  -	When validating data, show appropriate messages to the user.
 
### Additional:
•	Follow the best practices for Object-Oriented design and high-quality code for the Web application:
  o	Use data encapsulation.
  o	Use exception handling properly.
  o	Use inheritance, abstraction, and polymorphism properly.
  o	Follow the principles of strong cohesion and loose coupling.
  o	Correctly format and structure your code, name your identifiers and make the code readable.

•	Well-looking user interface (UI).
•	Good user experience (UX).
•	Use a source control system by choice, e.g., GitHub, BitBucket.
  o	Submit a link to your public source code repository.

### Bonuses:
•	Write tests (Unit & Integration) for your views/models/forms - at least 10 tests
•	Writing asynchronous view/s somewhere in the project
•	Extend your Django project with REST Capabilities 
•	Extend Django user
•	Host the application in a cloud environment
•	Additional functionality, not explicitly described in this section, will be counted as a bonus if it has practical usage
