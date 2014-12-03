SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET search_path = trade, pg_catalog;


CREATE SCHEMA trade;

CREATE TABLE api_keys (
    character_id integer NOT NULL PRIMARY KEY,
    character_name text,
    key_id integer,
    vcode text
);

CREATE TABLE wallet_transactions (
    transaction_id bigint NOT NULL PRIMARY KEY,
    character_id integer NOT NULL,
    transaction_date timestamp without time zone,
    quantity integer,
    type_id integer,
    price numeric(15,2),
    client_name text,
    station_id integer,
    transaction_type integer
);

CREATE RULE wallet_transactions_ignore_duplicates AS
ON INSERT TO wallet_transactions WHERE EXISTS (SELECT 1 FROM wallet_transactions WHERE (wallet_transactions.transaction_id = new.transaction_id))
DO INSTEAD NOTHING;

CREATE TYPE market_order_type AS ENUM ('buy', 'sell');

CREATE TABLE market_orders (
    order_id bigint NOT NULL PRIMARY KEY,
    character_id integer NOT NULL,
    issued_date timestamp without time zone,
    type_id integer,
    price numeric(15,2),
    order_type market_order_type,
    station_id integer,
    range integer,
    vol_entered integer,
    vol_remaining integer,
    order_state integer
);

CREATE RULE market_orders_update AS
ON INSERT TO market_orders WHERE EXISTS (SELECT 1 FROM market_orders WHERE (market_orders.order_id = new.order_id))
DO INSTEAD
UPDATE market_orders SET price = new.price, vol_remaining = new.vol_remaining, order_state = new.order_state
WHERE order_id = new.order_id;
