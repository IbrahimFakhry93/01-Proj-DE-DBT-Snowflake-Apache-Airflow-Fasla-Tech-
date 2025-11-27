#

#! course video:
# https://www.youtube.com/watch?v=x8DE4DprAzY&t=1165s

#! Course Repo:
# https://github.com/ansamAY/dbt_snowflake_project


#! snowflake:
# user: ibrahim9316
# Bebokepeer93$%
# BT39698


#! snowflake website UI:
# https://app.snowflake.com/fimnzvb/bt39698/#/homepage

#! Airflow UI:
# http://localhost:8080

#! airflow kiwi:
# 2.8.3

# Airflow officially supports Python 3.8–3.11.

# * ==========================================================================================
# & Creating Resources:

# ^ Warehouses:
# * A virtual warehouse (compute power) named COMPUTE_WH
# * or FINANCE_WAREHOUSE is selected/created to run queries.

# ^ Databases & Schemas:
# * Database named: FINANCE_DB
# * Schema named: RAW

# * The RAW schema will hold the unprocessed data. That's why it's called RAW

# ^ note:
# * Always pay attention to credit cost optimization while working on cloud
# * by defining warehouse size, auto suspend


# ^ go to snowflake website and sign in
#! snowflake:
# user: ibrahim9316
# Bebokepeer93$%
# BT39698

# ^ create sql worksheet:

# ^ create finance_wh as new warehouse
# CREATE OR REPLACE WAREHOUSE finance_wh
# WITH WAREHOUSE_SIZE = 'XSMALL'
# AUTO_SUSPEND = 60
# AUTO_RESUME = TRUE
# INITIALLY_SUSPENDED = TRUE;

# ^ create finance_db
# CREATE OR REPLACE DATABASE finance_db;
# CREATE OR REPLACE SCHEMA raw;

# ^ create tables
# CREATE OR REPLACE TABLE raw.customers (
#   id varchar PRIMARY KEY,
#   name varchar,
#   email varchar,
#   country varchar
# );

# CREATE OR REPLACE TABLE raw.orders (
#   id INT PRIMARY KEY,
#   customer_id INT,
#   order_date DATE,
#   total_amount INT,
#   status varchar
# );

# CREATE OR REPLACE TABLE raw.order_items (
#     id INT,
#     order_id INT,
#     product_id INT,
#     quantity INT,
#     unit_price INT
# );

# CREATE OR REPLACE TABLE raw.products (
#     id int PRIMARY KEY,
#     name STRING,
#     category STRING,
#     price int
# );

# ^ load data to each table using snowflake UI
# ^ choose headers (revise the video)

# ^ create stage (temp storage) to load large data set
# CREATE OR REPLACE STAGE finance_stage
# FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1);

# ^ load data from the stage to raw.products table :
# COPY INTO raw.products
# FROM @finance_stage/products.csv
# FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1);

# *=================================================================================

#! dbt part:

# 8 make connection between dbt and snowflake why?
# so can dbt observe the created databases and schemas on snowflake

# how to connect to data base:
# setup the adapter with the thing we want to connect to (snowflake in this case)

# ^ go to vs code bash terminal
# pip install dbt-core dbt-snowflake
#^ uninstall
# pip uninstall dbt-core dbt-snowflake

#^ to create dbt project folder
# dbt init snowflake_data_project
from 00 Course Repo.dbt-env.lib.python3.11.site-packages.airflow.www.api.experimental.endpoints import test
azure_uaenorth

#^ to remove dbt project
# rm -rf snowflake_data_project

#^ choose the number of snow flake database (ex. number: 1)

#^ enter account details so you need:

#~ go to snowflake worksheet
SELECT lower(CURRENT_REGION()), lower(CURRENT_ACCOUNT());
SELECT CURRENT_USER();

# This snippet retrieves session-specific metadata in Snowflake or similar environments:

# CURRENT_REGION() → returns the region of the current session (e.g., AWS US East).

# CURRENT_ACCOUNT() → returns the account identifier.

# CURRENT_USER() → returns the username of the current session.

#^ enter in vs code terminal this:
# account: lower account no.current region.cloud provider when signup on snowflake (azure)
# enter username

azure_uaenorth

#! User Creation and Credentials Granting:

#^ create new user for dbt
CREATE USER dbt_user
  PASSWORD = 'dbt_password'
  LOGIN_NAME = 'dbt_user'
  DEFAULT_ROLE = ACCOUNTADMIN
  MUST_CHANGE_PASSWORD = FALSE;
 
#? note:
#~ By default, new users are automatically granted the PUBLIC role.
#* Setting DEFAULT_ROLE doesn’t automatically grant the role — you must explicitly grant it. 
GRANT ROLE ACCOUNTADMIN TO USER dbt_user;

#^ Show granted roles
SHOW GRANTS TO USER dbt_user;

#? or switch explicitly roles in a session 
USE ROLE ACCOUNTADMIN;

#^ -- Grant access to database
# GRANT USAGE ON DATABASE finance_db TO ROLE ACCOUNTADMIN;

#^ -- Grant access on schema
# GRANT USAGE ON SCHEMA finance_db.raw TO ROLE ACCOUNTADMIN;

#^ -- Grant usage on warehouse
# GRANT USAGE ON WAREHOUSE finance_wh TO ROLE ACCOUNTADMIN;

# ^-- Grant select, insert, update, delete on all tables in schema finance_db.raw to role ACCOUNTADMIN
# GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA finance_db.raw TO ROLE ACCOUNTADMIN;

#^ return to vs code terminal:
#* enter warehouse,database,schema names
#* enter number of threads: 4

#^ test connection:
#* open in terminal: the directory of snowflake_data_project
#* dbt debug

#^ to navigate to profile.yaml:
#* C:\Users\Ibrahim-Fakhry\.dbt
#~ or:
# dbt debug --config-dir
#* To view your profiles.yml file, run:
#* open /Users/alice/.dbt

#? Best practice
#^ It’s not recommended to give dbt_user the powerful ACCOUNTADMIN role in production. Instead:

#* Create a custom role (e.g. DBT_ROLE).

#* Grant only the privileges dbt needs (USAGE on warehouse, database, schema; SELECT/INSERT/UPDATE/DELETE on tables).

#* Assign DBT_ROLE as the default role for dbt_user.

#*===========================================================================================================
#! Writing models in dbt:

#* how to write models, how to clean our data, how to make aggregation, sum and test using dbt
#* our so far sequence:on snowflake, we created warehouse -> created database -> created schema-> under schema we created four tables
#* dbt needs to understand this structure or sequence , how?

#* we create file contains our sources: database name, used schema, used tables
#* any source of data will be placed in sources file

#^ create file: sources.yml inside models folder in snowflake data project

#* sources.yml is useful as it's one source of truth
#* if we changed database or schema, we need to change only this file

#* sources of all data models
#* it's useful also for data lineage (the track of data path)
#* to every step of a data, what was the data source at this step

#^ next step: observe your data on snowflake to decide how the cleaning will be
#^ go to snowflake worksheet:
select * from customers;          #* change id to customer_id
select * from orders;             #* change id to order_id, change status to order_status
select * from order_items;        #* add column: total price  
select * from products;           #* change id to product_id, product_name etc..


#^ stages in dbt:
#* stage is a middle place between raw data (unprocessed data) and data tables for analytics

#* stage is for cleaning the data
#* Cleaning of raw data (renaming columns, adding columns etc..) takes place in staging 

#* analytics tables: contained joined tables or aggregated tables (complex queries in general)

#^ create folder: staging inside models folder in snowflake data project
#^ create staging models: each model contains the required changes to be applied on each table
# stg_customers.sql 
# stg_orders.sql
# stg_orders_items.sql
# stg_products.sql

#^ open: stg_customers.sql
# SELECT id AS customer_id, name AS customer_name,email,country FROM {{source('raw_data','customers')}}
# in dbt, statement is not hard coded (static) as finance_db.raw.customers
# It's useful when changing database or when switching environment among development, testing, production

#^ Check if dbt sees the source
# dbt ls --resource-type source

#^ Preview compiled SQL
# dbt compile --select stg_customers

#^ See the final SQL that dbt sends to Snowflake — no Jinja, just raw SQL.
# target/compiled/snowflake_data_project/models/staging/stg_orders.sql


#^ then in terminal:
#* dbt run

#* staging will be as views according to dbt_project.yml

#^ show views on snowflake
USE DATABASE finance_db;
USE SCHEMA raw;
SHOW VIEWS;

#^ shows the columns and their types.
DESCRIBE VIEW raw.stg_customers;

#^ go to sql worksheet on snowflake
#* select * from stg_orders_items

#^ some commands to run in case of some config problems:
Clear cache
Sometimes dbt caches manifests. Run:
# dbt clean
# dbt deps

#*========================

#? Analytics:

#^ create fact tables (joined tables) for analysis and reporting

#^ create folder: marts (for joins and aggregation) inside models folder in snowflake data project
# fct.daily_order_revenue.sql


#*====================

#^ testing
#^ create file: snowflake_test.yml in tests folder in snowflake data project

# dbt test

# dbt docs generate

# dbt docs serve --port 8088

#^ check lineage graph


#*===================================================================
#* 45:10
#! Airflow Section

#* dbt core doesn't have scheduling so we need airflow to execute jobs and models in a certain schedule
#* but dbt cloud has scheduling

#* first drop pre-created views on snowflake so we make sure they will be created again by airflow
DROP VIEW STG_ORDER_ITEMS;
DROP VIEW STG_CUSTOMERS;
DROP VIEW STG_ORDERS;
DROP VIEW STG_PRODUCTS;

#^ install apache airflow

pip install apache-airflow

#~^ install provider so airflow can deal with snowflake
pip install apache-airflow-providers-snowflake  #* If using Snowflake

#! if encounter this error:
#! ERROR: Could not install packages due to an OSError: [WinError 5] 
# Access is denied: 'C:\\1Programming\\01 Data Engineer\\01 Fesla Tech\\01 DE Projects\\01 Proj DE, DBT,
# Snowflake & Apache Airflow\\01 My Project\\venv\\Lib\\site-packages\\google\\~upb\\_message.pyd' Check the permissions.

#? solution:
#~ Fixing WinError 5 during pip install (Airflow Snowflake provider)

#* This error means Windows blocked access to a file inside your virtual environment during the install — specifically:
#! Access is denied: '...\\venv\\Lib\\site-packages\\google\\~upb\\_message.pyd'
# That’s a compiled binary used by protobuf

#?Note: Windows blocks access to certain .pyd files if they're in use or lack admin rights.
#  This error usually happens inside virtual environments during package upgrades.
#  The file in question was '_message.pyd' from the protobuf package.

#~ Step 1: Close all Python-related processes
#  Use Task Manager (Ctrl + Shift + Esc) → End any 'python.exe' or 'airflow.exe'

#~ Step 2: Run terminal as Administrator
#  Right-click VS Code or Git Bash → "Run as administrator"
#  Then activate your virtual environment:
source venv/Scripts/activate  # Git Bash
.\venv\Scripts\activate       # PowerShell

#~ Step 3: Retry the install
pip install apache-airflow-providers-snowflake

#~ Step 4: If error persists, manually delete the locked file
#  Navigate to:
#    C:\1Programming\...\venv\Lib\site-packages\google\
#  Delete '_message.pyd'
#  Then rerun the install command.

#~ Why this works:
#  Windows locks compiled binaries (.pyd) during runtime.
#  Admin rights + file unlock resolves permission errors.

#~ Optional: Clean reinstall (if issues persist)
#  Delete and recreate your virtual environment:
rm -r venv
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt


#================================================

#^ sets the environment variable AIRFLOW_HOME to point to ~/airflow, 
#^ which tells Airflow where to store its config, logs, and metadata DB.
export AIRFLOW_HOME=~/airflow

#* export → defines a shell environment variable.
#* AIRFLOW_HOME → the variable Airflow uses to locate its working directory.
#* ~/airflow → sets the directory to a folder named airflow inside your home directory.

#~ Why it matters
#* By default, Airflow uses ~/airflow unless you override it. Setting AIRFLOW_HOME explicitly
#* Ensures consistency across sessions and scripts.
#* Lets you isolate multiple Airflow setups (e.g., dev vs prod).
#* Avoids cluttering your home directory if you want to relocate Airflow elsewhere.

#^ Initialize airflow: launch the database initially for airflow
airflow db init

#^ create folder dags inside airflow 

mkdir -p ~/airflow/dags
# mkdir -p → creates the ~/airflow/dags directory (including parent folders if missing).

#^ note:
# The ~ symbol means your home directory — it's a shortcut used in Unix-like shells (like Bash, zsh, WSL, Git Bash).
# On Git Bash (Windows): C:\Users\your-username

nano ~/airflow/dags/dbt_dag.py
# nano → opens the file dbt_dag.py in the nano text editor

#^ copy and paste in the terminal this: 
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 25),  # Change as needed
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'dbt_snowflake_pipeline',
    default_args=default_args,
    description='Run dbt models using dbt Core',
    schedule_interval='@daily',  # Run daily
    catchup=False,
)

# Define the path to your dbt project
DBT_PROJECT_DIR = r"C:\1Programming\01 Data Engineer\01 Fesla Tech\01 DE Projects\01 Proj DE, DBT, Snowflake & Apache Airflow\01 My Project\snowflake_data_project"

# Task 1: Run dbt models
dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command=f'cd "{DBT_PROJECT_DIR}" && dbt run',
    dag=dag,
)

# Task 2: Run dbt tests after models are built
dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command=f'cd "{DBT_PROJECT_DIR}" && dbt test',
    dag=dag,
)

# Define task dependencies
dbt_run >> dbt_test  # dbt_run must finish before dbt_test starts


#^ then click: ctrl + x , then press y then enter

#^ launch the scheduler and webserver
airflow scheduler &
airflow webserver &


#^ go to airflow UI
# http://localhost:8080

#^ Find your DAG: dbt_snowflake_pipeline
#^ select dbt_snowflake_pipeline
# Pause → then trigger it manually (unpause will rerun the dag automatically)

#^ go to snowflake
# observe the created views 

# You should see views created by dbt inside your Snowflake project.
# This confirms Airflow successfully ran dbt run and dbt test.

#^ so by that: we used airflow to run dbt and create the models


# Create a default Unix user account: ibrahim-fakhry
# bebokepeer93

#& Update WSL on Windows 11

#? Step 1: Open PowerShell as Administrator
#* Press Win + S → type "PowerShell"
#* Right‑click → "Run as administrator"

#? Step 2: Update WSL
#* wsl --update        # installs the latest WSL version (WSL 2)

#? Step 3: Restart your computer
#* Required for changes to take effect

#? Step 4: Verify installation
#* wsl --version       # shows current WSL version
#* wsl --list --online # lists available Linux distros you can install

#? Step 5: (Optional) Install Ubuntu for testing
#* wsl --install -d Ubuntu

# Docker Desktop on Windows 11 uses WSL 2 as its backend.



# \\wsl$\Ubuntu\home\Ibrahim-Fakhry\airflow_project



airflow users create \
  --username ibrahim9316 \
  --firstname Ibrahim \
  --lastname Fakhry \
  --role Admin \
  --email ibrahim.fakhry93@yahoo.com \
  --password bebokepeer93
  
  cat ~/airflow/simple_auth_manager_passwords.json.generated

 Login with username: admin  password: u5qysrxpNRSv9fhe