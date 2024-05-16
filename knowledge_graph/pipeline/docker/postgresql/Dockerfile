FROM pgvector/pgvector:pg16
WORKDIR /docker-entrypoint-initdb.d
COPY docker/postgresql/postgres-script.sql .
COPY docker/postgresql/zinit-ailab.sql .
RUN chmod -R 775 .
