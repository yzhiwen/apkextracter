import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os

df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'apk.csv'))

fig = go.Figure()

# https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.Sunburst.html
# help(go.Sunburst)

fig.add_trace(go.Sunburst(
    ids=df.ids,
    labels=df.labels,
    parents=df.pids,
    values=df.zipsizes,
    # domain=dict(column=1),
    maxdepth=2,
    # insidetextorientation='radial',
    branchvalues="total", # total
))

fig.update_layout(
    title = 'title',
    margin = dict(t=50, l=50, r=50, b=50),
)

out = os.path.join(os.path.dirname(__file__), "apk.html")
fig.write_html(out)

fig.show()