
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
    user_id VARCHAR(255) PRIMARY KEY,
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
    user_id VARCHAR(255),
    academic_level_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (academic_level_id) REFERENCES academic_levels(academic_level_id)
);

CREATE TABLE user_channels (
    user_group_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),
    group_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (group_id) REFERENCES channels(group_id)
);

CREATE TABLE messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT ,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id VARCHAR(255),
    group_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (group_id) REFERENCES channels(group_id)
);


CREATE TABLE notices (
    notice_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    post_data DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


INSERT INTO schools (school_id, school_code, school_name, parent_auth_key, teacher_auth_key) VALUES (1, 'demo01', 'Demo School', 'parent', 'teacher');

INSERT INTO academic_levels (academic_level_id, grade, section, school_id) VALUES (1,'1年', 'A組', 1);

INSERT INTO users (user_id, name_kanji_full, name_kana_full, parent_name, email, password, role, phone_number, academic_level_id, school_id)
VALUES  ('970af84c-dd40-47ff-af23-282b72b7cca8','五条　悟', 'ゴジョウ　サトル', '五条　由紀子', 'satoru@example.com', '011f55b984b0ea1e5e1d6a32df1ac1548fe24f8c20d85012b04c6fc5139abb42', 'student', '09012345678', 1, 1),
        ('5a59c7e8-080a-4a82-8f5a-7a3a6e10a30f','夏油　傑', 'ゲトウ　スグル', NULL, 'suguru@example.com', '54aaa3aced18c8f91fa47b375ea186680236a0359f80dcf483ad7b90b72f8d0d', 'teacher', '08087654321', 1, 1),
        ('4e0a0e4b-0637-4d0e-b8d7-42e9b8d8e2b5','家入　硝子', 'イエイリ　ショウコ', NULL, 'syouko@example.com', 'ade7c829d3edab5cdb685fa383149fa867d0880136341ecfe1e1128dc9e2dfdd', 'teacher', '08043218765', 1, 1),
        ('a0f42572-31b6-4f52-8ad3-c6bbd0e7d44b','高田　真希', 'タカダ　マキ', NULL, 'maki@example.com', 'cdda29d8bf916a0f97e4ea583bb1dcf6769c1c66773b9a15435a7f4d9fa1d7db', 'student', '09065432109', 1, 1),
        ('7f2eae4e-7c57-4648-b1f8-1e3a99a5e9b6','伊地知　洋介', 'イジチ　ヨウスケ', NULL, 'yousuke@example.com', 'd5c3ec5f6d4121298e1a6b9095fb8493a4f35dbb3e6fc01f3c885eb9db9fb8d4', 'teacher', '08054321098', 1, 1);

INSERT INTO channels (group_id, user_id, group_name, academic_level_id) 
VALUES  (1, '970af84c-dd40-47ff-af23-282b72b7cca8', '田中 田中', 1), 
        (2, '5a59c7e8-080a-4a82-8f5a-7a3a6e10a30f', 'プロスイマー 佐藤', 1),
        (3, '4e0a0e4b-0637-4d0e-b8d7-42e9b8d8e2b5', '佐藤 道哉', 1), 
        (4, '970af84c-dd40-47ff-af23-282b72b7cca8', '五条 悟', 1), 
        (5, '5a59c7e8-080a-4a82-8f5a-7a3a6e10a30f', '夏油 傑', 1),
        (6, '5a59c7e8-080a-4a82-8f5a-7a3a6e10a30f', '夏油 傑', 1),
        (7, '4e0a0e4b-0637-4d0e-b8d7-42e9b8d8e2b5', '家入 硝子', 1),
        (8, 'a0f42572-31b6-4f52-8ad3-c6bbd0e7d44b', '高田 真希', 1),
        (9, '7f2eae4e-7c57-4648-b1f8-1e3a99a5e9b6', '伊地知 洋介', 1);


INSERT INTO user_channels (user_id, group_id) 
VALUES  ('970af84c-dd40-47ff-af23-282b72b7cca8', 1), 
        ('5a59c7e8-080a-4a82-8f5a-7a3a6e10a30f', 2),
        ('4e0a0e4b-0637-4d0e-b8d7-42e9b8d8e2b5', 3), 
        ('970af84c-dd40-47ff-af23-282b72b7cca8', 4), 
        ('5a59c7e8-080a-4a82-8f5a-7a3a6e10a30f', 5), 
        ('5a59c7e8-080a-4a82-8f5a-7a3a6e10a30f', 6), 
        ('4e0a0e4b-0637-4d0e-b8d7-42e9b8d8e2b5', 7), 
        ('a0f42572-31b6-4f52-8ad3-c6bbd0e7d44b', 8), 
        ('7f2eae4e-7c57-4648-b1f8-1e3a99a5e9b6', 9);

INSERT INTO messages (message, user_id, group_id) 
VALUES  ('本日欠席します〜', '970af84c-dd40-47ff-af23-282b72b7cca8', 1), 
        ('本日欠席します〜', '5a59c7e8-080a-4a82-8f5a-7a3a6e10a30f', 2), 
        ('本日欠席します〜', '4e0a0e4b-0637-4d0e-b8d7-42e9b8d8e2b5', 3), 
        ('本日欠席します〜', '970af84c-dd40-47ff-af23-282b72b7cca8', 4), 
        ('本日欠席します〜', '5a59c7e8-080a-4a82-8f5a-7a3a6e10a30f', 5), 
        ('本日欠席します〜', '5a59c7e8-080a-4a82-8f5a-7a3a6e10a30f', 6),
        ('本日欠席します〜', '4e0a0e4b-0637-4d0e-b8d7-42e9b8d8e2b5', 7),
        ('本日欠席します〜', 'a0f42572-31b6-4f52-8ad3-c6bbd0e7d44b', 8),
        ('本日欠席します〜', '7f2eae4e-7c57-4648-b1f8-1e3a99a5e9b6', 9);

INSERT INTO notices (notice_id, category, title, description, post_data, user_id)
VALUES  (1,'1年生','夏休みのお知らせ', '7月20日から8月31日まで夏休みです。', '2024-07-15', '5a59c7e8-080a-4a82-8f5a-7a3a6e10a30f'),
        (2,'1年生','運動会のお知らせ', '10月10日に運動会が開催されます。参加希望者は申し込みをお願いします。', '2024-09-01', '4e0a0e4b-0637-4d0e-b8d7-42e9b8d8e2b5'),
        (3,'1年生','保護者会のお知らせ', '11月20日に保護者会を行います。出席をお願いします。', '2024-10-15', '5a59c7e8-080a-4a82-8f5a-7a3a6e10a30f'),
        (4,'1年生','期末テストのお知らせ', '12月1日から12月3日まで期末テストを実施します。', '2024-11-20', '4e0a0e4b-0637-4d0e-b8d7-42e9b8d8e2b5'),
        (5,'1年生','新年の挨拶', '明けましておめでとうございます。今年もよろしくお願いします。', '2024-01-01', '5a59c7e8-080a-4a82-8f5a-7a3a6e10a30f');
