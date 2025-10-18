package com.aditionwala.nakeml;

import com.aditionwala.payload.LeadRequest;
import com.aditionwala.payload.RecommendResponse;

import java.util.ArrayList;
import java.util.List;

/**
 * A tiny deterministic "ML-like" service implemented without external packages.
 * It computes a lead score and returns simple recommendations.
 */
public class NakeMlService {

    public double scoreLead(com.aditionwala.payload.LeadRequest lead) {
        // Very simple heuristic scoring: normalize fields to [0,1] and combine
        double interest = normalize(lead.getInterestLevel()); // 0-10
        double budget = normalize(lead.getBudgetK()); // in thousands
        double engagement = lead.isSubscribed() ? 0.9 : 0.3;

        double score = 0.5 * interest + 0.3 * budget + 0.2 * engagement;
        // clamp
        return Math.max(0.0, Math.min(1.0, score));
    }

    private double normalize(double x) {
        // assume input roughly in 0..10, clamp and divide
        double v = Math.max(0.0, Math.min(10.0, x));
        return v / 10.0;
    }

    public RecommendResponse recommendServices(LeadRequest lead) {
        List<String> services = new ArrayList<>();
        double score = scoreLead(lead);

        if (score > 0.7) {
            services.add("Premium Growth Package: Campaigns + Dedicated Manager");
            services.add("Conversion Rate Optimization");
        } else if (score > 0.4) {
            services.add("Starter Marketing Pack: Social + Ads");
            services.add("Lead Nurturing Email Sequence");
        } else {
            services.add("Business Development Consultation");
            services.add("Branding Workshop");
        }

        return new RecommendResponse(score, services);
    }
}
