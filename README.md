# Soteria

I tried structuring this project to allow easy collaboration, but any feedback
or update to the structure would be appreciated!

## Project Structure

- `/scripts` — Contains scripts to run the program and manage related tasks.
- `/tests` — Stores files for experimental code and tests. These files are not meant for production but serve as a space for testing out ideas and functionality.
- `/utils` — Holds all stable, working modules and utilities. Contributors are encouraged to create and place new functionalities in this folder.
- `.gitignore` — Lists files and folders to be excluded from version control.
- `main.py` — Contains the main program logic.

## Getting Started

### Step 0: Connecting to ESP32

If there are any problems in this step you could meet Daniella or ping me on Discord and I will walk you
through setting this up!

### Step 1: Set Up the Virtual Environment

Before running the program, please set up a virtual environment. This ensures all dependencies are isolated and prevents conflicts. You can do this with the following command:

```bash
python -m venv .venv
```

Alternatively, you may use any other virtual environment setup method you prefer. Once created, activate the virtual environment:

- On **Windows**: `.\.venv\Scripts\activate`
- On **macOS/Linux**: `source .venv/bin/activate`

### Step 2: Install Required Packages
After activating the virtual environment, install the required packages by running:

```bash
pip install -r requirements.txt
```
This will install all necessary dependencies listed in `requirements.txt` for the
project.

### Step 3: Running the Program

To start the main program, run the following command:

```bash
source scripts/start
```

The start script will:
- Update files on the ESP32
- Run the `main.py` file on the ESP32 device

**Note**: Ensure the ESP32 device is connected and accessible at the designated port (`COM6` by default).

### Step 4: Testing New Code (Optional)

You can add experimental scripts to the `/tests` folder. To test a new file, follow these steps:

1. Place the script in the `/tests` directory.
2. Update the `scripts/start` script to replace `main.py` with the path to your test file.
3. Run `source scripts/start` to execute your test file on the ESP32.

## Contribution Guidelines

- **New Functionalities**: Add new, stable functions or modules in the `/utils` folder.
- **Testing**: Use the `/tests` folder for experimental code. This keeps the main codebase clean and organized.
- **Scripts**: If updating the start script for custom testing, please revert to `main.py` after your test to maintain consistency.

## Example

To run the main program:
```bash
source scripts/start
```

To run a test script located at `/tests/my_test_script.py`:
1. Edit `scripts/start` to replace `main.py` with `/tests/my_test_script.py`.
2. Run:
   ```bash
   source scripts/start
   ```

**Note for Windows Users**: This script is written in Bash. To run it on Windows, you can use [Git Bash for Windows](https://git-scm.com/downloads/win), which provides a compatible environment for executing Bash scripts on a Windows system.