CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    resume_text TEXT NOT NULL,
    education_data JSONB,
    experience_data JSONB,
    verification_status VARCHAR(50),
    risk_score FLOAT,
    flags JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE verified_institutions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50),
    country VARCHAR(100),
    verification_source VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE verification_history (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id),
    verification_result JSONB,
    verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
