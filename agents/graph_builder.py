import json

def build_claim_graph_html(claim: str, sources: list, analysis: dict) -> str:
    nodes = []
    edges = []

    claim_label = claim[:55] + "..." if len(claim) > 55 else claim
    verdict = analysis.get("verdict", "UNVERIFIED")
    verdict_colors = {
        "TRUE": "#1D9E75",
        "FALSE": "#E24B4A",
        "MISLEADING": "#BA7517",
        "UNVERIFIED": "#888780"
    }
    claim_color = verdict_colors.get(verdict, "#888780")

    nodes.append({
        "id": 0,
        "label": f"CLAIM\n{claim_label}",
        "color": {"background": claim_color, "border": claim_color, "highlight": {"background": claim_color}},
        "font": {"color": "#ffffff", "size": 12, "bold": True},
        "shape": "box",
        "borderWidth": 2,
        "size": 30,
        "x": 0,
        "y": 0
    })

    supporting = analysis.get("supporting_sources", [])
    contradicting = analysis.get("contradicting_sources", [])

    for i, s in enumerate(sources):
        if not s.get("url"):
            continue
        url = s["url"]
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]
        title = s.get("title", domain)
        label = (title[:40] + "...") if len(title) > 40 else title

        if url in supporting:
            bg = "#E1F5EE"
            border = "#1D9E75"
            font_color = "#085041"
            edge_color = "#1D9E75"
            edge_label = "supports"
        elif url in contradicting:
            bg = "#FCEBEB"
            border = "#E24B4A"
            font_color = "#501313"
            edge_color = "#E24B4A"
            edge_label = "contradicts"
        else:
            bg = "#F1EFE8"
            border = "#888780"
            font_color = "#2C2C2A"
            edge_color = "#888780"
            edge_label = "related"

        nodes.append({
            "id": i + 1,
            "label": label,
            "title": f'<a href="{url}" target="_blank">{title}</a><br>{s.get("snippet","")[:120]}...',
            "color": {"background": bg, "border": border, "highlight": {"background": bg, "border": border}},
            "font": {"color": font_color, "size": 11},
            "shape": "box",
            "borderWidth": 1.5,
            "url": url
        })
        edges.append({
            "from": 0,
            "to": i + 1,
            "color": {"color": edge_color, "opacity": 0.7},
            "label": edge_label,
            "font": {"size": 9, "color": edge_color},
            "arrows": "to",
            "width": 1.5
        })

    nodes_json = json.dumps(nodes)
    edges_json = json.dumps(edges)

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<style>
  body {{ margin: 0; background: transparent; }}
  #graph {{ width: 100%; height: 380px; background: transparent; }}
</style>
</head>
<body>
<div id="graph"></div>
<script>
const nodes = new vis.DataSet({nodes_json});
const edges = new vis.DataSet({edges_json});
const container = document.getElementById('graph');
const options = {{
  physics: {{
    enabled: true,
    stabilization: {{ iterations: 150 }},
    barnesHut: {{ gravitationalConstant: -3000, springLength: 140 }}
  }},
  interaction: {{ hover: true, tooltipDelay: 100 }},
  layout: {{ improvedLayout: true }},
  nodes: {{ borderWidth: 1.5, borderWidthSelected: 2.5, margin: 8 }},
  edges: {{ smooth: {{ type: "cubicBezier" }} }}
}};
const network = new vis.Network(container, {{ nodes, edges }}, options);
network.on("click", function(params) {{
  if (params.nodes.length > 0) {{
    const node = nodes.get(params.nodes[0]);
    if (node && node.url) window.open(node.url, '_blank');
  }}
}});
</script>
</body>
</html>"""
    return html
