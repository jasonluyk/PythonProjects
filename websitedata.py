import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

# Load Excel file
file_path = "report_qr_Nov 11, 2025_08-57.xlsx"
df = pd.read_excel(file_path)

# Select relevant columns and clean data
df = df.iloc[:, [2, 3, 4]]  # Columns C, D, and E
df.columns = ["Time", "Country", "City"]
df.dropna(inplace=True)

# Convert time to datetime if possible
df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
df.dropna(subset=["Time"], inplace=True)

# Group data by date and country (for heatmap simplicity)
df["Date"] = df["Time"].dt.date
# --- Bar Chart by City ---
city_counts = df["City"].value_counts().head(16)  # Top 15 cities
grouped = df.groupby(["Date", "City"]).size().reset_index(name="Count")


plt.figure(figsize=(10, 6))
city_counts.plot(kind="bar", color="skyblue")
plt.title("Top 15 Cities by Number of Reports")
plt.xlabel("City")
plt.ylabel("Number of Reports")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# --- Donut Chart by Country ---
country_counts = df["Country"].value_counts()

plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(
    country_counts,
    labels=country_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops=dict(width=0.5)
)
plt.setp(autotexts, size=10, weight="bold", color="white")
plt.title("Reports by Country (Donut Chart)")
plt.tight_layout()
plt.show()

top_cities = df["City"].value_counts().head(10).index
grouped = grouped[grouped["City"].isin(top_cities)]

dates = sorted(grouped["Date"].unique())
cities = list(top_cities)
xpos, ypos = np.meshgrid(np.arange(len(dates)), np.arange(len(cities)), indexing="ij")

count_matrix = np.zeros_like(xpos, dtype=float)
for i, date in enumerate(dates):
    for j, city in enumerate(cities):
        count = grouped[(grouped["Date"] == date) & (grouped["City"] == city)]["Count"]
        count_matrix[i, j] = count.values[0] if not count.empty else 0

xpos = xpos.flatten()
ypos = ypos.flatten()
zpos = np.zeros_like(xpos)
dx = dy = 0.5
dz = count_matrix.flatten()

# --- Version 1: Single Color ---
fig = plt.figure(figsize=(14, 8))
ax = fig.add_subplot(111, projection="3d")
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color="steelblue", shade=True)

ax.set_xticks(np.arange(len(dates)))
ax.set_xticklabels([d.strftime("%b %d") for d in dates], rotation=45, ha="right")
ax.set_yticks(np.arange(len(cities)))
ax.set_yticklabels(cities)
ax.set_xlabel("Date")
ax.set_ylabel("City")
ax.set_zlabel("Number of Reports")
ax.set_title("3D Clustered Bar Chart – Reports by City and Date (Single Color)")
plt.tight_layout()
plt.show()

# --- Version 2: Multi-Color by City ---
colors = cm.tab10(np.linspace(0, 1, len(cities)))  # unique color per city
city_colors = {city: colors[i] for i, city in enumerate(cities)}
bar_colors = [city_colors[cities[j % len(cities)]] for j in ypos]

fig = plt.figure(figsize=(14, 8))
ax = fig.add_subplot(111, projection="3d")
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=bar_colors, shade=True)

ax.set_xticks(np.arange(len(dates)))
ax.set_xticklabels([d.strftime("%b %d") for d in dates], rotation=45, ha="right")
ax.set_yticks(np.arange(len(cities)))
ax.set_yticklabels(cities)
ax.set_xlabel("Date")
ax.set_ylabel("City")
ax.set_zlabel("Number of Reports")
ax.set_title("3D Clustered Bar Chart – Reports by City and Date (Color by City)")
plt.tight_layout()
plt.show()
