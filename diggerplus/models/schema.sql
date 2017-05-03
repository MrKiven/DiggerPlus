CREATE DATABASE IF NOT EXISTS `diggerplus`;

USE `diggerplus`;

CREATE TABLE `todo`(
    `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(20) DEFAULT "" COMMENT '任务名',
    `is_done` INT(1) NOT NULL DEFAULT 0 COMMENT '是否完成',
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY `title` (`title`),
    INDEX `dp_todo_created_at` (`created_at`),
    INDEX `dp_todo_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='任务信息';
