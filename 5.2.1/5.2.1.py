import json

# Load JSON data
json_path = "JSON File obtained from VOSViewer.json"
with open(json_path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# List of goals (normalized to lowercase)
goals = {
    "energy utilization", "resource allocation", "quality of service", "resource management",
    "resources allocation", "green computing", "energy-consumption", "energy efficiency",
    "decision making", "quality-of-service", "wireless communications", "scheduling algorithms",
    "computational efficiency", "economic and social effects", "information management",
    "network security", "low-latency communication"
}

# List of techniques (normalized to lowercase)
techniques = {
    "computation offloading", "reinforcement learning", "task analysis", "deep learning",
    "job analysis", "task offloading", "reinforcement learnings", "optimisations", "optimization",
    "integer programming", "deep reinforcement learning", "multiaccess", "computational modelling",
    "network architecture", "learning algorithms", "heuristic algorithms", "iterative methods",
    "markov processes", "nonlinear programming", "game theory", "convex optimization",
    "computation resources", "learning systems", "multi agent systems", "bandwidth",
    "approximation algorithms", "computational complexity", "optimization problems",
    "benchmarking", "machine learning", "transfer functions"
}

# Keyword normalization mappings
goal_aliases = {
    "resources allocation": "resource allocation",
    "quality-of-service": "quality of service"
}
technique_aliases = {
    "reinforcement learnings": "reinforcement learning",
    "optimisations": "optimization"
}

# Apply normalization
goals = {goal_aliases.get(g, g) for g in goals}
techniques = {technique_aliases.get(t, t) for t in techniques}

# Extract data
items = data['network']['items']
links = data['network']['links']

# Create ID-to-keyword mapping
id_to_keyword = {item['id']: item['label'].lower() for item in items}
keyword_to_id = {item['label'].lower(): item['id'] for item in items}

# Normalize keyword labels using aliases
normalized_id_to_keyword = {
    item['id']: goal_aliases.get(item['label'].lower(),
                technique_aliases.get(item['label'].lower(), item['label'].lower()))
    for item in items
}

# Collect results
results = {}

for goal in goals:
    keyword_id = keyword_to_id.get(goal)
    if keyword_id is None:
        results[goal] = "Not found"
        continue

    # Collect connected keywords and strengths
    connected_keywords_strength = [
        (normalized_id_to_keyword[link['target_id']], link['strength'])
        if link['source_id'] == keyword_id else
        (normalized_id_to_keyword[link['source_id']], link['strength'])
        for link in links
        if link['source_id'] == keyword_id or link['target_id'] == keyword_id
    ]

    # Filter to techniques only
    connected_techniques = [(kw, strength) for kw, strength in connected_keywords_strength if kw in techniques]

    # Get top 5
    top_5 = sorted(connected_techniques, key=lambda x: x[1], reverse=True)[:5]

    results[goal] = top_5 if top_5 else "No technique connections found"

# Print results
for goal, top_techs in results.items():
    print(f"\nGoal: {goal.capitalize()}")
    if isinstance(top_techs, str):
        print(top_techs)
    else:
        for tech, strength in top_techs:
            print(f"  {tech} (Strength: {strength})")
