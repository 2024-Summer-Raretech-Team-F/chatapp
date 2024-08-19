
DROP DATABASE  chatapp;
DROP USER  'testuser';

CREATE USER 'testuser'@'%' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser'@'%';

USE chatapp;

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

CREATE TABLE channels (
    group_id INT AUTO_INCREMENT PRIMARY KEY,
    group_name VARCHAR(100),
    user_id INT,
    academic_level_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (academic_level_id) REFERENCES academic_levels(academic_level_id)
);

CREATE TABLE user_channels (
    user_group_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    group_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (group_id) REFERENCES channels(group_id)
);

CREATE TABLE messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INT,
    group_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (group_id) REFERENCES channels(group_id)
);


CREATE TABLE notices (
    notice_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    post_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


INSERT INTO schools (school_id, school_code, school_name, parent_auth_key, teacher_auth_key) VALUES (1, 'demo01', 'Demo School', 'parent', 'teacher');

INSERT INTO academic_levels (academic_level_id, grade, section, school_id) VALUES (1,'1年', 'A組', 1);

INSERT INTO users (user_id, name_kanji_full, name_kana_full, parent_name, email, password, role, phone_number, academic_level_id, school_id)
VALUES  (1, '五条　悟', 'ゴジョウ　サトル', '五条　由紀子', 'satoru@example.com', '011f55b984b0ea1e5e1d6a32df1ac1548fe24f8c20d85012b04c6fc5139abb42', 'student', '09012345678', 1, 1),
        (2, '夏油　傑', 'ゲトウ　スグル', NULL, 'suguru@example.com', '54aaa3aced18c8f91fa47b375ea186680236a0359f80dcf483ad7b90b72f8d0d', 'teacher', '08087654321', 1, 1),
        (3, '家入　硝子', 'イエイリ　ショウコ', NULL, 'syouko@example.com', 'ade7c829d3edab5cdb685fa383149fa867d0880136341ecfe1e1128dc9e2dfdd', 'teacher', '08043218765', 1, 1);

INSERT INTO channels (group_id, user_id, group_name, academic_level_id) VALUES (1, 1, '佐藤 道哉', 1), (2, '田中 智樹', 1), (3, '佐藤 道哉', 1);

INSERT INTO user_channels (user_id, group_id) VALUES (1, 1), (2, 1), (3, 1);

INSERT INTO messages (message, user_id, group_id) VALUES ('初めまして。', 1, 1);

INSERT INTO notices (category, title, description, post_date, user_id)
VALUES  ('1年生','夏休みのお知らせ', '7月20日から8月31日まで夏休みです。', '7月15日', 2),
        ('1年生','運動会のお知らせ', '10月10日に運動会が開催されます。参加希望者は申し込みをお願いします。', '9月1日', 3),
        ('1年生','保護者会のお知らせ', '11月20日に保護者会を行います。出席をお願いします。', '10月15日', 2),
        ('1年生','期末テストのお知らせ', '12月1日から12月3日まで期末テストを実施します。', '11月20日', 3),
        ('1年生','新年の挨拶', '明けましておめでとうございます。今年もよろしくお願いします。', '1月1日', 2);

