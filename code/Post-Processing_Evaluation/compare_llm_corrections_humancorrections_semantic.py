# LLM-generated Corrections: AccessGuruLLM/results/accessguru_dataset/semantic/GPT4/Re-Prompting_metacognitivePrompting_results_accessguru_semantic_dataset_gpt_4.xlsx
# Human Developer Corrections: human_developer_correction_study/humanCorrection_developer1.csv
from sentence_transformers import SentenceTransformer, util

# Load Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Example LLM-generated Alt text
llm_generated_alt = "A golden retriever playing with a ball in a grassy park." # AccessGuru with Corrective Re-prompting GPT-4

# Three human-generated variants
human_alt_texts = [
    "A dog fetching a ball in a green field.", # Developer 1 Alt-text
    "A golden retriever running in the park with a toy.", # Developer 2 Alt-text
    "A happy dog playing outdoors with a ball." # Developer 3 Alt-text
]

# Compute cosine similarity between LLM-generated text and each human-generated text
similarity_scores = [
    util.pytorch_cos_sim(model.encode(llm_generated_alt), model.encode(human_alt))[0][0].item()
    for human_alt in human_alt_texts
]

# Compute average similarity
average_similarity = sum(similarity_scores) / len(similarity_scores)

# Output results
for i, score in enumerate(similarity_scores):
    print(f"Similarity between LLM-generated and Human-{i+1}: {score:.4f}")

print(f"Average Similarity: {average_similarity:.4f}")

# Example LLM-generated lang attributes
llm_langs = {"en"} # Language Attributes in LLM correction

# Three human-generated lang attribute sets
human_langs_list = [
    {"en", "fr"}, # Language Attributes in Developer 1 Correction
    {"en"}, # Language Attributes in Developer 2 Correction
    {"en", "de"} # Language Attributes in Developer 3 Correction
]

# Compute Jaccard similarity: |Intersection| / |Union|
def jaccard_similarity(set1, set2):
    if not set1 and not set2:
        return 1.0  # Both empty = perfect match
    return len(set1 & set2) / len(set1 | set2)

# Compute similarities
similarity_scores = [
    jaccard_similarity(llm_langs, human_langs)
    for human_langs in human_langs_list
]

# Average similarity
average_similarity = sum(similarity_scores) / len(similarity_scores)

# Output results
for i, score in enumerate(similarity_scores):
    print(f"Similarity between LLM-generated and Human-{i+1}: {score:.4f}")

print(f"Average Similarity: {average_similarity:.4f}")

