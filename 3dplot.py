# --- Refined Static 3D Bar Charts ---
from matplotlib import cm

# Common data setup
df["Date"] = df["Time"].dt.date
grouped = df.groupby(["Date", "City"]).size().reset_index(name="Count")

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
