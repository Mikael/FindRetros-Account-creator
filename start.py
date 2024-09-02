import os
import json
import requests
import random
import string
import time

def generate_random_email():
    domains = ["gmail.com", "yahoo.com", "hotmail.com"]
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{name}@{random.choice(domains)}"

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=length))

def generate_random_username():
    adjectives = ["Swift", "Silent", "Brave", "Clever", "Mighty", "Eager", "Bright"]
    nouns = ["Fox", "Wolf", "Lion", "Eagle", "Hawk", "Tiger", "Bear"]
    return random.choice(adjectives) + random.choice(nouns) + ''.join(random.choices(string.digits, k=4))

def get_random_proxy():
    with open("proxies.txt", "r") as file:
        proxies = [line.strip() for line in file.readlines() if line.strip()]
    proxy = random.choice(proxies)
    return {"http": proxy, "https": proxy}

def solve_captcha(site_key, url, capmonster_api_key, proxies):
    task_url = "https://api.capmonster.cloud/createTask"
    task_payload = {
        "clientKey": capmonster_api_key,
        "task": {
            "type": "RecaptchaV2TaskProxyless",
            "websiteURL": url,
            "websiteKey": site_key
        }
    }
    
    response = requests.post(task_url, json=task_payload, proxies=proxies)
    
    if response.status_code != 200:
        print(f"Error: Failed to create task. Status code: {response.status_code}, Response: {response.text}")
        return None
    
    response_json = response.json()
    task_id = response_json.get("taskId")
    if not task_id:
        print("Error: taskId not found in CapMonster response.")
        return None
    
    print(f"Task created successfully. Task ID: {task_id}")
    
    get_task_result_url = "https://api.capmonster.cloud/getTaskResult"
    result_payload = {
        "clientKey": capmonster_api_key,
        "taskId": task_id
    }
    
    while True:
        result_response = requests.post(get_task_result_url, json=result_payload, proxies=proxies)
        if result_response.status_code != 200:
            print(f"Error: Failed to get task result. Status code: {result_response.status_code}, Response: {result_response.text}")
            return None
        
        result = result_response.json()
        status = result.get("status")
        if status == "ready":
            solution = result.get("solution")
            g_recaptcha_response = solution.get("gRecaptchaResponse") if solution else None
            if g_recaptcha_response:
                print("CAPTCHA solved successfully.")
                print(f"g-recaptcha-response: {g_recaptcha_response}")
                return g_recaptcha_response
            else:
                print("Error: CAPTCHA solution not found.")
                return None
        elif status == "processing":
            print("Waiting for CAPTCHA task to be completed...")
            time.sleep(5)
        else:
            print(f"Error: Unexpected status {status} in CAPTCHA result.")
            return None

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
        "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    ]
    return random.choice(user_agents)

def register_account(session, username, email, password, captcha_response, token, proxies):
    url = "https://findretros.com/register"
    payload = {
        "_token": token,
        "name": username,
        "email": email,
        "password": password,
        "password_confirmation": password,
        "g-recaptcha-response": captcha_response
    }
    
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://findretros.com",
        "referer": "https://findretros.com/register",
        "user-agent": get_random_user_agent()
    }
    
    response = session.post(url, data=payload, headers=headers, proxies=proxies, allow_redirects=False)
    
    if response.status_code == 302:
        redirect_url = response.headers.get('Location')
        if redirect_url:
            redirect_response = session.get(redirect_url, proxies=proxies)
            if redirect_response.url == 'https://findretros.com/':
                return True
    return False

def append_account_to_file(file_path, username, password):
    if not os.path.isfile(file_path):
        print(f"File does not exist. Creating new file: {file_path}")
        with open(file_path, 'w') as file:
            json.dump([], file)
    
    try:
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error reading JSON file: {e}")
                data = []
        
        data.append({username: password})
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            print(f"Account details written to file: {file_path}")
    except IOError as e:
        print(f"Error reading or writing to file: {e}")

# Main function
def main():
    capmonster_api_key = "capmonster api key"
    site_key = "6LfawPkSAAAAABU4mJpZNLPAP7FqVKW5506oBuOf"
    registration_url = "https://findretros.com/register"
    
    proxies = get_random_proxy()

    session = requests.Session()

    registration_page = session.get(registration_url, headers={"user-agent": get_random_user_agent()}, proxies=proxies)
    
    print("Page content:")
    print(registration_page.text)
    
    token_start = registration_page.text.find('name="_token" value="') + len('name="_token" value="')
    token_end = registration_page.text.find('"', token_start)
    token = registration_page.text[token_start:token_end]
    
    if token:
        print(f"Token found: {token}")
    else:
        print("Token not found!")
        return

    username = generate_random_username()
    email = generate_random_email()
    password = generate_random_password()
    
    captcha_response = solve_captcha(site_key, registration_url, capmonster_api_key, proxies)
    if captcha_response:
        success = register_account(session, username, email, password, captcha_response, token, proxies)
        if success:
            print("Registration successful")
            append_account_to_file("accounts.json", username, password)
            print(f"New account details - Username: {username}, Password: {password}")
        else:
            print("Registration failed")
    else:
        print("CAPTCHA solving failed")

if __name__ == "__main__":
    main()
