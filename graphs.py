import json
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

# Load JSON from file (save your JSON as 'ip_data.json')
with open('ipabusedb.json', 'r') as f:
    data = json.load(f)

# Extract countryCode from nested structure
countries = []
for item in data['data']:
    country_code = item['data']['countryCode']
    countries.append(country_code)

# Count occurrences
country_counts = Counter(countries)
print("Country counts:", dict(country_counts))

# Create figure with subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Bar chart
countries_list = list(country_counts.keys())
counts = list(country_counts.values())
bars = ax1.bar(countries_list, counts, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
ax1.set_title('Country Code Distribution')
ax1.set_ylabel('Number of IPs')
ax1.set_xlabel('Country Code')

# Add value labels on bars
for bar, count in zip(bars, counts):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.05,
             f'{count}', ha='center', va='bottom')

# Pie chart
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
wedges, texts, autotexts = ax2.pie(counts, labels=countries_list, autopct='%1.1f%%',
                                   colors=colors, startangle=90)
ax2.set_title('Country Code Percentage')

plt.tight_layout()

# Save the complete figure with both charts as PNG
plt.savefig('country_distribution.png', dpi=300, bbox_inches='tight')
print("Saved combined chart: country_distribution.png")

# Save individual charts
# Bar chart only
fig_bar, ax_bar = plt.subplots(figsize=(8, 6))
ax_bar.bar(countries_list, counts, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
ax_bar.set_title('Country Code Distribution')
ax_bar.set_ylabel('Number of IPs')
ax_bar.set_xlabel('Country Code')
for bar, count in zip(ax_bar.patches, counts):
    height = bar.get_height()
    ax_bar.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{count}', ha='center', va='bottom')
plt.tight_layout()
fig_bar.savefig('bar_chart.png', dpi=300, bbox_inches='tight')
plt.close(fig_bar)
print("Saved bar chart: bar_chart.png")

# Pie chart only
fig_pie, ax_pie = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax_pie.pie(counts, labels=countries_list, autopct='%1.1f%%',
                                      colors=colors, startangle=90)
ax_pie.set_title('Country Code Percentage')
plt.tight_layout()
fig_pie.savefig('pie_chart.png', dpi=300, bbox_inches='tight')
plt.close(fig_pie)
print("Saved pie chart: pie_chart.png")

# Optionally still show the plots
plt.show()

