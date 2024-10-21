# get-marvel-characters

Fetch a list of Marvel characters and the number of comics in which they have appeared. Download the list as a JSON or CSV file.

![diagram](https://github.com/user-attachments/assets/932f923f-8732-4c23-a13f-a28bee8669c6)


## Prerequisites

- Python 3.x installed on your machine.
- API Keys for Marvel Developer Portal 

## How to get a Marvel API key?

1. Go to the [Marvel Developer Portal](https://developer.marvel.com/).
2. Log in or sign up to the portal.
3. Click on 'Get a key'.
4. Create a new application and copy your public & private key.

## How to run the project

### Step 1: Clone this repository
```bash
git clone https://github.com/pablov-1995/get-marvel-characters/
cd get-marvel-characters
``` 
### Step 2: Create a Virtual Environment
```bash 
python3 -m .venv venv
```
### Step 3: Activate the Virtual Environment
- On Windows (Command Prompt):
``` bash
.\.venv\Scripts\activate
```
 - On Windows (PowerShell):
``` bash 
.\.venv\Scripts\Activate.ps1
```
 - On macOS/Linux (Bash/Zsh):

``` bash 
source .venv/bin/activate
```
### Step 4: Install Dependencies
```bash 
pip install -r requirements.txt
```
### Step 5: Create .env file from blueprint .env.example
You only need to fill in public & private key.

### Step 6: Run the Script
```bash
python main.py
```

## Arguments of the script
- use_multiprocessing (True, False; default = False): enable multiprocessing using the maximum number of available cores in your machine to speed up the API requests.

- output_format (csv, json; default = csv): specify the format you want to download the file as.

- file_name (default: marvel_output): name of the file containing the data.

Example:


```bash 
python main.py --use_multiprocessing=True --output_format=json ==file_name=marvel_characters
```
