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

import org.neo4j.procedure.Description;
import org.neo4j.procedure.Name;
import org.neo4j.procedure.Procedure;

import com.fasterxml.jackson.databind.ObjectMapper;

public class EmbeddingsServer {

    private static final String API_SERVER_URL = "http://localhost:3000/embed";
    private static final String TEXT_KEY = "text";

    public static class CustomEmbeddingsResult {

        public final List<Double> embeddings;

        public CustomEmbeddingsResult() {
            this.embeddings = null;
        }

        public CustomEmbeddingsResult(List<Double> embeddings) {
            this.embeddings = embeddings;
        }
    }

    private static final ObjectMapper objectMapper = new ObjectMapper();

    @Procedure(name = "io.ailab.embeddings")
    @Description("io.ailab.embeddings('string') - return vector embeddings for the input text.")
    public Stream<CustomEmbeddingsResult> embeddings(
            @Name("text") String text) throws URISyntaxException, IOException, InterruptedException {
        if (text == null) {
            return null;
        }

        URI postURI = new URI(API_SERVER_URL);
        JSONObject requestPayload = new JSONObject();
        requestPayload.put(TEXT_KEY, text);
        HttpRequest httpRequestPost = HttpRequest.newBuilder()
                .uri(postURI)
                .POST(HttpRequest.BodyPublishers.ofString(requestPayload.toString()))
                .header("Content-Type", "application/json")
                .build();
        HttpClient httpClient = HttpClient.newHttpClient();

        HttpResponse<String> postResponse = httpClient.send(httpRequestPost, HttpResponse.BodyHandlers.ofString());
        CustomEmbeddingsResult result = objectMapper.readValue(postResponse.body(), CustomEmbeddingsResult.class);
        return Stream.of(new CustomEmbeddingsResult(result.embeddings));
    }
}