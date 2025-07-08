import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import defaultdict

def build_keyword_occurrence_matrix(book_files, goal_aliases, technique_aliases, goals_raw, techniques_raw):
    year_ranges = list(book_files.keys())
    canonical_goals = sorted({goal_aliases.get(g, g) for g in goals_raw})
    canonical_techniques = sorted({technique_aliases.get(t, t) for t in techniques_raw})
    all_keywords = canonical_goals + canonical_techniques  # GOALS FIRST, THEN TECHNIQUES

    data = {k: defaultdict(int) for k in all_keywords}

    for year, file_path in book_files.items():
        df = pd.read_excel(file_path, usecols=["Abstract", "Author Keywords", "Index Keywords"])

        for _, row in df.iterrows():
            text = " ".join(str(row[col]) for col in df.columns if pd.notna(row[col])).lower()

            seen = set()
            for raw in goals_raw:
                canon = goal_aliases.get(raw, raw)
                if raw.lower() in text:
                    seen.add(canon)
            for raw in techniques_raw:
                canon = technique_aliases.get(raw, raw)
                if raw.lower() in text:
                    seen.add(canon)

            for keyword in seen:
                data[keyword][year] += 1

    return data, year_ranges, canonical_goals, canonical_techniques

def save_occurrence_csv(data, year_ranges, canonical_goals, canonical_techniques, output_csv_path):
    rows = []
    for keyword in canonical_goals + canonical_techniques:
        for year in year_ranges:
            count = data[keyword].get(year, 0)
            if count > 0:
                rows.append({
                    "Keyword": keyword,
                    "Type": "Goal" if keyword in canonical_goals else "Technique",
                    "Year Range": year,
                    "Count": count
                })
    df = pd.DataFrame(rows)
    df.to_csv(output_csv_path, index=False)
    print(f"✅ CSV file saved to: {output_csv_path}")

def plot_stacked_bar_chart(data, year_ranges, canonical_goals, canonical_techniques, output_path):
    all_keywords = canonical_goals + canonical_techniques
    year_colors = plt.cm.tab10.colors
    bar_data = {year: [data[k].get(year, 0) for k in all_keywords] for year in year_ranges}

    plt.figure(figsize=(18, 8))
    bottoms = [0] * len(all_keywords)

    for idx, year in enumerate(year_ranges):
        heights = bar_data[year]
        bars = plt.bar(all_keywords, heights, bottom=bottoms, color=year_colors[idx % len(year_colors)], 
                       label=year)

        for i, bar in enumerate(bars):
            if heights[i] > 0:
                plt.text(bar.get_x() + bar.get_width() / 2, bottoms[i] + heights[i] / 2,
                         str(heights[i]), ha='center', va='center', fontsize=8, color='white')

        bottoms = [bottoms[i] + heights[i] for i in range(len(heights))]

    tick_colors = []
    for label in all_keywords:
        if label in canonical_goals:
            tick_colors.append('blue')
        elif label in canonical_techniques:
            tick_colors.append('green')
        else:
            tick_colors.append('black')

    plt.xticks(ticks=range(len(all_keywords)), labels=all_keywords, rotation=45, ha='right', fontsize=9)
    ax = plt.gca()
    for tick_label, color in zip(ax.get_xticklabels(), tick_colors):
        tick_label.set_color(color)

    plt.ylabel("Total Occurrences Across Years", fontsize=12)
    plt.xlabel("Keywords (Blue: Goal, Green: Technique)", fontsize=12)
    plt.title("Stacked Keyword Occurrences Across Time Periods", fontsize=14)
    plt.legend(title="Year Range")
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"✅ Stacked bar chart saved to: {output_path}")

# === SETTINGS ===
book_files = {
    "2011-2013": r"Top  10 Papers from Year span\2011-2013.xlsx",
    "2014-2016": r"Top  10 Papers from Year span\2014-2016.xlsx",
    "2017-2019": r"Top  10 Papers from Year span\2017-2019.xlsx",
    "2020-2022": r"Top  10 Papers from Year span\2020-2022.xlsx",
    "2023-2024": r"Top  10 Papers from Year span\2023-2024.xlsx",
}

goal_aliases = {
    "resources allocation": "resource allocation",
    "quality-of-service": "quality of service",
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

# === OUTPUT PATHS ===
output_chart = r"stacked_keyword_occurrences_colored_ordered.png"
output_csv = r"stacked_keyword_occurrences_data.csv"

# === RUN ===
data, year_ranges, canonical_goals, canonical_techniques = build_keyword_occurrence_matrix(
    book_files, goal_aliases, technique_aliases, goals_raw, techniques_raw
)

# Plot graph
plot_stacked_bar_chart(data, year_ranges, canonical_goals, canonical_techniques, output_chart)

# Save CSV
save_occurrence_csv(data, year_ranges, canonical_goals, canonical_techniques, output_csv)
