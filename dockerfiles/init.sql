CREATE DATABASE IF NOT EXISTS fable;
USE fable;

CREATE TABLE IF NOT EXISTS fablelog (
  id INT NOT NULL AUTO_INCREMENT,
  event_name VARCHAR(255) NOT NULL,
  user_id INT NOT NULL,
  unix_ts INT NOT NULL,
  PRIMARY KEY (id)
);
