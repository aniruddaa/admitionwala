package com.aditionwala.payload;

import java.util.List;

public class RecommendResponse {
    private double score;
    private List<String> recommendations;

    public RecommendResponse() {}

    public RecommendResponse(double score, List<String> recommendations) {
        this.score = score;
        this.recommendations = recommendations;
    }

    public double getScore() { return score; }
    public void setScore(double score) { this.score = score; }
    public List<String> getRecommendations() { return recommendations; }
    public void setRecommendations(List<String> recommendations) { this.recommendations = recommendations; }
}
