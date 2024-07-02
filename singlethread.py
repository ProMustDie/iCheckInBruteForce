import requests

# URLs of the login page and form submission page
login_url = 'https://izone.sunway.edu.my/login'
form_url = 'https://izone.sunway.edu.my/icheckin/iCheckinNowWithCode'

# Credentials for login (replace with actual login credentials)
login_data = {
    'form_action': 'submitted',
    'student_uid': '', #enter userID
    'password': '', #enter password
    'g-captcha-response': ''
}

# Create a session object to persist cookies
session = requests.Session()

# Log in to the website
login_response = session.post(login_url, data=login_data)

# Check if login was successful by checking response status or some keyword in the response
if login_response.status_code == 200:
    print("Login successful!")

    # Loop through checkin codes from 00000 to 99999
    for code in range(100000):
        # Format the checkin code with leading zeros
        checkin_code = '{:05d}'.format(code)
        print(checkin_code)

        # Form data to be sent
        form_data = {
            'checkin_code': checkin_code
        }

        # Submit the form using the session
        response = session.post(form_url, data=form_data)

        # Check the response status
        if response.status_code == 200:
            # Check if the word "successfully" is in the response content
            if 'successfully' in response.text.lower():
                print("Form submitted successfully with code:", checkin_code)
                break  # Exit the loop if successful
        else:
            print("Failed to submit the form with code:", checkin_code)

    else:
        print("No valid checkin code found.")
else:
    print("Failed to log in. Status code:", login_response.status_code)