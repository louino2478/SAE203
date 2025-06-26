-- Nettoyage
DROP USER IF EXISTS 'SAE'@'localhost';
DROP DATABASE IF EXISTS SAE;

-- Creation
CREATE DATABASE SAE;
CREATE USER 'SAE'@'localhost' IDENTIFIED BY 'ChangePasswordHere';

-- Permission
GRANT ALL PRIVILEGES ON SAE.* TO 'SAE'@'localhost';
FLUSH PRIVILEGES;

-- Connection a la DB
USE SAE;

-- Creation des table
-- temperature et humidité
CREATE TABLE environment (
    timestamp TIMESTAMP PRIMARY KEY,
    louistemp FLOAT,
    louishum FLOAT,
    paweltemp FLOAT,
    pawelhum FLOAT,
    owmtemp FLOAT,
    owmhum FLOAT
);

-- info elec
CREATE TABLE power_data (
    timestamp TIMESTAMP PRIMARY KEY,
    louisPAPP FLOAT,
    pawelPAPP FLOAT,
    pawelPTEC FLOAT
);

-- info system
CREATE TABLE system_usage (
    timestamp TIMESTAMP PRIMARY KEY,
    louisCPU FLOAT,
    louisRAM FLOAT,
    pawelCPU FLOAT,
    pawelRAM FLOAT
);

