# Scraper-Cedulas-Profesionales

This project is a scraper dedicated to obtaining information about professional licenses of professionals in Mexico who are registered with the SEP (Secretary of Public Education). Since it is a school project, a local interface is included to run it locally.

## Prerequisites

Before you begin, make sure you have Python installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/).

## Step 1: Create a Virtual Environment

```shell
python -m venv .venv
```

This command will create a virtual environment named **.venv** in your project directory.


## Step 2: Activate the Virtual Environment

```shell
source .venv/bin/activate
```

This command activates the virtual environment, isolating your project's dependencies from the system-wide Python installation.

## Step 3: Update pip

```shell
python -m pip install --upgrade pip
```

Updating pip ensures you have the latest version of the Python package manager.

## Step 4: Install pip-tools

```shell
pip install pip-tools
```

** Pip-tools ** will be used to manage your project's dependencies efficiently.


## Step 5: Create a requirements.txt File

```shell
pip-compile requirements.in
```

This command generates a **requirements.txt** file containing your project's dependencies and their specific versions.


## Step 6: Create a dev-requirements.txt File (Optional)

```shell
pip-compile dev-requirements.in
```

If you have development-specific dependencies, use this command to generate a ** dev-requirements.txt ** file.

## Step 7: Install Dependencies

```shell
pip install -r requirements.txt
pip install -r dev-requirements.txt  # Only if you created a dev-requirements.txt file
```

These commands install the project's dependencies in the virtual environment.

## Step 8: Install Pre-commit Hooks (Optional)

```shell
pre-commit install
```

If you use ** pre-commit ** hooks for code formatting and linting, install them in your project.


## Step 9: Run the service

```shell
python cedulas_interface.py    
```

## Step 9: Run test

```shell
python -m unittest discover -v tests
```


