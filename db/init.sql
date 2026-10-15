CREATE DATABASE ml_predictions;
CREATE USER ml_app WITH ENCRYPTED PASSWORD 'StrongPassword';
GRANT ALL PRIVILEGES ON DATABASE ml_predictions TO ml_app;
\c ml_predictions
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    input_data JSONB NOT NULL,
    prediction JSONB NOT NULL,
    model_version VARCHAR(50) NOT NULL
);
GRANT SELECT, INSERT ON predictions TO ml_app;
GRANT USAGE, SELECT ON SEQUENCE predictions_id_seq TO ml_app;
