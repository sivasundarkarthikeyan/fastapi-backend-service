FROM postgres
ENV POSTGRES_PASSWORD ${POSTGRES_PASS}
ENV POSTGRES_DB ${POSTGRES_DATA}
COPY vehicle_table.sql /docker-entrypoint-initdb.d/vehicle_table.sql
EXPOSE 5432
