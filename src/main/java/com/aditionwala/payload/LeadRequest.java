package com.aditionwala.payload;

public class LeadRequest {
    private String name;
    private String email;
    private double interestLevel; // 0-10
    private double budgetK; // budget in thousands
    private boolean subscribed;

    public LeadRequest() {}

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public double getInterestLevel() { return interestLevel; }
    public void setInterestLevel(double interestLevel) { this.interestLevel = interestLevel; }
    public double getBudgetK() { return budgetK; }
    public void setBudgetK(double budgetK) { this.budgetK = budgetK; }
    public boolean isSubscribed() { return subscribed; }
    public void setSubscribed(boolean subscribed) { this.subscribed = subscribed; }
}
