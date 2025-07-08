import os
import pandas as pd
import json
from collections import defaultdict, Counter

# Define paths
base_path = r"Splitting Dataset into 5 Time periods"
csv_files = [
    "2011_2013.csv", "2014_2016.csv", "2017_2019.csv",
    "2020_2022.csv", "2023_2024.csv"
]

# Define goals and technique aliases
goal_aliases = {
    "resources allocation": "resource allocation",
    "quality-of-service": "quality of service"
}
technique_aliases = {
    "optimisations": "optimization",
    "reinforcement learnings": "reinforcement learning"
}

goals_raw = [
    "computational efficiency", "decision making", "economic and social effects", "energy efficiency",
    "energy utilization", "energy-consumption", "green computing", "information management",
    "low-latency communication", "network security", "quality of service", "quality-of-service",
    "resource allocation", "resource management", "resources allocation", "scheduling algorithms",
    "wireless communications"
]

techniques_raw = [
    "approximation algorithms", "bandwidth", "benchmarking", "computation offloading",
    "computation resources", "computational complexity", "computational modelling",
    "convex optimization", "deep learning", "deep reinforcement learning", "game theory",
    "heuristic algorithms", "integer programming", "iterative methods", "job analysis",
    "learning algorithms", "learning systems", "machine learning", "markov processes",
    "multi agent systems", "multiaccess", "network architecture", "nonlinear programming",
    "optimisations", "optimization", "optimization problems", "reinforcement learning",
    "reinforcement learnings", "task analysis", "task offloading", "transfer functions"
]

# Normalize lists
goals = list({goal_aliases.get(g, g) for g in goals_raw})
techniques = list({technique_aliases.get(t, t) for t in techniques_raw})

# Combine all results
all_results = []

# Combined text output path
combined_txt_path = os.path.join(base_path, "combined_goal_technique_analysis.txt")
with open(combined_txt_path, 'w', encoding='utf-8') as tf:

    for csv_file in csv_files:
        print(f"\n==== Processing {csv_file} ====")
        file_path = os.path.join(base_path, csv_file)
        df = pd.read_csv(file_path).fillna('')

        goal_occurrence = Counter()
        goal_to_technique_counter = defaultdict(Counter)

        for _, row in df.iterrows():
            text = f"{row.get('Abstract', '')} {row.get('Author Keywords', '')}{row.get('Index Keywords', '')}".lower()
        

            found_goals = {
                goal_aliases.get(g, g)
                for g in goals_raw if g.lower() in text
            }

            found_techniques = {
                technique_aliases.get(t, t)
                for t in techniques_raw if t.lower() in text
            }

            for g in found_goals:
                goal_occurrence[g] += 1
                goal_to_technique_counter[g].update(found_techniques)

        results = []
        period_label = csv_file.replace(".csv", "")
        tf.write(f"\n===== Period: {period_label} =====\n\n")

        for goal in goal_occurrence:
            techs = goal_to_technique_counter[goal].most_common(3)
            row = {
                "Time Period": period_label,
                "Goal": goal,
                "Goal Occurrence": goal_occurrence[goal]
            }
            tf.write(f"Goal: {goal} (Occurrences: {goal_occurrence[goal]})\n")
            for i, (tech, count) in enumerate(techs, start=1):
                row[f"Technique {i}"] = tech
                row[f"Count {i}"] = count
                tf.write(f"  Technique {i}: {tech} (Count: {count})\n")
            tf.write("\n")
            results.append(row)

        all_results.extend(results)
    print(f"✅ Combined text file saved to: {combined_txt_path}")

# Save all results to a single CSV
combined_csv_path = os.path.join(base_path, "combined_goal_technique_analysis.csv")
combined_df = pd.DataFrame(all_results)
combined_df.to_csv(combined_csv_path, index=False)
print(f"✅ Combined CSV file saved to: {combined_csv_path}")
