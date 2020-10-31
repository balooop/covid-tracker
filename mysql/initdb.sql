DROP DATABASE IF EXISTS `COVID_Dashboard`;

CREATE DATABASE `COVID_Dashboard`;
USE `COVID_Dashboard`;

CREATE TABLE `Cases`
(
    `Address_visited` NVARCHAR(255) NOT NULL,
    `Case_id` INT NOT NULL,
    `time_stamp` DATETIME,
    PRIMARY KEY(`Case_id`, `Address_visited`)
);

CREATE TABLE `Addresses`
(
    `Address_location` NVARCHAR(255) NOT NULL,
    `Block_id` INT,
    `Num_cases` INT,
    PRIMARY KEY(`Address_location`)
);

CREATE TABLE `Blocks`
(
    `Block_id` INT NOT NULL,
    `Num_cases_blk` INT,
    PRIMARY KEY(`Block_id`)
);