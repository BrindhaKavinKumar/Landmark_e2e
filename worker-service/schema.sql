CREATE TABLE IF NOT EXISTS file_processing (
    file_id UUID PRIMARY KEY,
    store_id VARCHAR(50) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    source_path TEXT NOT NULL,
    status VARCHAR(50) NOT NULL,
    uploaded_at TIMESTAMP,
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP,
    total_records INT DEFAULT 0,
    success_records INT DEFAULT 0,
    failed_records INT DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_store_file UNIQUE (store_id, file_name)
);

CREATE TABLE IF NOT EXISTS record_processing (
    record_id UUID PRIMARY KEY,
    file_id UUID REFERENCES file_processing(file_id) ON DELETE CASCADE,
    row_number INT NOT NULL,
    sku VARCHAR(100),
    status VARCHAR(50) NOT NULL,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product_updates (
    id UUID PRIMARY KEY,
    file_id UUID REFERENCES file_processing(file_id) ON DELETE CASCADE,
    store_id VARCHAR(50) NOT NULL,
    sku VARCHAR(100) NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    offer_price NUMERIC(10,2),
    stock INT NOT NULL,
    campaign_id VARCHAR(100),
    last_updated TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS error_logs (
    error_id UUID PRIMARY KEY,
    file_id UUID REFERENCES file_processing(file_id) ON DELETE CASCADE,
    row_number INT,
    error_type VARCHAR(100),
    error_message TEXT,
    raw_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE file_processing
ADD CONSTRAINT unique_store_file UNIQUE (store_id, file_name);