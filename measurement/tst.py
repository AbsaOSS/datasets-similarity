import matplotlib.pyplot as plt
import numpy as np

# Example data
configurations = ['Config 1', 'Config 2', 'Config 3', 'Config 4']
scores = [85, 90, 78, 88]
processing_times = [120, 95, 130, 110]

x = np.arange(len(configurations))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
bars1 = ax.bar(x - width/2, scores, width, label='Score')
bars2 = ax.bar(x + width/2, processing_times, width, label='Processing Time')

# Add labels, title, and legend
ax.set_xlabel('Configurations')
ax.set_ylabel('Values')
ax.set_title('Scores and Processing Times by Configuration')
ax.set_xticks(x)
ax.set_xticklabels(configurations)
ax.legend()

plt.show()
