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

# hoe to connect?
# setup the adapter with the thing we want to connect to (snowflake in this case)

# ^ go to vs code bash terminal
# pip install dbt-core dbt-snowflake

# dbt init snowflake_data_project

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
# account identifier.current region.cloud provider when signup on snowflake (azure)
# enter username

#! User Creation and Credentials Granting:

# CREATE USER dbt_user
#   PASSWORD = 'dbt_password'
#   LOGIN_NAME = 'dbt_user'
#   MUST_CHANGE_PASSWORD = FALSE;

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
#* dbt debug

#! Writing models in dbt:

