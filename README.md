# Registration Automation Script

## Overview

This Python script automates the process of creating accounts on findretros using a combination of random data generation, CAPTCHA solving, and HTTP requests. It uses CapMonster to solve CAPTCHA challenges, handles HTTP requests for registration, and manages user credentials by saving them to a file.

**Note:** This script is intended for educational purposes only. Use it responsibly and ensure you comply with the terms of service of any website you interact with.

## Features

- **Random Data Generation:** Automatically generates random usernames, emails, and passwords.
- **CAPTCHA Solving:** Uses CapMonster's API to solve CAPTCHA challenges.
- **HTTP Requests:** Handles HTTP requests to register accounts and follow redirects.
- **Data Storage:** Saves successfully registered account details to a JSON file.

## Configuration

1. **CapMonster API Key:**

   Edit the `main()` function in the script and replace `"capmonster api key"` with your actual CapMonster API key:

   ```python
   capmonster_api_key = "your_capmonster_api_key_here"
   ```
2. Prepare Proxies:

Create a file named proxies.txt in the same directory as the script. List each proxy on a new line in the format:
```
http://username:password@proxyserver:port
```
or
```
http://proxyserver:port
```
## Running the Script
```
python start.py
```
## The script will:

1. Load proxies from proxies.txt.
2. Fetch the registration page and extract the necessary token.
3. Generate random user data (username, email, password).
4. Solve the CAPTCHA using CapMonster.
5. Attempt to register the account with the generated data.
6. Save the registered account details to accounts.json if successful.
## Important Notes
***Educational Purposes Only***: This script is designed for educational use and should not be used for spamming or malicious activities. Always adhere to the terms of service of the website you are interacting with.
**API Key**: Ensure you have a valid CapMonster API key to solve CAPTCHA challenges.
**Proxy Handling**: Make sure your proxies are properly configured and valid.
## License
This project is licensed under the MIT License. See the [LICENSE](https://en.wikipedia.org/wiki/MIT_License) file for details.
```
Copyright (c) <2024> <Mikael>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.```
