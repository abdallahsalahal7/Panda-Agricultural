# Panda Agricultural
An Arabic plant shopping website

## Video Demo
https://youtu.be/DaelozgSyBo

## Description
Panda Agricultural is a simple web application that allows users to browse and buy plants in Arabic.
The main goal of the project is to provide an easy and accessible online shopping experience for plant lovers.
The website focuses on clarity, usability, and Arabic language support, making it suitable for local users.

This project was built as a practical solution rather than a theoretical one.
It simulates a real online store where users can view products, add them to a cart, and manage their selections.

---

## Why I Built This Project
I built this project because my uncle owns a plantation, but he does not have a website to sell his products online.
Most of his sales depend on local customers, which limits his reach.
By creating this website, I wanted to show how technology can help small agricultural businesses grow and connect with more people.

This project also allowed me to apply what I learned in CS50 in a real-world context.

---

## Technologies Used
The project uses several technologies that work together:

- **Python** with **Flask** for backend logic and routing
- **HTML, CSS, and Bootstrap** for building responsive and clean user interfaces
- **JavaScript** to handle cart interactions and quantity updates without reloading the page
- **SQLite3** as a lightweight and simple database solution

---

## Database Design
The database file is called `plant.db`.
It stores all user and plant information needed for the application.

### `users` table
- `id`: unique user ID
- `username`: unique username for login
- `hash`: hashed password for security

### `plants` table
- `id`: unique plant ID
- `name`: plant name stored in UTF-8 to support Arabic
- `price`: plant price
- `description`: detailed description of the plant in Arabic
- `image`: URL of the plant image

---

## Layout
The main layout file is `layout.html`, written in Arabic.
It contains the website logo and a navigation bar that allows users to move easily between pages.
The navigation bar includes links to plants, the shopping cart, login, registration, and logout.

Flash messages are used to display error messages and notifications in a clear way.

---

## User Registration
The registration page is `register.html`.
Users are required to enter a username, a password, and confirm their password.

In the `/register` route, the application:
- Verifies that all input fields are filled
- Checks that both passwords match
- Ensures the password is at least 8 characters long
- Stores the username and password hash securely in the database

---

## Login and Logout
The login page is `login.html`.
Users log in using their username and password.

The application verifies the credentials, creates a user session, and allows access to protected pages.
Logging out clears the session to keep the account secure.

---

## Homepage
The homepage (`index.html`) displays all available plants.
Each plant is presented using Bootstrap cards that adapt well to both mobile devices and desktop computers.

Plant data is fetched from the database and rendered using Jinja templates.

---

## Shopping Cart
The `/cart` route supports both GET and POST requests.

- A cart session is created automatically if it does not already exist
- Users can add plants to the cart or remove them at any time
- Plant details are retrieved from the database and shown in a table

The cart page displays:
- Plant name and price
- Quantity controls using JavaScript
- Total price for each item
- A grand total that updates automatically without refreshing the page
