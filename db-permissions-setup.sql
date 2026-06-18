create user admin with password '[password here]';

GRANT ALL ON ALL TABLES IN SCHEMA public to admin;
GRANT ALL ON ALL sequences IN SCHEMA public to admin;
GRANT ALL ON ALL functions IN SCHEMA public to admin;

GRANT create on SCHEMA public to admin;

# to support tests
ALTER ROLE admin CREATEDB;
