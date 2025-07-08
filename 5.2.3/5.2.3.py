import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches  # <-- added for legend
import os

# ==== File paths ====
input_file = r"Input containing Top 100 recommended papers From 2011-2024 of Mobile Edge Computing.xlsx"
output_excel = r"Keyword_Counts_Cleaned.xlsx"
output_image = r"Keyword_BarGraph.png"

# ==== Load top 100 rows ====
df = pd.read_excel(input_file,nrows=100)

# ==== Columns to search ====
columns_to_search = ['Abstract', 'Author Keywords', 'Index Keywords']
for col in columns_to_search:
    df[col] = df[col].astype(str).str.lower()

# ==== Cleaned list of unique keywords ====
goals = [
    "energy utilization", "resource allocation", "quality of service", "resource management",
    "green computing", "energy-consumption", "energy efficiency", "decision making",
    "wireless communications", "scheduling algorithms", "computational efficiency",
    "economic and social effects", "information management", "network security",
    "low-latency communication"
]

techniques = [
    "computation offloading", "reinforcement learning", "task analysis", "deep learning",
    "job analysis", "task offloading", "optimization", "integer programming",
    "deep reinforcement learning", "multiaccess", "computational modelling",
    "network architecture", "learning algorithms", "heuristic algorithms", "iterative methods",
    "markov processes", "nonlinear programming", "game theory", "convex optimization",
    "computation resources", "learning systems", "multi agent systems", "bandwidth",
    "approximation algorithms", "computational complexity", "optimization problems",
    "benchmarking", "machine learning", "transfer functions"
]

# ==== Merged keyword aliases ====
keyword_aliases = {
    "resources allocation": "resource allocation",
    "quality-of-service": "quality of service",
    "optimisations": "optimization",
    "reinforcement learnings": "reinforcement learning"
}

# ==== Count keyword occurrences ====
results = []
for keyword, kw_type in [(kw, 'Goal') for kw in goals] + [(kw, 'Technique') for kw in techniques]:
    keyword_lower = keyword.lower()
    # Gather all aliases mapped to this keyword
    variants = [k for k, v in keyword_aliases.items() if v == keyword_lower]
    all_forms = [keyword_lower] + variants

    count = df.apply(
        lambda row: any(
            any(form in row[col] for form in all_forms)
            for col in columns_to_search
        ),
        axis=1
    ).sum()

    results.append({'Keyword': keyword, 'Type': kw_type, 'Count': count})

# ==== Save to Excel ====
result_df = pd.DataFrame(results)
result_df.to_excel(output_excel, index=False)
print("✅ Keyword count saved to Excel:", output_excel)

# ==== Plot and save the bar graph ====
plt.figure(figsize=(20, 8))
x_labels = result_df['Keyword']
y_values = result_df['Count']
bar_colors = ['skyblue' if t == 'Goal' else 'lightgreen' for t in result_df['Type']]

bars = plt.bar(x_labels, y_values, color=bar_colors)

# Add count values above bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, str(yval),
             ha='center', va='bottom', fontsize=8)

# Add legend for colors
goal_patch = mpatches.Patch(color='skyblue', label='Goal')
tech_patch = mpatches.Patch(color='lightgreen', label='Technique')
plt.legend(handles=[goal_patch, tech_patch], loc='upper right', fontsize=10)

plt.xticks(rotation=90, fontsize=8)
plt.xlabel("Keywords (Goals & Techniques)", fontsize=12)
plt.ylabel("Number of Papers", fontsize=12)
plt.title("Keyword Occurrence in Total Dataset (3400+ Papers)", fontsize=14)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Save image
plt.savefig(output_image, dpi=300)
print("✅ Bar graph image saved to:", output_image)

# Show the plot
plt.show()
