import random
import json
import time

# Simulated roles for testing
roles = ["Data Analyst", "Software Engineer", "UX Designer", "General", "Project Manager"]

# Simulated metrics structure
metrics = {
    'total_analyses': 0,
    'job_role_counts': {},
    'api_response_times': [],
    'successful_analyses': 0,
    'failed_analyses': 0
}

# Simulate 2000 resume uploads
for _ in range(2000):
    role = random.choice(roles)
    response_time = round(random.uniform(1.2, 3.0), 2)  # Simulate response time in seconds
    success = random.random() < 0.95  # 95% success rate

    metrics['total_analyses'] += 1
    metrics['job_role_counts'][role] = metrics['job_role_counts'].get(role, 0) + 1
    metrics['api_response_times'].append(response_time)

    if success:
        metrics['successful_analyses'] += 1
    else:
        metrics['failed_analyses'] += 1

# Save to metrics.json (overwrite current file)
with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("Simulated metrics saved.")
