package io.ailab.nembedding;

import org.json.JSONObject;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;
import java.util.stream.Stream;

import org.neo4j.procedure.Context;
import org.neo4j.procedure.Description;
import org.neo4j.logging.InternalLog;
import org.neo4j.procedure.Name;
import org.neo4j.procedure.Procedure;

import com.fasterxml.jackson.databind.ObjectMapper;

public class EmbeddingsServer {

    // Change me when testing from laptop
    // This is the URL from the neo4j pod to the transformer pod
    // private static final String API_SERVER_URL = "http://transformer.knowledge-graph.svc.cluster.local:3000/embed";
    private static final String API_SERVER_URL = "http://localhost:3000/embed";
    private static final String TEXT_KEY = "text";
    private static final ObjectMapper objectMapper = new ObjectMapper();
    private static final HttpClient httpClient = HttpClient.newHttpClient();

    public static class CustomEmbeddingResult {

        public final List<Double> embedding;

        public CustomEmbeddingResult() {
            this.embedding = null;
        }

        public CustomEmbeddingResult(List<Double> embedding) {
            this.embedding = embedding;
        }
    }

    @Context
    public InternalLog log;

    @Procedure(name = "io.ailab.embeddings")
    @Description("io.ailab.embeddings('string') - return vector embeddings for the input text.")
    public Stream<CustomEmbeddingResult> embeddings(
            @Name("text") String text) throws URISyntaxException, IOException, InterruptedException {

        if (text == null) {
            return null;
        }

        try {
            URI postURI = new URI(API_SERVER_URL);
            JSONObject requestPayload = new JSONObject();
            requestPayload.put(TEXT_KEY, text);
            HttpRequest httpRequestPost = HttpRequest.newBuilder()
                .uri(postURI)
                .POST(HttpRequest.BodyPublishers.ofString(requestPayload.toString()))
                .header("Content-Type", "application/json")
                .build();

            HttpResponse<String> postResponse = httpClient.send(httpRequestPost, HttpResponse.BodyHandlers.ofString());
            CustomEmbeddingResult result = objectMapper.readValue(postResponse.body(), CustomEmbeddingResult.class);
            return Stream.of(new CustomEmbeddingResult(result.embedding));
        } catch (Exception e) {
            log.error(String.format("Error in embeddings procedure against %s: %s", API_SERVER_URL, e));
            throw e;
        }

    }
}