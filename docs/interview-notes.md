# Interview notes

1. Your result was significant but below the MDE: what do you do?
   - You do not ship on a statistically significant result if it does not clear the pre-set decision threshold. The repo makes that explicit in the preregistration and the decision memo.

2. What is SRM and what would you check?
   - SRM is sample-ratio mismatch. Check the observed arm sizes against the expected 50/50 split; if p<0.05, investigate logging, assignment, or data pipeline issues before trusting a result.

3. Why not peek?
   - Peeking without clear rules raises false positives. The repo documents that timestamps are absent, so the precise effect of peeking cannot be audited; nonetheless, the correct practice is to set the rule before analysis.

4. How does this change with low B2B traffic?
   - The same design logic applies, but the sample size problem becomes more acute. Small B2B products often cannot detect small lifts; that is why the playbook emphasizes larger effects, practical significance, and other research methods.

5. Why are you treating subgroup results as exploratory?
   - Post-randomization segmentation can be biased because the subgroup is defined after assignment. The repo uses a clear label and warns against causal interpretation.

6. What is the difference between CTR and click-through probability?
   - CTR is a rate computed across impressions; click-through probability is the probability that a single user clicks after an exposure. The same statistical logic applies, but the unit of analysis differs.

7. Why do you need a power calculation?
   - Without it, a test may never be able to detect the business impact you care about. The MDE and sample size tables make that evident.

8. Why are the trade-offs between retention and revenue important?
   - A retention gain or loss is not automatically a business win if the same product change cuts revenue or monetization. The repo does not have purchase data, so it explicitly notes the missing revenue evidence.
