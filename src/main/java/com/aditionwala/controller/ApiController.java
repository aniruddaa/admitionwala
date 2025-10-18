package com.aditionwala.controller;

import com.aditionwala.nakeml.NakeMlService;
import com.aditionwala.payload.LeadRequest;
import com.aditionwala.payload.PredictResponse;
import com.aditionwala.payload.RecommendResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class ApiController {

    private final NakeMlService nakeMlService = new NakeMlService();

    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("ok");
    }

    @PostMapping("/predict")
    public ResponseEntity<PredictResponse> predict(@RequestBody LeadRequest req) {
        double score = nakeMlService.scoreLead(req);
        PredictResponse res = new PredictResponse(score, score >= 0.5);
        return ResponseEntity.ok(res);
    }

    @PostMapping("/recommend")
    public ResponseEntity<RecommendResponse> recommend(@RequestBody LeadRequest req) {
        RecommendResponse r = nakeMlService.recommendServices(req);
        return ResponseEntity.ok(r);
    }
}
