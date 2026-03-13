import json
import pandas as pd
import matplotlib.pyplot as plt

# Load and parse nested JSON
with open('ipabusedb.json', 'r') as f:
    raw_data = json.load(f)

# Extract nested data
records = []
for entry in raw_data['data']:
    data = entry['data']
    records.append({
        'countryCode': data['countryCode'],
        'abuseConfidenceScore': data['abuseConfidenceScore']
    })

df = pd.DataFrame(records)
print(df)

# Create figure with subplots
#fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig, (ax1) = plt.subplots(1, figsize=(12, 5))

# Bar plot: Average score by country
country_avg = df.groupby('countryCode')['abuseConfidenceScore'].mean()
bars = ax1.bar(country_avg.index, country_avg.values, 
               color=['#ff6b6b', '#4ecdc4'], alpha=0.8)
ax1.set_title('Average Abuse Score by Country')
ax1.set_ylabel('Confidence Score')
ax1.set_ylim(0, 110)

# Add value labels on bars
#for bar in bars:
#    height = bar.get_height()
#    ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
#             f'{int(height)}', ha='center', va='bottom')

# Scatter plot: Individual scores
#colors = {'US': '#ff6b6b', 'IN': '#4ecdc4', 'VN': '#4ecdc6', 'NL': '#4ecdc6' , 'CN': '#4ecdc6' , 'DE': '#4ecdc6', \
#        'SG': '#4ecdc6', 'BR': '#4ecdc6', 'FI': '#4ecdc6', 'FR': '#4ecdc6', 'LT': '#4ecdc6', 'DO': '#4ecdc6', \
#        'CA': '#4ecdc6', 'HK': '#4ecdc6', 'MA': '#4ecdc6', 'SE': '#4ecdc6', 'TR': '#4ecdc6', 'UA': '#4ecdc6', \
#        'AR': '#4ecdc6', 'AU': '#4ecdc6', 'GB': '#4ecdc6', 'RU': '#4ecdc6', 'KR': '#4ecdc6', 'NO': '#4ecdc6', \
#        'IE': '#4ecdc6', 'JP': '#4ecdc6', 'PL': '#4ecdc6', 'LU': '#4ecdc6', 'MK': '#4ecdc6', 'LV': '#4ecdc6', \
#        'IS': '#4ecdc6'}
#for country in df['countryCode'].unique():
#    subset = df[df['countryCode'] == country]
#    ax2.scatter([country] * len(subset), subset['abuseConfidenceScore'], 
#                c=colors[country], s=200, alpha=0.8, label=country)
#ax2.set_title('Individual Abuse Scores by Country')
#ax2.set_ylabel('Confidence Score')
#ax2.set_ylim(0, 110)
#ax2.legend()
#ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('abuse_scores_by_country.png', dpi=300, bbox_inches='tight')
plt.show()

