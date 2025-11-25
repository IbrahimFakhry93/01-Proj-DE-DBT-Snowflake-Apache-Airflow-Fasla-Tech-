-- CREATE OR REPLACE WAREHOUSE finance_wh
-- WITH WAREHOUSE_SIZE = 'XSMALL'
-- AUTO_SUSPEND = 60
-- AUTO_RESUME = TRUE
-- INITIALLY_SUSPENDED = TRUE;

-- CREATE OR REPLACE DATABASE finance_db;
-- CREATE OR REPLACE SCHEMA raw;

-- Drop TABLE customers;

-- CREATE OR REPLACE TABLE raw.customers (
--   id int PRIMARY KEY,
--   name varchar,
--   email varchar,
--   country varchar
-- );

-- CREATE OR REPLACE TABLE raw.orders (
--   id INT PRIMARY KEY,
--   customer_id INT,
--   order_date DATE,
--   total_amount INT,
--   status varchar
-- );

-- CREATE OR REPLACE TABLE raw.order_items (
--     id INT,
--     order_id INT,
--     product_id INT,
--     quantity INT,
--     unit_price INT
-- );

-- CREATE OR REPLACE TABLE raw.products (
--     id int PRIMARY KEY,
--     name STRING,
--     category STRING,
--     price int
-- );

-- CREATE OR REPLACE STAGE finance_stage
-- FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1);

-- COPY INTO raw.products
-- FROM @finance_stage/products.csv
-- FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1);


-- SELECT lower(CURRENT_REGION()), lower(CURRENT_ACCOUNT());
-- SELECT CURRENT_USER();


-- CREATE USER dbt_user
--   PASSWORD = 'dbt_password'
--   LOGIN_NAME = 'dbt_user'
--   DEFAULT_ROLE = ACCOUNTADMIN
--   MUST_CHANGE_PASSWORD = FALSE;

-- GRANT USAGE ON DATABASE finance_db TO ROLE ACCOUNTADMIN;

-- GRANT USAGE ON SCHEMA finance_db.raw TO ROLE ACCOUNTADMIN;

-- GRANT USAGE ON WAREHOUSE finance_wh TO ROLE ACCOUNTADMIN;

-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA finance_db.raw TO ROLE ACCOUNTADMIN;
  
  
--   SHOW USERS LIKE 'dbt_user';
-- SELECT CURRENT_ORGANIZATION_NAME(), CURRENT_ACCOUNT_NAME();


-- SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ORGANIZATION_NAME(), CURRENT_ACCOUNT_NAME();