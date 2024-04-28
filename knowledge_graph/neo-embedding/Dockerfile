FROM neo4j:5.19.0
ARG VERSION=0.0.6

ENV NEO4J_HOME=/var/lib/neo4j
COPY nembedding-${VERSION}.jar $NEO4J_HOME/plugins/

CMD ["neo4j"]
