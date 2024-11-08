# Class Representative Election Portal

This is a web application built using Flask and HTML/CSS for managing and conducting a Class Representative (CR) election. The platform allows students to register as candidates, vote for their preferred candidate, and view election results. It also provides a secure login system for users and candidates.

## Features

- **User Login**: Users can log in with their registration number to vote in the election.
- **Candidate Registration**: Candidates can register with their details, including vision statements, image, department, year, and a password for login.
- **Voting System**: Registered users can vote for candidates, view their profiles, and submit their votes securely.
- **Admin Features**: The department can verify candidate details, and a password-protected results page allows for viewing the final vote count.
- **Responsive Design**: The app is designed to be mobile-friendly and includes dynamic components for a seamless experience.

## Pages

1. **Home Page**: Displays the election portal with options to log in, register as a candidate, and view results.
2. **Candidate Dashboard**: Displays the details of the logged-in candidate and an option to withdraw from the election.
3. **Login Page**: Provides login options for both users and candidates.
4. **Candidate Registration**: A form for students to register as a candidate, uploading their image and providing other necessary details.
5. **Election Results**: A password-protected page where election results can be viewed once the election ends.
6. **Voting Page**: Allows users to view the list of candidates and vote for their preferred representative.

## Technologies Used

- **Frontend**: HTML, CSS
- **Backend**: Flask (Python)
- **Database**: SQLite (or any other preferred database for storing user, candidate, and voting data)
- **Styling**: Custom CSS with glassmorphism design elements.

## `database.py` File

The `database.py` file is used to set up and manage the database required for the application. It automatically creates the necessary tables based on the needs of the Flask application. This includes tables for users, candidates, votes, and election-related data. You can modify this file to add or alter tables as needed.

To initialize the database, simply run the `database.py` script:

```bash
python database.py


## Installation

To run the project locally:

1. Clone the repository:

    ```bash
    git clone https://github.com/Imkkrish/class-representative-election-portal.git
    ```

2. Navigate to the project directory:

    ```bash
    cd class-representative-election-portal
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask application:

    ```bash
    python app.py
    ```

5. Open a web browser and go to `http://127.0.0.1:5000` to access the application.

## Contributing

Feel free to fork this project, submit issues, or create pull requests. Any contributions are welcome!

## License

This project is licensed under the MIT License.
