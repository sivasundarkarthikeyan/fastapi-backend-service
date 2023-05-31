FROM postgres
ENV POSTGRES_PASSWORD Ie9yaAlhhb
ENV POSTGRES_DB ionos
COPY vehicle_table.sql /docker-entrypoint-initdb.d/vehicle_table.sql
EXPOSE 5432
