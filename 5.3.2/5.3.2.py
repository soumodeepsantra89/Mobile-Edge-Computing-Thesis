import pandas as pd

# ==== File and Paths ====
file_path = "Mobile Edge computing dataset.csv"
output_file_path = "top_goals_techniques_filtered.xlsx"

# ==== Load CSV ====
data = pd.read_csv(file_path, low_memory=False)

# ==== Normalize text columns ====
for col in ['Abstract', 'Author Keywords', 'Index Keywords']:
    data[col] = data[col].astype(str).str.lower()

# ==== Alias Mappings ====
goal_aliases = {
    "resources allocation": "resource allocation",
    "quality-of-service": "quality of service"
}

technique_aliases = {
    "optimisations": "optimization",
    "reinforcement learnings": "reinforcement learning"
}

# ==== Master Keyword Lists ====
goals_raw = [
    "resource allocation", "energy utilization", "quality of service", "resource management",
    "resources allocation", "green computing", "energy efficiency", "energy-consumption",
    "decision making", "quality-of-service", "network security", "information management",
    "scheduling algorithms", "economic and social effects", "low-latency communication",
    "wireless communications", "computational efficiency"
]

techniques_raw = [
    "computation offloading", "reinforcement learning", "task analysis", "deep learning",
    "job analysis", "task offloading", "reinforcement learnings", "optimisations", "optimization",
    "integer programming", "deep reinforcement learning", "multiaccess", "computational modelling",
    "network architecture", "learning algorithms", "heuristic algorithms", "iterative methods",
    "markov processes", "nonlinear programming", "game theory", "convex optimization",
    "computation resources", "learning systems", "multi agent systems", "bandwidth",
    "approximation algorithms", "computational complexity", "optimization problems",
    "benchmarking", "machine learning", "transfer functions"
]

# ==== Normalize keyword lists ====
goals = list({goal_aliases.get(g, g) for g in goals_raw})
techniques = list({technique_aliases.get(t, t) for t in techniques_raw})

# ==== Year Ranges ====
year_ranges = {
    "2011-2013": (2011, 2013),
    "2014-2016": (2014, 2016),
    "2017-2019": (2017, 2019),
    "2020-2022": (2020, 2022),
    "2023-2024": (2023, 2024)
}

# ==== Initialize Count Containers ====
technique_doc_count = {
    yr: {dt: {tech: 0 for tech in techniques} for dt in ["Article", "Conference paper", "Book chapter"]}
    for yr in year_ranges
}
goal_doc_count = {
    yr: {dt: {goal: 0 for goal in goals} for dt in ["Article", "Conference paper", "Book chapter"]}
    for yr in year_ranges
}

# ==== Iterate and Count ====
for _, row in data.iterrows():
    year = row.get("Year", None)
    doc_type = row.get("Document Type", "")
    if pd.isna(year) or doc_type not in ["Article", "Conference paper", "Book chapter"]:
        continue

    # Find year slot
    for range_label, (start, end) in year_ranges.items():
        if start <= year <= end:
            # Combine text fields
            text = f"{row['Abstract']} {row['Author Keywords']} {row['Index Keywords']}"

            # Check techniques
            for raw_tech in techniques_raw:
                canonical_tech = technique_aliases.get(raw_tech, raw_tech)
                if raw_tech in text:
                    technique_doc_count[range_label][doc_type][canonical_tech] += 1

            # Check goals
            for raw_goal in goals_raw:
                canonical_goal = goal_aliases.get(raw_goal, raw_goal)
                if raw_goal in text:
                    goal_doc_count[range_label][doc_type][canonical_goal] += 1

# ==== Prepare Output ====
output_data = []

for yr in year_ranges:
    for doc_type in ["Article", "Conference paper", "Book chapter"]:
        top_techniques = sorted(technique_doc_count[yr][doc_type].items(), key=lambda x: x[1], reverse=True)[:6]
        top_goals = sorted(goal_doc_count[yr][doc_type].items(), key=lambda x: x[1], reverse=True)[:5]

        for tech, count in top_techniques:
            if count > 0:
                output_data.append([yr, doc_type, "Technique", tech, count])
        for goal, count in top_goals:
            if count > 0:
                output_data.append([yr, doc_type, "Goal", goal, count])

# ==== Export to Excel ====
df_results = pd.DataFrame(output_data, columns=["Year Range", "Document Type", "Category", "Name", "Count"])
df_results.to_excel(output_file_path, index=False)

print(f"✅ Filtered data with alias normalization saved to: {output_file_path}")
