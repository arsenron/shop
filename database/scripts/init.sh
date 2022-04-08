sudo -u postgres psql -c "CREATE USER shop WITH SUPERUSER LOGIN PASSWORD 'shop'"
sudo -u postgres psql -c "CREATE DATABASE shop WITH OWNER shop"
