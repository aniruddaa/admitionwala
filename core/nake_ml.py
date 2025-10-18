class NakeMl:
    def __init__(self):
        pass

    def _norm(self, x):
        v = max(0.0, min(10.0, float(x)))
        return v / 10.0

    def score_lead(self, interest, budgetK, subscribed):
        interest_s = self._norm(interest)
        budget_s = self._norm(budgetK)
        engagement = 0.9 if subscribed else 0.3
        score = 0.5 * interest_s + 0.3 * budget_s + 0.2 * engagement
        return max(0.0, min(1.0, score))

    def recommend_services(self, interest, budgetK, subscribed):
        score = self.score_lead(interest, budgetK, subscribed)
        services = []
        if score > 0.7:
            services = ["Premium Growth Package", "Conversion Rate Optimization"]
        elif score > 0.4:
            services = ["Starter Marketing Pack", "Lead Nurturing Emails"]
        else:
            services = ["Branding Workshop", "Business Consultation"]
        return (score, services)
