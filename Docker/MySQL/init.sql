
DROP DATABASE IF EXISTS chimyapp;
DROP USER IF EXISTS 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chimyapp;
USE chimyapp;
GRANT ALL PRIVILEGES ON chimyapp.* TO 'testuser';

CREATE TABLE schools (
    school_id INT AUTO_INCREMENT PRIMARY KEY,
    school_code VARCHAR(50) NOT NULL,
    school_name VARCHAR(100) NOT NULL,
    parent_auth_key VARCHAR(100) NOT NULL,
    teacher_auth_key VARCHAR(100) NOT NULL
);

CREATE TABLE academic_levels (
    academic_level_id INT AUTO_INCREMENT PRIMARY KEY,
    grade VARCHAR(10) NOT NULL,
    section VARCHAR(10) NOT NULL,
    school_id INT,
    FOREIGN KEY (school_id) REFERENCES schools(school_id)
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name_kanji_full VARCHAR(100) NOT NULL,
    name_kana_full VARCHAR(100) NOT NULL,
    parent_name VARCHAR(100),
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'teacher') NOT NULL,
    phone_number VARCHAR(15),
    academic_level_id INT,
    school_id INT,
    FOREIGN KEY (academic_level_id) REFERENCES academic_levels(academic_level_id),
    FOREIGN KEY (school_id) REFERENCES schools(school_id)
);

CREATE TABLE groups (
    group_id INT AUTO_INCREMENT PRIMARY KEY,
    group_name VARCHAR(100),
    academic_level_id INT,
    FOREIGN KEY (academic_level_id) REFERENCES academic_levels(academic_level_id)
);

CREATE TABLE user_groups (
    user_group_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    group_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (group_id) REFERENCES groups(group_id)
);

CREATE TABLE messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INT,
    group_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (group_id) REFERENCES groups(group_id)
);

CREATE TABLE notices (
    notice_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    post_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    teacher_id INT,
    FOREIGN KEY (teacher_id) REFERENCES users(user_id)
);


INSERT INTO schools (school_code, school_name, parent_auth_key, teacher_auth_key)VALUES ('demo0101','サンプル小学校', 'parent_key_example', 'teacher_key_example');

INSERT INTO academic_levels (grade, section, school_id) VALUES ('1年', 'A組', 1);

INSERT INTO users (user_kanji_full, user_kana_full, parent_name, email, password, role, phone_number, academic_level_id, school_id)
VALUES  ('五条　悟', 'ゴジョウ　サトル', '五条　由紀子', 'satoru@example.com', '011f55b984b0ea1e5e1d6a32df1ac1548fe24f8c20d85012b04c6fc5139abb42', 'student', '090-1234-5678', 1, 1),
        ('夏油　傑', 'ゲトウ　スグル', NULL, 'suguru@example.com', '54aaa3aced18c8f91fa47b375ea186680236a0359f80dcf483ad7b90b72f8d0d', 'teacher', '080-8765-4321', 1, 1),
        ('家入　硝子', 'イエイリ　ショウコ', NULL, 'syouko@example.com', 'ade7c829d3edab5cdb685fa383149fa867d0880136341ecfe1e1128dc9e2dfdd', 'teacher', '080-4321-8765', 1, 1);

INSERT INTO groups (group_name, academic_level_id) VALUES ('グループA', 1);

INSERT INTO user_groups (user_id, group_id) VALUES (1, 1), (2, 1), (3, 1);

INSERT INTO messages (message, user_id, group_id) VALUES ('初めまして。', 1, 1);
