package com.aditionwala.payload;

public class PredictResponse {
    private double score;
    private boolean hot;

    public PredictResponse() {}

    public PredictResponse(double score, boolean hot) {
        this.score = score;
        this.hot = hot;
    }

    public double getScore() { return score; }
    public void setScore(double score) { this.score = score; }
    public boolean isHot() { return hot; }
    public void setHot(boolean hot) { this.hot = hot; }
}
