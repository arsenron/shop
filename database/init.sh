#!/bin/bash

set -e

sudo -u postgres psql -c "CREATE USER shop WITH PASSWORD 'shop'"
sudo -u postgres psql -c "CREATE DATABASE shop WITH OWNER shop"

flyway -user=shop -password=shop -sqlMigrationPrefix=v \
  -url=jdbc:postgresql://localhost:5432/shop \
  -locations=filesystem:migrations \
  migrate
