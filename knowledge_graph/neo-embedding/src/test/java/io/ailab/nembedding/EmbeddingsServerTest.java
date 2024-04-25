package io.ailab.nembedding;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInstance;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.Record;
import org.neo4j.driver.Session;
import org.neo4j.driver.Value;
import org.neo4j.harness.Neo4j;
import org.neo4j.harness.Neo4jBuilders;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public class EmbeddingsServerTest {

    private Neo4j embeddedDatabaseServer;

    @BeforeAll
    void initializeNeo4j() {
        this.embeddedDatabaseServer = Neo4jBuilders.newInProcessBuilder()
                .withDisabledServer()
                .withProcedure(EmbeddingsServer.class)
                .build();
    }

    @AfterAll
    void closeNeo4j() {
        this.embeddedDatabaseServer.close();
    }

    @Test
    void generateEmbeddings() {
        try(Driver driver = GraphDatabase.driver(embeddedDatabaseServer.boltURI());
            Session session = driver.session()) {

            Record result = session.run("CALL io.ailab.embeddings('Hello') YIELD embeddings RETURN embeddings").single();
            Value actual_embeddings = result.get("embeddings");
            List<Double> expected_embeddings = List.of(-0.0627717524766922, 0.054958831518888474, 0.05216477811336517);

            assertThat(actual_embeddings.get(0).asDouble()).isEqualTo(expected_embeddings.get(0));
            assertThat(actual_embeddings.get(1).asDouble()).isEqualTo(expected_embeddings.get(1));
            assertThat(actual_embeddings.get(2).asDouble()).isEqualTo(expected_embeddings.get(2));
        }
    }
}