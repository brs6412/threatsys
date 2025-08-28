-- Insert organizations --
INSERT INTO organizations (id, name, tier)
VALUES
  ('11111111-1111-1111-1111-111111111111', 'Acme Corp', 'Gold'),
  ('22222222-2222-2222-2222-222222222222', 'Beta Ltd', 'Silver'),
  ('33333333-3333-3333-3333-333333333333', 'Gamma Inc', 'Bronze');

-- Insert roles --
INSERT INTO roles (name)
VALUES
  ('Admin'),
  ('Analyst'),
  ('User');

-- Insert users --
INSERT INTO users (id, first_name, last_name, email, organization_id, role_id)
VALUES
  ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Alice', 'Abcd', 'alice@acme.com', '11111111-1111-1111-1111-111111111111', 1),
  ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'Bob', 'Bcde', 'bob@beta.com', '22222222-2222-2222-2222-222222222222', 2),
  ('cccccccc-cccc-cccc-cccc-cccccccccccc', 'Carol', 'Cdef', 'carol@gamma.com', '33333333-3333-3333-3333-333333333333', 3);

-- Insert IOC types --
INSERT INTO ioc_types (name, category)
VALUES
  ('ipv4_addr', 'Network'),
  ('ipv6_addr', 'Network'), 
  ('domain', 'Network'),
  ('email', 'Network'),
  ('file_hash_md5', 'File'),
  ('file_hash_sha1', 'File'),
  ('file_hash_sha256', 'File'),
  ('file_hash_sha512', 'File'),
  ('url', 'Network'),
  ('mutex', 'System'), 
  ('registry_key', 'System'),
  ('yara_rule', 'Detection');

-- Insert IOCs --
INSERT INTO iocs (id, type_id, value, value_hash, active, source_org_id, created_by)
VALUES
  ('dddddddd-dddd-dddd-dddd-dddddddddddd', 1, '192.168.1.100', 'abc123def4567890abc123def4567890abc123def4567890abc123def4567890', true, '11111111-1111-1111-1111-111111111111', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'),
  ('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 2, 'malicious.com', 'def456abc1237890def456abc1237890def456abc1237890def456abc1237890', true, '22222222-2222-2222-2222-222222222222', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'),
  ('ffffffff-ffff-ffff-ffff-ffffffffffff', 3, 'e99a18c428cb38d5f260853678922e03', '7890abcdef1234567890abcdef1234567890abcdef1234567890abcdef123456', false, '33333333-3333-3333-3333-333333333333', 'cccccccc-cccc-cccc-cccc-cccccccccccc');

-- Insert IOC relationships --
INSERT INTO ioc_relationships (id, source_id, target_id, relationship_type, confidence_score)
VALUES
  ('12121212-1212-1212-1212-121212121212', 'dddddddd-dddd-dddd-dddd-dddddddddddd', 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 'associated_with', 80),
  ('34343434-3434-3434-3434-343434343434', 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 'ffffffff-ffff-ffff-ffff-ffffffffffff', 'derived_from', 70);
