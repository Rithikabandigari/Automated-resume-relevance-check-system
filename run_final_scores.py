from scoring import combine_scores

# Example scores
hard_score = 78
soft_score = 86.0
llm_score = 50.0  # optional

result = combine_scores(hard_score, soft_score, llm_score)
print("==== FINAL SCORE ====")
print(result)