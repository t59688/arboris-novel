-- 全量数据库建表脚本，适用于 MySQL 8.x
-- 如需重建，请先根据需要执行 DROP TABLE，再运行本脚本

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(128) UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    external_id VARCHAR(255) UNIQUE,
    is_admin TINYINT(1) DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS novel_projects (
    id CHAR(36) PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    initial_prompt TEXT,
    status VARCHAR(32) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_novel_projects_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS novel_conversations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    project_id CHAR(36) NOT NULL,
    seq INT NOT NULL,
    role VARCHAR(32) NOT NULL,
    content LONGTEXT NOT NULL,
    metadata JSON NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_conversations_project FOREIGN KEY (project_id) REFERENCES novel_projects(id) ON DELETE CASCADE,
    UNIQUE KEY uq_conversations_project_seq (project_id, seq)
);

CREATE TABLE IF NOT EXISTS novel_blueprints (
    project_id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NULL,
    target_audience VARCHAR(255) NULL,
    genre VARCHAR(128) NULL,
    style VARCHAR(128) NULL,
    tone VARCHAR(128) NULL,
    one_sentence_summary TEXT NULL,
    full_synopsis LONGTEXT NULL,
    world_setting JSON NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_blueprints_project FOREIGN KEY (project_id) REFERENCES novel_projects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS blueprint_characters (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    project_id CHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    identity VARCHAR(255) NULL,
    personality TEXT NULL,
    goals TEXT NULL,
    abilities TEXT NULL,
    relationship_to_protagonist TEXT NULL,
    extra JSON NULL,
    position INT DEFAULT 0,
    CONSTRAINT fk_characters_project FOREIGN KEY (project_id) REFERENCES novel_projects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS blueprint_relationships (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    project_id CHAR(36) NOT NULL,
    character_from VARCHAR(255) NOT NULL,
    character_to VARCHAR(255) NOT NULL,
    description TEXT NULL,
    position INT DEFAULT 0,
    CONSTRAINT fk_relationships_project FOREIGN KEY (project_id) REFERENCES novel_projects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS chapter_outlines (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    project_id CHAR(36) NOT NULL,
    chapter_number INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    summary TEXT NULL,
    narrative_phase VARCHAR(64) NULL,
    foreshadowing JSON NULL,
    emotion_hook TEXT NULL,
    CONSTRAINT fk_outlines_project FOREIGN KEY (project_id) REFERENCES novel_projects(id) ON DELETE CASCADE,
    UNIQUE KEY uq_outline_project_chapter (project_id, chapter_number)
);

CREATE TABLE IF NOT EXISTS chapters (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    project_id CHAR(36) NOT NULL,
    chapter_number INT NOT NULL,
    real_summary TEXT NULL,
    status VARCHAR(32) DEFAULT 'not_generated',
    word_count INT DEFAULT 0,
    selected_version_id BIGINT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_chapters_project FOREIGN KEY (project_id) REFERENCES novel_projects(id) ON DELETE CASCADE,
    UNIQUE KEY uq_chapter_project_number (project_id, chapter_number)
);

CREATE TABLE IF NOT EXISTS chapter_versions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    chapter_id BIGINT NOT NULL,
    version_label VARCHAR(64) NULL,
    provider VARCHAR(64) NULL,
    content LONGTEXT NOT NULL,
    metadata JSON NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_versions_chapter FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE
);

ALTER TABLE chapters
    ADD CONSTRAINT fk_chapter_selected_version
    FOREIGN KEY (selected_version_id) REFERENCES chapter_versions(id)
    ON DELETE SET NULL;

CREATE TABLE IF NOT EXISTS chapter_evaluations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    chapter_id BIGINT NOT NULL,
    version_id BIGINT NULL,
    decision VARCHAR(32) NULL,
    feedback TEXT NULL,
    score DECIMAL(5,2) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_evaluations_chapter FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE,
    CONSTRAINT fk_evaluations_version FOREIGN KEY (version_id) REFERENCES chapter_versions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS llm_configs (
    user_id INT PRIMARY KEY,
    llm_provider_url TEXT NULL,
    llm_provider_api_key TEXT NULL,
    llm_provider_model TEXT NULL,
    CONSTRAINT fk_llm_configs_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS prompts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(255) NULL,
    content LONGTEXT NOT NULL,
    tags VARCHAR(255) NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS system_configs (
    `key` VARCHAR(100) PRIMARY KEY,
    value TEXT NOT NULL,
    description VARCHAR(255) NULL
);

CREATE TABLE IF NOT EXISTS admin_settings (
    `key` VARCHAR(64) PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_daily_requests (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    request_date DATE NOT NULL,
    request_count INT DEFAULT 0,
    UNIQUE KEY uq_user_request_date (user_id, request_date),
    CONSTRAINT fk_daily_requests_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS usage_metrics (
    `key` VARCHAR(64) PRIMARY KEY,
    value INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS update_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(64) NULL,
    is_pinned TINYINT(1) DEFAULT 0
);
