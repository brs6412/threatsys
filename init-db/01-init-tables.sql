-- Enable pgcrypto to use gen_random_uuid() --
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Create organizations table --
CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    tier VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create roles table --
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Create users table --
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    organization_id UUID REFERENCES organizations(id),
    role_id INTEGER NOT NULL DEFAULT 3 REFERENCES roles(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

-- Create IOCs Type table --
CREATE TABLE IF NOT EXISTS ioc_types (
    type_id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL
);

-- Create IOCs table --
CREATE TABLE IF NOT EXISTS iocs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type_id INTEGER REFERENCES ioc_types(type_id),
    value VARCHAR(255) NOT NULL,
    value_hash VARCHAR(64) NOT NULL,
    tlp_level VARCHAR(20) DEFAULT 'WHITE',
    received_at TIMESTAMP DEFAULT NOW(),
    last_seen TIMESTAMP DEFAULT NOW(),
    active BOOLEAN NOT NULL,
    metadata JSONB DEFAULT '{}',
    source_org_id UUID REFERENCES organizations(id),
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create IOC relationships --
CREATE TABLE IF NOT EXISTS ioc_relationships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES iocs(id),
    target_id UUID REFERENCES iocs(id),
    relationship_type VARCHAR(50) NOT NULL,
    confidence_score INTEGER DEFAULT 50,
    first_observed TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_observed TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);
