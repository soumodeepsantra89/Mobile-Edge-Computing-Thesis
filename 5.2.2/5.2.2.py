import pandas as pd

# Load dataset
file_path = "Mobile Edge computing dataset.csv"
data = pd.read_csv(file_path, low_memory=False)

# Define alias mappings
alias_map = {
    "resources allocation": "resource allocation",
    "quality-of-service": "quality of service",
    "optimisations": "optimization",
    "reinforcement learnings": "reinforcement learning"
}

# Define raw lists
goals_raw = [
    "resource allocation", "energy utilization", "quality of service",
    "resource management", "resources allocation", "green computing",
    "energy efficiency", "energy-consumption", "decision making",
    "quality-of-service", "network security", "information management",
    "scheduling algorithms", "economic and social effects",
    "low-latency communication", "wireless communications", "computational efficiency"
]

techniques_raw = [
    "computation offloading", "reinforcement learning", "task analysis", "deep learning",
    "job analysis", "task offloading", "optimisations", "optimization", "integer programming",
    "deep reinforcement learning", "multiaccess", "computational modelling", "network architecture",
    "learning algorithms", "heuristic algorithms", "iterative methods", "markov processes",
    "nonlinear programming", "game theory", "convex optimization", "computation resources",
    "learning systems", "multi agent systems", "bandwidth", "approximation algorithms",
    "computational complexity", "optimization problems", "benchmarking", "machine learning",
    "transfer functions", "reinforcement learnings"
]

# Normalize and build keyword categories
canonical_goals = sorted({alias_map.get(g, g) for g in goals_raw})
canonical_techniques = sorted({alias_map.get(t, t) for t in techniques_raw})

doc_types = ["Article", "Book chapter", "Conference paper"]
goal_doc_count = {g: {dt: 0 for dt in doc_types} for g in canonical_goals}
tech_doc_count = {t: {dt: 0 for dt in doc_types} for t in canonical_techniques}

# Process rows
for _, row in data.iterrows():
    doc_type = row.get("Document Type", "")
    if doc_type not in doc_types:
        continue

    text = " ".join([
        str(row.get("Abstract", "")).lower(),
        str(row.get("Author Keywords", "")).lower(),
        str(row.get("Index Keywords", "")).lower()
    ])

    seen_goals = set()
    seen_techs = set()

    for g in goals_raw:
        canonical = alias_map.get(g, g)
        if g.lower() in text:
            seen_goals.add(canonical)

    for t in techniques_raw:
        canonical = alias_map.get(t, t)
        if t.lower() in text:
            seen_techs.add(canonical)

    for g in seen_goals:
        goal_doc_count[g][doc_type] += 1
    for t in seen_techs:
        tech_doc_count[t][doc_type] += 1

# Convert to DataFrame
goal_rows = [[dt, 'Goal', g, count] for g, counts in goal_doc_count.items() for dt, count in counts.items()]
tech_rows = [[dt, 'Technique', t, count] for t, counts in tech_doc_count.items() for dt, count in 
             counts.items()]
df_all = pd.DataFrame(goal_rows + tech_rows, columns=["Document Type", "Category", "Keyword", "Count"])

# Function to display top 5 for each category and document type
def display_top_5_by_category(df):
    for doc_type in doc_types:
        for category in ["Goal", "Technique"]:
            print(f"\nTop 5 {category}s for {doc_type}:")
            subset = df[(df["Document Type"] == doc_type) & (df["Category"] == category)]
            top_5 = subset.nlargest(5, "Count")
            for _, row in top_5.iterrows():
                print(f"  {row['Keyword']}: {row['Count']}")

# Display the results
display_top_5_by_category(df_all)
