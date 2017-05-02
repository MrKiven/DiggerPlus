CREATE DATABASE IF NOT EXISTS `diggerplus`;

USE `diggerplus`;

CREATE TABLE `todo`(
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(20) DEFAULT "",
    `is_done` INT(1) NOT NULL DEFAULT 0,
    KEY `dp_todo_title` (`title`)
);
