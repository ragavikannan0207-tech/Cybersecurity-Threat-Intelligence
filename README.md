# Cybersecurity Threat Intelligence Database

A full-stack cybersecurity web application built with **Python, Flask, MySQL, SQLAlchemy, HTML, CSS, and JavaScript**. It allows users to report suspicious cyber activity and authorized analysts to investigate reports, manage threat intelligence, and maintain a database of verified threats.

This project is designed as an educational cybersecurity application.

---

## 1. Project Overview

Cybersecurity threats such as phishing websites, suspicious IP addresses, malware indicators, and online scams can be difficult to track. This project provides a centralized platform to collect reports, investigate suspicious activity, and maintain threat intelligence records.

The application has two main types of users:

### Public Users

- Browse the public homepage.
- Submit suspicious cyber activity reports without creating an account.
- Create an account and sign in.
- View their submitted reports.
- Delete their own reports where permitted by the application.
- View available threat information and alerts provided by the application.

### Authorized Analysts

- Sign in through the separate analyst login.
- View and search submitted reports.
- Investigate suspicious activity.
- Review possible matches against existing threat records.
- Add investigation notes and assessments.
- Manage threat intelligence records.
- Create, view, search, update, and delete threat records.
- Maintain audit logs of analyst actions.

**Important:** A submitted report is not automatically considered a confirmed threat. Analysts must evaluate the available evidence before treating a threat as verified.

---

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask 3 | Web application framework |
| MySQL 8.0+ | Relational database |
| PyMySQL | Python-to-MySQL database driver |
| SQLAlchemy | Database ORM and queries |
| Jinja2 | Dynamic HTML templates |
| HTML5 | Web page structure |
| CSS3 | Styling and responsive layout |
| JavaScript | Frontend interactions |
| Werkzeug | Password hashing and authentication utilities |
| Flask-WTF / WTForms | Form validation and CSRF protection |
| pytest | Automated testing |
| Visual Studio Code | Code editor |

The exact Python packages are listed in `requirements.txt` and are installed during setup.

---

## 3. Features

- Public threat-report submission without mandatory registration.
- Public user registration, login, and account management.
- Separate analyst authentication and authorization.
- Threat-report investigation and assessment.
- Evidence-only indicator matching against existing threat records.
- Threat intelligence CRUD operations.
- Search, filtering, and sorting.
- Report references and submission status.
- Analyst audit logging.
- SQLite support for local development and testing.
- MySQL support for a full database setup.

---

# 4. Windows Setup: Step-by-Step Guide

Follow these instructions from the beginning if you are setting up the project on a new Windows computer.

## Step 1: Download the project from GitHub

1. Open the GitHub repository shared by the project owner.
2. Click the green **Code** button.
3. Select **Download ZIP**.
4. Wait for the ZIP file to download.
5. Open your Windows Downloads folder.
6. Right-click the downloaded ZIP file.
7. Select **Extract All**.
8. Choose a convenient location, such as your Desktop.
9. Click **Extract**.

You should now have a project folder containing files such as:

```text
CYBERSECURITY THREAT PROJECT/
│
├── app/
├── database/
│   ├── migrations/
│   ├── schema.sql
│   └── sample_data.sql
├── migrations/
├── tests/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

Your extracted folder may have a slightly different name.

**Important:** The `.env` file and the local SQLite preview database are intentionally not included in the GitHub download. You will create your own configuration.

## Step 2: Install Python

1. Open the official Python website:

   https://www.python.org/downloads/windows/

2. Download a Python version compatible with the project's dependencies.
3. Run the installer.
4. On the first installation screen, select **Add Python to PATH** if that option is available.
5. Complete the installation.

Open Command Prompt or PowerShell and check the installation:

```powershell
py --version
```

Then check pip:

```powershell
py -m pip --version
```

Both commands should display version information.

If `py` is not recognized, reopen the terminal or repair the Python installation and PATH configuration.

## Step 3: Install Visual Studio Code

1. Open:

   https://code.visualstudio.com/

2. Download Visual Studio Code for Windows.
3. Install it using the default options.
4. Launch Visual Studio Code.

### Install the Python extension

1. Click the Extensions icon on the left side of VS Code.
2. Search for **Python**.
3. Install the Python extension published by Microsoft.

The Python extension helps VS Code select interpreters, run Python code, and provide code assistance.

## Step 4: Open the extracted project folder

1. Open VS Code.
2. Select **File → Open Folder**.
3. Navigate to the folder extracted in Step 1.
4. Select the project folder containing `run.py` and `requirements.txt`.
5. Click **Open**.
6. If VS Code asks whether you trust the folder, verify that it came from the expected repository before trusting it.

Do not open only the `app` folder. Open the main project folder.

## Step 5: Install MySQL Server

MySQL stores the project's users, analysts, reports, investigations, threats, and audit records.

1. Open the official MySQL Installer page:

   https://dev.mysql.com/downloads/installer/

2. Download the MySQL Installer for Windows.
3. Run the installer.
4. Select a setup type that includes **MySQL Server 8.0 or a compatible supported version**.
5. Follow the installation wizard.
6. Configure MySQL Server to run locally.
7. Set a strong password for the MySQL administrative account.
8. Remember that password securely.

You do not need to expose MySQL to the internet. For this project, a local database is sufficient.

## Step 6: Install MySQL Workbench

MySQL Workbench provides a graphical interface for managing the database.

1. Open:

   https://dev.mysql.com/downloads/workbench/

2. Download and install MySQL Workbench if it was not installed with MySQL Server.
3. Open Workbench.
4. Connect to the local MySQL Server using the credentials configured during installation.

If Workbench connects successfully, continue to the next step.

## Step 7: Create the project database

In MySQL Workbench, open a new SQL query tab and execute:

```sql
CREATE DATABASE ThreatIntelDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

This creates an empty database for the application.

### Create a dedicated database user

For a local development setup, execute the following SQL after choosing your own strong password:

```sql
CREATE USER 'threatuser'@'localhost'
IDENTIFIED BY 'REPLACE_WITH_YOUR_OWN_STRONG_PASSWORD';

GRANT ALL PRIVILEGES ON ThreatIntelDB.*
TO 'threatuser'@'localhost';
```

Replace the example password with your own password before executing the SQL.

These commands are intended for a fresh setup. If the database or user already exists, inspect the existing configuration rather than blindly rerunning the commands.

## Step 8: Create the Python virtual environment

In VS Code, select **Terminal → New Terminal**.

Make sure the terminal is inside the project root directory.

Create a virtual environment:

```powershell
py -m venv .venv
```

This creates an isolated Python environment for the project.

### Activate the environment

In PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, you can instead open Command Prompt in VS Code and run:

```bat
.venv\Scripts\activate.bat
```

Alternatively, if you choose to change the PowerShell execution policy, understand the implications and use an appropriate policy for your machine.

After activation, the terminal prompt will normally show `(.venv)`.

## Step 9: Install the required Python packages

With the virtual environment activated, run:

```powershell
python -m pip install --upgrade pip
```

Then install the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Wait until installation finishes.

This installs the packages listed in `requirements.txt`, including the Flask application dependencies and MySQL driver specified by the project.

Do not install packages individually unless you encounter a specific dependency issue.

## Step 10: Create your local `.env` configuration

The `.env` file stores your local database connection and application settings.

A safe template named `.env.example` is included in the project.

From the project root, run:

```powershell
Copy-Item .env.example .env
```

Open `.env` in VS Code.

Configure it using the variable names expected by the application. For example:

```dotenv
SECRET_KEY=REPLACE_WITH_A_RANDOM_SECRET
DATABASE_URL=mysql+pymysql://threatuser:URL_ENCODED_PASSWORD@127.0.0.1:3306/ThreatIntelDB?charset=utf8mb4
SESSION_COOKIE_SECURE=false
FLASK_DEBUG=false
```

Replace the example secret and database password with your own values.

Important configuration notes:

- `SECRET_KEY` must be a strong, private random value.
- `DATABASE_URL` must match the database user, password, host, port, and database created above.
- URL-encode special characters in the database password when required by the URL format.
- `SESSION_COOKIE_SECURE=false` is suitable only for local HTTP development. Use HTTPS and secure cookie settings for deployment.
- Keep `.env` private. Never upload it to GitHub.

If the project's `.env.example` contains additional settings required by the current code, preserve those settings.

## Step 11: Initialize the database tables

Before starting the application, create the required tables.

For a new database, first inspect `database/schema.sql` and the database setup instructions in this README.

The project provides a MySQL schema file:

```text
database/schema.sql
```

You can load it in MySQL Workbench by opening the file and executing its SQL against `ThreatIntelDB`, or by using the MySQL command-line client.

If the project is configured to use Flask's SQLAlchemy initialization command, the documented command is:

```powershell
python -m flask --app run.py init-db
```

For an existing database that needs missing tables or supported columns added, use:

```powershell
python -m flask --app run.py migrate-db
```

**Do not blindly execute both the schema file and initialization commands against an existing database.** Inspect the current schema and use the appropriate setup path. Do not drop or reset a database containing records you need to preserve.

### Optional: Load sample data

The project includes:

```text
database/sample_data.sql
```

This file contains illustrative sample rows.

Review the file before executing it. Load it only after the schema exists, and only if you want sample records for demonstration. Do not load sample data repeatedly into a database with existing records without checking for duplicate or conflicting rows.

## Step 12: Create an analyst account

The application keeps public users and analysts separate.

Create an analyst account using the project's supported CLI command:

```powershell
python -m flask --app run.py create-analyst --username yourname
```

If the CLI supports interactive password entry, follow the prompts to set a strong password. If the command requires a password argument, follow the syntax documented by the actual CLI implementation.

Do not use a default production password or share your private analyst password in a public repository.

## Step 13: Start the application

Ensure that:

- MySQL Server is running.
- Your `.env` contains the correct connection details.
- The virtual environment is activated.
- The database schema has been initialized.

Then run:

```powershell
python run.py
```

Alternatively, if the Flask CLI entry point is supported:

```powershell
python -m flask --app run.py run --host 127.0.0.1 --port 5000
```

Wait for Flask to report that the development server is running.

## Step 14: Open the website

Open your browser and visit:

**Homepage**

http://127.0.0.1:5000/

**Public registration**

http://127.0.0.1:5000/users/register

**Public login**

http://127.0.0.1:5000/users/login

**Anonymous threat reporting**

http://127.0.0.1:5000/reports/new

**Analyst login**

http://127.0.0.1:5000/auth/login

**Threat intelligence**

http://127.0.0.1:5000/threats/

Sign in using the analyst account created in Step 12 to access analyst-only features.

---

# 5. Running Automated Tests

The project includes a `tests/` directory containing automated tests.

To run the test suite, activate the virtual environment and execute:

```powershell
python -m pytest -q
```

The tests are designed to use SQLite in-memory databases where configured, so a running MySQL server should not be required for those tests.

Use the actual test output to determine whether the suite passed.

---

# 6. Database Configuration Explained

The application can use different databases depending on its configuration.

### MySQL database

Use MySQL for the Windows setup described in this guide.

The application connects using `DATABASE_URL` in `.env`.

Example format:

```text
mysql+pymysql://USERNAME:PASSWORD@HOST:3306/DATABASE_NAME
```

### SQLite preview database

SQLite can be used for local development when the application is configured for SQLite.

For example:

```dotenv
DATABASE_URL=sqlite:///preview.db
```

In this project, the relative SQLite path may resolve to a file under Flask's instance directory.

SQLite preview data is local to that computer. It is not automatically transferred to MySQL and should not be used as a substitute for creating the MySQL schema on a new machine.

---

# 7. Troubleshooting

### Python is not recognized

Check the installation:

```powershell
py --version
```

If the command fails, verify the Python installation and PATH configuration.

### The virtual environment will not activate

Try activating it from Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### Flask or another package is missing

Make sure the virtual environment is activated and run:

```powershell
python -m pip install -r requirements.txt
```

### MySQL connection fails

Check that:

1. MySQL Server is running.
2. The database name is correct.
3. The database user and password are correct.
4. The database user has the required privileges.
5. The `DATABASE_URL` uses the correct driver.
6. Special characters in the password are encoded correctly.
7. The required MySQL driver is installed.

### Database tables are missing

Inspect the current database and compare it with `database/schema.sql`. Use the documented initialization or migration command appropriate to the database's current state.

Do not delete or recreate the database as a first troubleshooting step.

### Analyst login fails

Check that the analyst account exists in the database configured by the running application. Public registration does not create analyst accounts.

### Port 5000 is already in use

Stop the other development server using that port or configure a different available port.

---

# 8. Security Notes

- Never commit `.env` or real credentials to GitHub.
- Keep `.env.example` free of actual secrets.
- Use strong secret keys and passwords.
- Do not use Flask debug mode in production.
- Use HTTPS and secure cookies in production.
- Restrict database access to authorized users.
- Keep public-user and analyst permissions separate.
- Treat submitted reports and external threat indicators as untrusted data.
- Do not treat a report as a confirmed threat without sufficient evidence.
- Review imported sample data and external intelligence before relying on it.

---

# 9. Project Structure

```text
CYBERSECURITY THREAT PROJECT/
│
├── app/
│   ├── forms/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── decorators.py
│   ├── errors.py
│   ├── extensions.py
│   └── template_helpers.py
│
├── database/
│   ├── migrations/
│   ├── sample_data.sql
│   └── schema.sql
│
├── migrations/
├── tests/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

The `.venv/`, `.env`, and local database files are machine-specific and should not be included in the public project repository.

---

# 10. Conclusion

The Cybersecurity Threat Intelligence Database provides a platform for collecting suspicious activity reports, investigating indicators, managing threat records, and maintaining an auditable analyst workflow.

The application separates public reporting from authorized analyst operations and supports local development with SQLite as well as MySQL-based use.

**Project status:** Educational project. Verify database setup, configuration, and test results on the target computer before relying on the application.
