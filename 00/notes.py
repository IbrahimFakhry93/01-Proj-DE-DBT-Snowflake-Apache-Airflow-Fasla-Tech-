#

#! course video:
# https://www.youtube.com/watch?v=x8DE4DprAzY&t=1165s

#! Course Repo:
# https://github.com/ansamAY/dbt_snowflake_project


#! snowflake:
# user: ibrahim9316
# Bebokepeer93$%
# BT39698


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


#! Writing models in dbt:

