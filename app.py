import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(
    page_title="FactTrace — Misinformation Detector",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.main { background: #0a0a0f; }
.block-container { padding: 2rem 2rem 4rem; max-width: 1400px; }

.hero-header { text-align: center; padding: 2.5rem 0 1.5rem; margin-bottom: 2rem; }
.hero-title { font-family: 'Syne', sans-serif; font-size: 3rem; font-weight: 800; letter-spacing: -0.03em; color: #f0ede8; margin: 0; line-height: 1; }
.hero-title span { color: #e24b4a; }
.hero-subtitle { font-family: 'DM Mono', monospace; font-size: 0.75rem; color: #5f5e5a; letter-spacing: 0.15em; margin-top: 0.6rem; text-transform: uppercase; }

.stTextArea textarea { background: #12121a !important; border: 1px solid #2a2a35 !important; border-radius: 12px !important; color: #d4d0c8 !important; font-family: 'DM Mono', monospace !important; font-size: 0.88rem !important; line-height: 1.7 !important; padding: 1rem !important; }
.stTextArea textarea:focus { border-color: #e24b4a !important; box-shadow: 0 0 0 2px rgba(226,75,74,0.15) !important; }

.stButton > button[kind="primary"] { background: #e24b4a !important; color: #fff !important; border: none !important; border-radius: 8px !important; font-family: 'Syne', sans-serif !important; font-weight: 700 !important; font-size: 0.9rem !important; letter-spacing: 0.05em !important; padding: 0.65rem 2rem !important; transition: all 0.2s !important; }
.stButton > button[kind="primary"]:hover { background: #c93938 !important; transform: translateY(-1px) !important; }
.stButton > button[kind="secondary"] { background: transparent !important; color: #888780 !important; border: 1px solid #2a2a35 !important; border-radius: 8px !important; font-family: 'DM Mono', monospace !important; font-size: 0.8rem !important; }

.claim-card { background: #12121a; border: 1px solid #2a2a35; border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; }
.claim-number { font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #e24b4a; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 0.4rem; }
.claim-text { font-size: 1rem; font-weight: 600; color: #f0ede8; line-height: 1.5; margin-bottom: 0; }

.verdict-badge { display: inline-block; padding: 4px 14px; border-radius: 99px; font-family: 'DM Mono', monospace; font-size: 0.72rem; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 1rem; }
.verdict-TRUE    { background: #0d2b1f; color: #1D9E75; border: 1px solid #1D9E75; }
.verdict-FALSE   { background: #2b0d0d; color: #E24B4A; border: 1px solid #E24B4A; }
.verdict-MISLEADING { background: #2b1f00; color: #EF9F27; border: 1px solid #EF9F27; }
.verdict-UNVERIFIED { background: #1a1a1a; color: #888780; border: 1px solid #444441; }

.score-container { margin: 0.8rem 0; }
.score-label { font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #5f5e5a; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.3rem; display: flex; justify-content: space-between; }
.score-track { background: #1e1e28; border-radius: 99px; height: 6px; width: 100%; overflow: hidden; }
.score-fill-high { background: #1D9E75; border-radius: 99px; height: 100%; }
.score-fill-mid  { background: #EF9F27; border-radius: 99px; height: 100%; }
.score-fill-low  { background: #E24B4A; border-radius: 99px; height: 100%; }

.score-rubric { background: #0e0e16; border: 1px solid #1e1e28; border-radius: 8px; padding: 0.75rem 1rem; margin: 0.6rem 0 1rem; }
.rubric-row { display: flex; justify-content: space-between; align-items: center; padding: 2px 0; font-family: 'DM Mono', monospace; font-size: 0.68rem; }
.rubric-range { color: #444441; min-width: 60px; }
.rubric-label { color: #9e9b93; flex: 1; padding-left: 8px; }
.rubric-active { background: #16161f; border-radius: 4px; padding: 2px 6px; }

.reasoning-box { background: #0e0e16; border-left: 3px solid #2a2a35; border-radius: 0 8px 8px 0; padding: 0.8rem 1rem; font-size: 0.88rem; color: #9e9b93; line-height: 1.65; margin: 0.8rem 0; }
.key-finding { background: #16161f; border: 1px solid #2a2a35; border-radius: 8px; padding: 0.6rem 1rem; font-family: 'DM Mono', monospace; font-size: 0.8rem; color: #d4d0c8; margin: 0.6rem 0; }
.bias-flag { display: inline-block; background: #1e140a; color: #BA7517; border: 1px solid #854F0B; border-radius: 6px; font-family: 'DM Mono', monospace; font-size: 0.7rem; padding: 2px 8px; margin: 2px 3px 2px 0; }

.source-chip { display: flex; align-items: flex-start; gap: 8px; padding: 0.6rem 0.8rem; border-radius: 8px; margin-bottom: 6px; font-size: 0.82rem; line-height: 1.4; }
.source-support   { background: #0a1f15; border: 1px solid #0F6E56; }
.source-contradict{ background: #1f0a0a; border: 1px solid #A32D2D; }
.source-neutral   { background: #14141c; border: 1px solid #2a2a35; }
.source-dot { width: 7px; height: 7px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
.dot-support    { background: #1D9E75; }
.dot-contradict { background: #E24B4A; }
.dot-neutral    { background: #444441; }

.section-label { font-family: 'DM Mono', monospace; font-size: 0.65rem; color: #444441; letter-spacing: 0.15em; text-transform: uppercase; margin: 1rem 0 0.4rem; }
.thin-divider { border: none; border-top: 1px solid #1e1e28; margin: 1.2rem 0; }

.history-item { background: #12121a; border: 1px solid #1e1e28; border-radius: 10px; padding: 0.75rem; margin-bottom: 0.5rem; }
.history-verdict-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 6px; }

.stSpinner > div { color: #e24b4a !important; }
[data-testid="stSidebar"] { background: #0d0d14 !important; border-right: 1px solid #1e1e28; }
[data-testid="stSidebar"] * { color: #9e9b93; }
h1,h2,h3 { color: #f0ede8 !important; font-family: 'Syne', sans-serif !important; }
label { color: #9e9b93 !important; font-family: 'DM Mono', monospace !important; font-size: 0.78rem !important; }
.stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── Sidebar — history + score guide ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='font-family:DM Mono,monospace;font-size:0.65rem;color:#444441;
    letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.5rem'>
    How scores work
    </div>
    <div style='background:#12121a;border:1px solid #1e1e28;border-radius:10px;padding:0.75rem;margin-bottom:1.2rem'>
      <div style='font-family:DM Mono,monospace;font-size:0.68rem;line-height:2;color:#9e9b93'>
        <span style='color:#1D9E75'>85–100</span> &nbsp;Multiple credible sources confirm<br>
        <span style='color:#5DCAA5'>65–84 </span> &nbsp;Mostly supported, minor gaps<br>
        <span style='color:#EF9F27'>45–64 </span> &nbsp;Mixed or insufficient evidence<br>
        <span style='color:#D85A30'>25–44 </span> &nbsp;Mostly contradicted / misleading<br>
        <span style='color:#E24B4A'>0–24  </span> &nbsp;Clearly false, debunked
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='font-family:DM Mono,monospace;font-size:0.65rem;color:#444441;
    letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.5rem'>
    Analysis history
    </div>""", unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown("<div style='font-size:0.78rem;color:#2a2a35'>No analyses yet.</div>",
                    unsafe_allow_html=True)
    else:
        dot_colors = {"TRUE":"#1D9E75","FALSE":"#E24B4A","MISLEADING":"#EF9F27","UNVERIFIED":"#444441"}
        for item in reversed(st.session_state.history[-10:]):
            vc = dot_colors.get(item.get("overall_verdict","UNVERIFIED"), "#444441")
            snippet = item["input"][:52]+"..." if len(item["input"]) > 52 else item["input"]
            st.markdown(f"""
            <div class='history-item'>
              <span class='history-verdict-dot' style='background:{vc}'></span>
              <span style='font-size:0.75rem;color:#9e9b93'>{snippet}</span>
              <div style='font-family:DM Mono,monospace;font-size:0.65rem;color:#444441;margin-top:4px'>
                {item["num_claims"]} claim(s) &middot; avg {item["avg_score"]}/100
              </div>
            </div>""", unsafe_allow_html=True)

        if st.button("Clear history", type="secondary"):
            st.session_state.history = []
            st.rerun()

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-header'>
  <div class='hero-title'>Fact<span>Trace</span></div>
  <div class='hero-subtitle'>AI-powered misinformation detector &amp; fact tracer &nbsp;·&nbsp; Powered by Groq + Llama 3.3</div>
</div>
""", unsafe_allow_html=True)

# ── Input ────────────────────────────────────────────────────────────────────
user_input = st.text_area(
    "claim_input",
    height=120,
    placeholder="Paste any claim, news snippet, or viral statement here...",
    label_visibility="collapsed"
)

st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
run_btn = st.button("Analyse claim", type="primary")

# ── Helpers ──────────────────────────────────────────────────────────────────
def score_color_class(score):
    if score >= 65: return "score-fill-high"
    if score >= 35: return "score-fill-mid"
    return "score-fill-low"

def rubric_html(active_score):
    bands = [
        ("85–100", "Multiple credible sources confirm", 85),
        ("65–84",  "Mostly supported, minor gaps",      65),
        ("45–64",  "Mixed or insufficient evidence",    45),
        ("25–44",  "Mostly contradicted / misleading",  25),
        ("0–24",   "Clearly false, debunked",           0),
    ]
    band_colors = ["#1D9E75","#5DCAA5","#EF9F27","#D85A30","#E24B4A"]
    rows = ""
    for i, (rng, lbl, threshold) in enumerate(bands):
        is_active = (i == len(bands)-1 and active_score <= 24) or \
                    (i < len(bands)-1 and active_score >= threshold and active_score < bands[i-1][2] if i > 0 else active_score >= threshold)
        # simpler: highlight the band the score falls in
        active = ""
        if   active_score >= 85 and i == 0: active = "rubric-active"
        elif 65 <= active_score < 85 and i == 1: active = "rubric-active"
        elif 45 <= active_score < 65 and i == 2: active = "rubric-active"
        elif 25 <= active_score < 45 and i == 3: active = "rubric-active"
        elif active_score < 25 and i == 4: active = "rubric-active"
        rows += f"""<div class='rubric-row {active}'>
          <span class='rubric-range' style='color:{band_colors[i]}'>{rng}</span>
          <span class='rubric-label'>{lbl}</span>
        </div>"""
    return f"<div class='score-rubric'>{rows}</div>"

# ── Analysis ─────────────────────────────────────────────────────────────────
if run_btn and user_input.strip():
    from agents.claim_extractor import extract_claims
    from agents.searcher import search_claim
    from agents.fact_analyser import analyse_claim
    from agents.graph_builder import build_claim_graph_html

    all_results = []
    verdicts    = []
    scores      = []

    with st.spinner("Extracting verifiable claims..."):
        try:
            claims = extract_claims(user_input)
        except Exception as e:
            st.error(f"Could not extract claims: {e}")
            st.stop()

    st.markdown(f"""
    <div style='font-family:DM Mono,monospace;font-size:0.72rem;color:#5f5e5a;
    letter-spacing:0.1em;text-transform:uppercase;margin-bottom:1.2rem'>
    Found {len(claims)} verifiable claim(s) — analysing each below
    </div>""", unsafe_allow_html=True)

    for idx, claim in enumerate(claims):
        st.markdown(f"""
        <div class='claim-card'>
          <div class='claim-number'>Claim {idx+1} of {len(claims)}</div>
          <div class='claim-text'>{claim}</div>
        </div>""", unsafe_allow_html=True)

        with st.spinner(f"Searching live sources for claim {idx+1}..."):
            sources = search_claim(claim)
            time.sleep(0.2)

        with st.spinner("Analysing credibility with strict rubric..."):
            analysis = analyse_claim(claim, sources)

        verdict     = analysis.get("verdict", "UNVERIFIED")
        score       = analysis.get("score", 50)
        reasoning   = analysis.get("reasoning", "")
        key_finding = analysis.get("key_finding", "")
        bias_flags  = analysis.get("bias_flags", [])
        supporting  = analysis.get("supporting_sources", [])
        contradicting = analysis.get("contradicting_sources", [])

        verdicts.append(verdict)
        scores.append(score)

        col_left, col_right = st.columns([1, 1])

        with col_left:
            sc_class  = score_color_class(score)
            bias_html = "".join([f"<span class='bias-flag'>{b}</span>" for b in bias_flags]) \
                        if bias_flags else "<span style='font-size:0.78rem;color:#2a2a35'>None detected</span>"

            st.markdown(f"<span class='verdict-badge verdict-{verdict}'>{verdict}</span>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class='score-container'>
              <div class='score-label'>
                <span>Credibility score</span>
                <span style='color:#d4d0c8;font-weight:500'>{score}/100</span>
              </div>
              <div class='score-track'>
                <div class='{sc_class}' style='width:{score}%'></div>
              </div>
            </div>
            {rubric_html(score)}
            <div class='section-label'>Key finding</div>
            <div class='key-finding'>{key_finding}</div>
            <div class='section-label'>Reasoning</div>
            <div class='reasoning-box'>{reasoning}</div>
            <div class='section-label'>Bias / framing flags</div>
            <div style='margin-bottom:0.5rem'>{bias_html}</div>
            """, unsafe_allow_html=True)

            st.markdown(f"<div class='section-label'>Sources ({len([s for s in sources if s.get('url')])} found)</div>", unsafe_allow_html=True)
            for s in sources:
                if not s.get("url"):
                    continue
                url        = s["url"]
                title      = s.get("title", "Unknown")[:58]
                src_engine = s.get("source", "tavily")
                engine_badge = (
                    "<span style='font-family:DM Mono,monospace;font-size:0.6rem;"
                    "background:#0d1a2b;color:#378ADD;border:1px solid #185FA5;"
                    "border-radius:4px;padding:1px 5px;margin-left:5px'>tavily</span>"
                    if src_engine == "tavily" else
                    "<span style='font-family:DM Mono,monospace;font-size:0.6rem;"
                    "background:#0d1f0d;color:#639922;border:1px solid #3B6D11;"
                    "border-radius:4px;padding:1px 5px;margin-left:5px'>ddg</span>"
                )
                if url in supporting:
                    chip_cls, dot_cls, lbl = "source-support",    "dot-support",    "supports"
                elif url in contradicting:
                    chip_cls, dot_cls, lbl = "source-contradict", "dot-contradict", "contradicts"
                else:
                    chip_cls, dot_cls, lbl = "source-neutral",    "dot-neutral",    "related"

                st.markdown(f"""
                <div class='source-chip {chip_cls}'>
                  <span class='source-dot {dot_cls}'></span>
                  <span>
                    <a href='{url}' target='_blank' style='color:#d4d0c8;text-decoration:none'>{title}</a>
                    {engine_badge}
                    <span style='font-family:DM Mono,monospace;font-size:0.65rem;
                    color:#444441;margin-left:6px'>{lbl}</span>
                  </span>
                </div>""", unsafe_allow_html=True)

        with col_right:
            st.markdown("""
            <div class='section-label'>Claim lineage graph</div>
            <div style='font-family:DM Mono,monospace;font-size:0.65rem;color:#2a2a35;margin-bottom:0.5rem'>
            Green = supports &nbsp;·&nbsp; Red = contradicts &nbsp;·&nbsp; Gray = related &nbsp;·&nbsp; Click node to open source
            </div>""", unsafe_allow_html=True)
            graph_html = build_claim_graph_html(claim, sources, analysis)
            components.html(graph_html, height=420)

        all_results.append({
            "claim": claim, "verdict": verdict, "score": score,
            "reasoning": reasoning, "key_finding": key_finding,
            "bias_flags": bias_flags, "sources": sources
        })
        st.markdown("<hr class='thin-divider'>", unsafe_allow_html=True)

    # ── Summary banner ────────────────────────────────────────────────────────
    avg_score      = round(sum(scores) / len(scores)) if scores else 0
    false_count    = verdicts.count("FALSE")
    mislead_count  = verdicts.count("MISLEADING")
    true_count     = verdicts.count("TRUE")
    unverif_count  = verdicts.count("UNVERIFIED")

    if false_count > 0:
        overall_color, overall_label = "#E24B4A", "HIGH RISK"
    elif mislead_count > 0:
        overall_color, overall_label = "#EF9F27", "MISLEADING"
    elif true_count == len(verdicts):
        overall_color, overall_label = "#1D9E75", "VERIFIED"
    else:
        overall_color, overall_label = "#888780", "UNVERIFIED"

    st.markdown(f"""
    <div style='background:#12121a;border:1px solid #2a2a35;border-radius:16px;
    padding:1.5rem;margin-top:1rem;display:flex;align-items:center;gap:2rem;flex-wrap:wrap'>
      <div>
        <div style='font-family:DM Mono,monospace;font-size:0.65rem;color:#444441;
        letter-spacing:0.15em;text-transform:uppercase;margin-bottom:4px'>Overall assessment</div>
        <div style='font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;color:{overall_color}'>{overall_label}</div>
      </div>
      <div>
        <div style='font-family:DM Mono,monospace;font-size:0.65rem;color:#444441;
        letter-spacing:0.15em;text-transform:uppercase;margin-bottom:4px'>Avg credibility</div>
        <div style='font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;color:#f0ede8'>
          {avg_score}<span style='font-size:0.9rem;color:#444441'>/100</span>
        </div>
      </div>
      <div>
        <div style='font-family:DM Mono,monospace;font-size:0.65rem;color:#444441;
        letter-spacing:0.15em;text-transform:uppercase;margin-bottom:4px'>Claims checked</div>
        <div style='font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;color:#f0ede8'>{len(claims)}</div>
      </div>
      <div style='display:flex;gap:8px;flex-wrap:wrap;margin-left:auto'>
        <span style='background:#0d2b1f;color:#1D9E75;border:1px solid #1D9E75;border-radius:6px;padding:3px 10px;font-family:DM Mono,monospace;font-size:0.72rem'>{true_count} TRUE</span>
        <span style='background:#2b0d0d;color:#E24B4A;border:1px solid #E24B4A;border-radius:6px;padding:3px 10px;font-family:DM Mono,monospace;font-size:0.72rem'>{false_count} FALSE</span>
        <span style='background:#2b1f00;color:#EF9F27;border:1px solid #EF9F27;border-radius:6px;padding:3px 10px;font-family:DM Mono,monospace;font-size:0.72rem'>{mislead_count} MISLEADING</span>
        <span style='background:#1a1a1a;color:#888780;border:1px solid #444441;border-radius:6px;padding:3px 10px;font-family:DM Mono,monospace;font-size:0.72rem'>{unverif_count} UNVERIFIED</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.history.append({
        "input": user_input,
        "num_claims": len(claims),
        "avg_score": avg_score,
        "overall_verdict": overall_label,
        "results": all_results
    })

elif run_btn and not user_input.strip():
    st.warning("Please paste a claim or news snippet to analyse.")
