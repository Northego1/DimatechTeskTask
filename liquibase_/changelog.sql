-- liquibase formatted sql

-- changeset alex:01
CREATE TABLE admins (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(64) NOT NULL,
    password BYTEA NOT NULL,
    email VARCHAR(128) UNIQUE NOT NULL
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(64) NOT NULL,
    email VARCHAR(128) UNIQUE NOT NULL,
    password BYTEA NOT NULL,
    admin_id UUID NOT NULL REFERENCES admins(id) ON DELETE CASCADE
);

CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    balance DECIMAL NOT NULL DEFAULT 0
);

CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    amount DECIMAL NOT NULL
);

CREATE INDEX idx_admins_email ON admins(email);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_accounts_user_id ON accounts(user_id);
CREATE INDEX idx_payments_account_id ON payments(account_id);

--changeset alex:02
INSERT INTO admins (id, name, password, email)
VALUES (
	'6a69714d-541a-42f7-8a8e-8cff48dc0f6d',
	'admin',
	'$2b$12$6xQoG8IscEYw9MLsoqVx6OYzuwT.JBj2mOurJ.29R6NNXLa1RHgHm',
	'admin@admin.com'
);

INSERT INTO users (id, name, password, email, admin_id)
VALUES(
    '6a69714d-541a-42f7-8a8e-8cff48dc0f6b',
    'user',
    '$2b$12$6xQoG8IscEYw9MLsoqVx6OYzuwT.JBj2mOurJ.29R6NNXLa1RHgHm',
    'user@user.com',
    '6a69714d-541a-42f7-8a8e-8cff48dc0f6d'
);