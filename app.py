from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import time
import os
import shutil

for root, dirs, files in os.walk('.', topdown=False):
    for name in dirs:
        if name == '__pycache__':
            shutil.rmtree(os.path.join(root, name))

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'your_secret_key'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'MySQL123'
app.config['MYSQL_DB'] = 'voting_app'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

mysql = MySQL(app)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Candidate Registration Route
@app.route('/register_candidate', methods=['GET', 'POST'])
def register_candidate():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        year = request.form['year']
        vision = request.form['vision']
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)
        image = request.files['image']
        filename = None
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO candidates (image, name, department, year, vision, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (filename, name, department, year, vision, username, hashed_password)
            )
            mysql.connection.commit()
            cur.close()
            flash('Candidate registered successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            print("Error during candidate registration:", e)
            flash('Error registering candidate. Please try again.', 'danger')

    return render_template('register_candidate.html')

@app.route('/')
def home():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, image, name, vision, username FROM candidates")
        candidates = cur.fetchall()
        cur.close()
    except Exception as e:
        print("Error fetching candidates:", e)
        candidates = []
    return render_template('home.html', candidates=candidates)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Example of checking credentials
        user = validate_user(username, password)  # Ensure this function exists and returns the user if valid
        
        if user:
            session['user_id'] = user.id  # Save user in session
            return redirect(url_for('candidate_dashboard'))
        else:
            return "Invalid credentials, please try again."
    return render_template('login.html')
@app.route('/login_candidate', methods=['POST'])
def login_candidate():
    candidate_username = request.form['candidate_username']
    candidate_password = request.form['candidate_password']
    print(f"Candidate Username: {candidate_username}")

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM candidates WHERE username=%s", (candidate_username,))
        candidate = cur.fetchone()
        cur.close()

        if candidate:
            print(f"Candidate Found: {candidate}")
            stored_password = candidate[7]  # Adjust based on DB structure

            if check_password_hash(stored_password, candidate_password):
                session['user_id'] = candidate[0]  # Set user ID in session
                flash('Logged in successfully as Candidate!', 'success')
                return redirect(url_for('candidate_dashboard'))
            else:
                flash('Invalid candidate credentials', 'danger')
                print("Password check failed")
        else:
            flash('Candidate not found', 'danger')
            print("Candidate not found")

    except Exception as e:
        print("Error during candidate login:", e)
        flash('Candidate login failed. Please try again.', 'danger')

    return redirect(url_for('login'))

# Function to fetch candidate data
def fetch_candidate_from_db(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM candidates WHERE id = %s", (user_id,))
        candidate = cur.fetchone()
        cur.close()
        return candidate
    except Exception as e:
        print("Error fetching candidate from database:", e)
        return None
# candidate_dashboard route
@app.route('/candidate_dashboard')
def candidate_dashboard():
    # Check if user_id is in session
    if 'user_id' not in session:
        flash('You must be logged in to access this page.', 'danger')
        return redirect(url_for('login'))
    
    # Fetch candidate data based on the user_id in session
    candidate = fetch_candidate_from_db(session['user_id'])
    
    # Handle case where candidate data is not found
    if candidate is None:
        flash('Candidate data not found', 'danger')
        return redirect(url_for('home'))
    
    # Pass the current time as a variable to the template
    return render_template('candidate_dashboard.html', candidate=candidate, cache_bust=time.time())
# Login helper function to validate user credentials
def validate_user(username, password):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password):  # Check stored password hash
            return user  # Return user details if authentication is successful
    except Exception as e:
        print("Error validating user:", e)
    return None


@app.route('/logout')
def logout():
    session.clear()  # Clear all session data to log out the user
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))  # Redirect to login page after logout

@app.route('/withdraw_candidate', methods=['POST'])
def withdraw_candidate():
    if 'user_id' not in session:  # Ensure user is logged in
        flash('You need to be logged in to withdraw.', 'danger')
        return redirect(url_for('login'))
    
    try:
        cur = mysql.connection.cursor()
        # Delete the candidate's record from the database using the session user_id
        cur.execute("DELETE FROM candidates WHERE id = %s", (session['user_id'],))
        mysql.connection.commit()
        cur.close()
        
        session.clear()  # Log the user out after withdrawal
        flash('You have successfully withdrawn from the election.', 'success')
        return redirect(url_for('home'))  # Redirect to home after successful withdrawal
    except Exception as e:
        print("Error withdrawing candidate:", e)
        flash('An error occurred. Please try again.', 'danger')
        return redirect(url_for('candidate_dashboard'))

@app.route('/login_user', methods=['POST'])
def login_user():
    username = request.form['username']
    registration_number = request.form['registration_number']  # Matches 'registration_number' column in the database

    try:
        cur = mysql.connection.cursor()
        # Fetch user from the database using the provided username and registration_number
        cur.execute("SELECT userid, username, registration_number FROM users WHERE username = %s AND registration_number = %s", (username, registration_number))
        user = cur.fetchone()
        cur.close()

        if user:
            # Store the user's ID in the session to track their login state
            session['user_id'] = user[0]  # userid column is at index 0
            flash("Logged in successfully!", "success")
            return redirect(url_for('vote'))
        else:
            flash("Invalid username or registration number. Please try again.", "danger")

    except Exception as e:
        print("Error during user login:", e)
        flash("An error occurred during login. Please try again.", "danger")

    return redirect(url_for('login'))  # Redirect back to login on failure

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'user_id' not in session:
        flash('Please log in to vote.', 'danger')
        return redirect(url_for('login'))

    user_id = session['user_id']

    try:
        conn = mysql.connection
        cursor = conn.cursor()

        # Fetch the username based on the user_id in session
        cursor.execute("SELECT username FROM users WHERE userid = %s", (user_id,))
        user = cursor.fetchone()
        username = user[0] if user else "Guest"  # Default to "Guest" if no user found

        # Check if the logged-in user has already voted
        cursor.execute("SELECT has_voted FROM users WHERE userid = %s", (user_id,))
        has_voted_result = cursor.fetchone()

        # Handle cases where the user is not found in the `users` table
        if not has_voted_result:
            flash("User not found. Please log in again.", 'danger')
            return redirect(url_for('login'))

        has_voted = has_voted_result[0]

        # Redirect if the user has already voted
        if has_voted:
            flash("You have already voted. Thank you!", 'info')
            return redirect(url_for('home'))

        cursor.execute("SELECT id, name, vision, image FROM candidates")
        candidates = cursor.fetchall()

        # Handle POST request to record the vote
        if request.method == 'POST':
            candidate_id = request.form['candidate_id']

            # Record the user's vote
            try:
                cursor.execute("INSERT INTO votes (candidate_id, user_id) VALUES (%s, %s)", (candidate_id, user_id))
                cursor.execute("UPDATE users SET has_voted = TRUE WHERE userid = %s", (user_id,))
                conn.commit()
                flash("Thank you for voting!", 'success')
                
                # Clear session to log out the user
                session.clear()
                
                return redirect(url_for('login'))
            except Exception as e:
                conn.rollback()
                flash("An error occurred while voting. Please try again.", 'danger')
                print("Error during vote recording:", e)

        cursor.close()
    except Exception as e:
        print("Database error:", e)
        flash("An internal server error occurred. Please try again later.", 'danger')

    # Pass the `username` to the template
    return render_template('vote.html', candidates=candidates, username=username)


@app.route('/results', methods=['GET', 'POST'])
def results():
    # Set developer password for accessing the results page
    developer_password = '12345'  # Replace with an actual secure password

    if request.method == 'POST':
        entered_password = request.form['password']

        # Verify entered password
        if entered_password == developer_password:
            try:
                cur = mysql.connection.cursor()

                # Fetch candidate names, registration numbers, and vote counts
                cur.execute("""
                    SELECT candidates.name, candidates.username, COUNT(votes.vote_id) AS vote_count
                    FROM votes
                    INNER JOIN candidates ON candidates.id = votes.candidate_id
                    GROUP BY candidates.id
                    ORDER BY vote_count DESC
                """)
                
                # Fetch all rows in descending order of vote count
                result_data = cur.fetchall()
                cur.close()
                
                # Render results with fetched data
                return render_template('result.html', results=result_data)
            except Exception as e:
                print("Error fetching results:", e)
                flash("An error occurred while fetching results. Please try again later.", 'danger')
                return redirect(url_for('results'))
        else:
            flash('Incorrect password. Access denied.', 'danger')
    
    # Render password entry form for the GET request
    return render_template('password_entry.html')


if __name__ == '__main__':
    app.run(debug=True)
