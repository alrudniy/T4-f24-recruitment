import requests

def post_to(url, params):
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, json=params)
    return response.json()

def main():
    # Test 1 Registration
    url_register = "http://127.0.0.1:5000/register"
    url_send_code = "http://127.0.0.1:5000/send_code"
    url_login = "http://127.0.0.1:5000/login_code"

    payload = {
        "phone": "1234567890",
        "username": "Username",
        "firstName": "First",
        "lastName": "Last",
        "email": "LastFirst@test.com",
        "password": "Password"
    }
    resp_json = post_to(url_register, payload)
    print(f"Test 1: {resp_json}")

    # Test 2 Duplication
    payload = {
        "phone": "1234567890",
        "username": "Username2",
        "firstName": "First2",
        "lastName": "Last2",
        "email": "LastFirst2@test.com",
        "password": "Password2"
    }

    resp_json = post_to(url_register, payload)
    print(f"Test 2: {resp_json}")

    # Test 3 send_code
    payload = {
        "phone": "1234567890",
    }
    resp_json = post_to(url_send_code, payload)
    print(f"Test 3: {resp_json}")
    valid_code = resp_json["v_code"]

    # Test 4 non-exist phone number
    payload = {
        "phone": "4008823823",
    }
    resp_json = post_to(url_send_code, payload)
    print(f"Test 4: {resp_json}")

    # Test 5 login
    payload = {
        "phone": "1234567890",
        "code": valid_code
    }
    resp_json = post_to(url_login, payload)
    print(f"Test 5: {resp_json}")

    # Test 6 wrong verification code
    payload = {
        "phone": "1234567890",
        "code": "123456"
    }
    resp_json = post_to(url_login, payload)
    print(f"Test 6: {resp_json}")

    # Test 7 Used code
    payload = {
        "phone": "1234567890",
        "code": "valid_code"
    }
    resp_json = post_to(url_login, payload)
    print(f"Test 7: {resp_json}")

if __name__ == "__main__":
    main()