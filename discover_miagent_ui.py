import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import requests

st.set_page_config(page_title="MarketMirror — Competitive Analysis",
                   layout="wide", page_icon="🪞")

# ---------- styling ----------
st.markdown("""
<style>
.block-container { padding-top: 1.5rem; max-width: 1180px; }
h1, h2, h3 { font-family: 'Inter', -apple-system, sans-serif; letter-spacing: -.02em; }

/* hero */
.hero {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 55%, #9333ea 100%);
    border-radius: 22px; padding: 38px 40px; color: #fff; margin-bottom: 8px;
    box-shadow: 0 12px 40px rgba(79,70,229,.28);
}
.hero-brand { display:flex; align-items:center; gap:12px; margin-bottom:14px; }
.hero-logo {
    width:42px; height:42px; border-radius:11px; background:rgba(255,255,255,.18);
    display:flex; align-items:center; justify-content:center; font-size:1.3rem;
}
.hero-name { font-size:1.35rem; font-weight:800; letter-spacing:-.02em; }
.hero h1 { color:#fff; font-size:2.5rem; font-weight:800; margin:0 0 10px; line-height:1.1; }
.hero p { color:rgba(255,255,255,.9); font-size:1.08rem; margin:0; max-width:640px; line-height:1.5; }
.hero-pill {
    display:inline-flex; align-items:center; gap:8px; margin-top:18px;
    background:rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.28);
    padding:8px 16px; border-radius:999px; font-size:.86rem; font-weight:600;
    white-space:normal; line-height:1.3; color:#fff; text-decoration:none;
    cursor:pointer; transition:background .2s, box-shadow .2s;
}
.hero-pill:hover {
    background:rgba(255,255,255,.28); box-shadow:0 4px 16px rgba(0,0,0,.15);
    color:#fff; text-decoration:none;
}
/* cards */
.comp-card {
    background:#fff; border:1px solid #ebebf2; border-radius:16px;
    padding:20px 22px; margin-bottom:16px;
    box-shadow:0 1px 2px rgba(16,24,40,.05); transition:box-shadow .2s;
}
.comp-card:hover { box-shadow:0 4px 16px rgba(16,24,40,.10); }
.comp-head { display:flex; align-items:center; gap:14px; margin-bottom:12px; }
.comp-avatar {
    width:48px; height:48px; border-radius:12px; flex-shrink:0;
    display:flex; align-items:center; justify-content:center;
    font-weight:700; font-size:1.1rem; color:#fff;
    background:linear-gradient(135deg,#6366f1 0%,#8b5cf6 100%);
}
.comp-name { font-size:1.18rem; font-weight:700; margin:0; color:#101828; }
.badge { display:inline-block; padding:3px 11px; border-radius:999px; font-size:.72rem; font-weight:600; }
.badge-High { background:#fee4e2; color:#b42318; }
.badge-Medium { background:#fef0c7; color:#b54708; }
.badge-Low { background:#dcfae6; color:#027a48; }
.field-label { font-size:.68rem; text-transform:uppercase; letter-spacing:.05em;
               color:#98a2b3; font-weight:700; margin-top:12px; margin-bottom:2px; }
.field-val { color:#475467; line-height:1.5; }
.gap-card { background:#fbfbfe; border:1px solid #eef0f5; border-left:4px solid #6366f1;
            border-radius:10px; padding:16px 18px; margin-bottom:12px; }
.gap-title { font-size:1rem; font-weight:600; color:#101828; }
.summary-box { background:linear-gradient(135deg,#f5f3ff 0%,#eef2ff 100%);
               border:1px solid #e0e7ff; border-radius:14px; padding:18px 22px;
               font-size:1.02rem; line-height:1.6; color:#3730a3; }
.section-eyebrow { font-size:.72rem; text-transform:uppercase; letter-spacing:.08em;
                   color:#7c3aed; font-weight:700; margin-bottom:2px; }
.stRadio div[role="radiogroup"] {
    align-items: center !important;
}
.stRadio,
.stRadio *,
div[role="radiogroup"],
div[role="radiogroup"] * {
    overflow: visible !important;
    height: auto !important;
    max-height: none !important;
    min-height: 0 !important;
    line-height: 1.6 !important;
    transform: none !important;
    clip-path: none !important;
}
.stRadio div[role="radiogroup"] {
    align-items: center !important;
    padding: 4px 0 !important;
}
</style>
""", unsafe_allow_html=True)

FEATURES = ["Pricing", "Product Breadth", "Recent Innovation",
            "Digital/Ecommerce", "Market Positioning", "Support"]
N8N_WEBHOOK = "https://nramya9.app.n8n.cloud/webhook/discover-miagent"  # production URL

# ---------- helpers ----------
def initials(name):
    parts = [p for p in name.split() if p]
    return (parts[0][0] + (parts[1][0] if len(parts) > 1 else "")).upper() if parts else "?"

def badge(level):
    lvl = level if level in ("High", "Medium", "Low") else "Low"
    return f'<span class="badge badge-{lvl}">{level or "—"}</span>'

def run_analysis(company, industry_hint, focus_area):
    payload = {"company": company, "industry_hint": industry_hint, "focus_area": focus_area}
    r = requests.post(N8N_WEBHOOK, json=payload, timeout=300)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, list): data = data[0]
    if "json" in data: data = data["json"]
    return data

# sample data for the landing graph (shown until a real run exists)
SAMPLE_SCORES = {
    "Competitor A": {"Pricing": 4, "Product Breadth": 5, "Recent Innovation": 4,
                     "Digital/Ecommerce": 3, "Market Positioning": 5, "Support": 4},
    "Competitor B": {"Pricing": 3, "Product Breadth": 4, "Recent Innovation": 5,
                     "Digital/Ecommerce": 4, "Market Positioning": 4, "Support": 3},
    "Competitor C": {"Pricing": 5, "Product Breadth": 3, "Recent Innovation": 3,
                     "Digital/Ecommerce": 2, "Market Positioning": 3, "Support": 4},
    "Competitor D": {"Pricing": 2, "Product Breadth": 4, "Recent Innovation": 4,
                     "Digital/Ecommerce": 5, "Market Positioning": 4, "Support": 5},
}

def scores_to_df(score_map):
    df = pd.DataFrame(score_map).T.reindex(columns=FEATURES).fillna(3).clip(1, 5)
    return df

def radar_chart(df, title):
    fig = go.Figure()
    palette = ["#6366f1", "#8b5cf6", "#ec4899", "#0ea5e9", "#10b981", "#f59e0b"]
    cats = FEATURES + [FEATURES[0]]  # close the loop
    for i, (name, row) in enumerate(df.iterrows()):
        vals = list(row.values) + [row.values[0]]
        c = palette[i % len(palette)]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=cats, fill="toself", name=name,
            line=dict(color=c, width=2), opacity=.75,
            fillcolor=c.replace(")", ",0.08)").replace("rgb", "rgba") if c.startswith("rgb") else c,
        ))
    fig.update_traces(fillcolor="rgba(99,102,241,0.06)", selector=dict(type="scatterpolar"))
    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=15)),
        polar=dict(radialaxis=dict(visible=True, range=[0, 5], tickvals=[1,2,3,4,5],
                                   gridcolor="#ececf5"),
                   angularaxis=dict(gridcolor="#ececf5")),
        showlegend=True, height=440, margin=dict(t=60, b=30, l=40, r=40),
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5),
    )
    return fig

def heatmap_chart(df):
    fig = go.Figure(data=go.Heatmap(
        z=df.values, x=df.columns.tolist(), y=df.index.tolist(),
        zmin=1, zmax=5, colorscale="RdYlGn",
        text=df.values, texttemplate="%{text}", textfont={"size": 14},
        colorbar=dict(title="Score", tickvals=[1, 2, 3, 4, 5]),
        hovertemplate="%{y} — %{x}: %{z}<extra></extra>",
    ))
    fig.update_layout(height=70 * len(df) + 200, xaxis=dict(side="top", tickangle=-25),
                      yaxis=dict(autorange="reversed"), margin=dict(l=120, t=110),
                      paper_bgcolor="rgba(0,0,0,0)")
    return fig

# ---------- state ----------
if "briefing" not in st.session_state:
    st.session_state.briefing = None
if "view_radio" not in st.session_state:
    st.session_state.view_radio = "🏠  Home"

# apply pending view switch BEFORE the radio widget is created
if st.session_state.pop("_go_results", False):
    st.session_state.view_radio = "📊  Results"
if st.session_state.pop("_go_home", False):
    st.session_state.view_radio = "🏠  Home"

# ---------- nav ----------
options = ["🏠  Home", "📊  Results"]
view = st.radio("view", options, horizontal=True,
                label_visibility="collapsed", key="view_radio")
is_results = view.startswith("📊")

# ================= HOME =================
if not is_results:
    # hero banner
    st.markdown("""
    <div class="hero">
      <div class="hero-brand">
        <div class="hero-logo">🪞</div>
        <div class="hero-name">MarketMirror</div>
      </div>
      <h1>See your competition clearly.</h1>
      <p>Enter a company and MarketMirror discovers its closest rivals, researches each,
         and hands you a prescriptive briefing — strengths, gaps, and a feature scorecard.</p>
      <a id="hero-cta" href="#analysis-form"
         style="display:inline-flex;align-items:center;gap:8px;margin-top:18px;
                background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.35);
                padding:10px 20px;border-radius:999px;font-size:.9rem;font-weight:700;
                color:#fff;text-decoration:none;cursor:pointer;">
        ✨ Try free basic analysis — results in less than 5 minutes →
      </a>
    </div>
    """, unsafe_allow_html=True)

    # wire up smooth scroll for the CTA — runs in iframe with parent window access
    components.html("""
    <script>
    (function() {
      function wire() {
        var link = window.parent.document.getElementById('hero-cta');
        if (!link) { setTimeout(wire, 150); return; }
        link.addEventListener('click', function(e) {
          e.preventDefault();
          var target = window.parent.document.getElementById('analysis-form');
          if (target) target.scrollIntoView({behavior: 'smooth', block: 'start'});
        });
      }
      wire();
    })();
    </script>
    """, height=0)

    st.write("")

    # landscape graph — sample until a real run exists, then real data
    b = st.session_state.briefing
    has_real = bool(b and b.get("feature_scores"))
    if has_real:
        st.markdown('<div class="section-eyebrow">Your latest analysis</div>', unsafe_allow_html=True)
        st.subheader(f"Competitive landscape · {b.get('target_company','')}")
        df = scores_to_df({x["competitor"]: x["scores"] for x in b["feature_scores"]})
        st.plotly_chart(radar_chart(df, "Feature strength across competitors"),
                        use_container_width=True)
    else:
        st.markdown('<div class="section-eyebrow">Sample preview</div>', unsafe_allow_html=True)
        st.subheader("What you'll get")
        df = scores_to_df(SAMPLE_SCORES)
        st.plotly_chart(radar_chart(df, "Feature strength across competitors (sample)"),
                        use_container_width=True)
        st.caption("This is sample data. Run an analysis below to see your own landscape.")

    st.divider()

    # input form
    st.markdown('<div id="analysis-form"></div>', unsafe_allow_html=True)
    st.subheader("Run a free analysis")
    st.caption("Enter a target company. Industry hint and focus area are optional.")
    c1, c2 = st.columns(2)
    with c1:
        company = st.text_input("Target company  *", placeholder="e.g. Agilent")
        industry_hint = st.text_input("Industry hint  (optional)",
                                      placeholder="disambiguates the company — e.g. life sciences")
    with c2:
        focus_area = st.selectbox("Focus area  (optional)",
                                  ["", "pricing", "features", "ecommerce", "positioning"])
        st.write(""); st.write("")
        run = st.button("Analyze competitors  ▶", type="primary", use_container_width=True)

    if run:
        if not company.strip():
            st.error("Enter a target company to analyze.")
        else:
            loader = st.empty()
            loader.markdown(f"""
            <div style="text-align:center;padding:48px 24px;
                        background:linear-gradient(135deg,#f5f3ff 0%,#eef2ff 100%);
                        border-radius:20px;margin:12px 0;border:1px solid #e0e7ff;">
              <div style="font-size:3.8rem;display:inline-block;animation:run 0.55s ease-in-out infinite alternate;">🕵️</div>
              <h3 style="color:#4f46e5;font-family:Inter,sans-serif;margin:16px 0 4px;">
                On the case for <em>{company}</em>…
              </h3>
              <div style="position:relative;height:26px;margin:14px auto;max-width:440px;">
                <p class="fmsg" style="animation-delay:0s">🔍 Stalking competitors' websites…</p>
                <p class="fmsg" style="animation-delay:3s">🤫 Bribing the AI for insider info…</p>
                <p class="fmsg" style="animation-delay:6s">📊 Crunching numbers furiously…</p>
                <p class="fmsg" style="animation-delay:9s">🧠 Reading their minds (legally)…</p>
                <p class="fmsg" style="animation-delay:12s">☕ Making coffee while Tavily searches…</p>
                <p class="fmsg" style="animation-delay:15s">✍️ Writing your prescriptive briefing…</p>
              </div>
              <div style="margin-top:22px;">
                <span class="fdot" style="animation-delay:0s">●</span>
                <span class="fdot" style="animation-delay:0.25s">●</span>
                <span class="fdot" style="animation-delay:0.5s">●</span>
              </div>
            </div>
            <style>
            @keyframes run {{
              from {{ transform: translateY(0) rotate(-5deg); }}
              to   {{ transform: translateY(-18px) rotate(5deg); }}
            }}
            @keyframes msgcycle {{
              0%   {{ opacity:0; transform:translateY(6px); }}
              4%   {{ opacity:1; transform:translateY(0); }}
              16%  {{ opacity:1; transform:translateY(0); }}
              20%  {{ opacity:0; transform:translateY(-6px); }}
              100% {{ opacity:0; }}
            }}
            @keyframes dotpop {{
              0%,100% {{ opacity:.25; transform:translateY(0); }}
              50%      {{ opacity:1;   transform:translateY(-7px); }}
            }}
            .fmsg {{
              position:absolute; left:0; right:0; margin:0;
              font-size:.95rem; color:#6366f1; font-weight:600;
              opacity:0; animation:msgcycle 18s infinite;
              font-family:Inter,-apple-system,sans-serif;
            }}
            .fdot {{
              color:#a5b4fc; font-size:.55rem; margin:0 5px;
              display:inline-block; animation:dotpop 1.1s ease-in-out infinite;
            }}
            </style>
            """, unsafe_allow_html=True)
            try:
                result = run_analysis(company, industry_hint, focus_area)
                loader.empty()
                if result.get("status") == "not_found":
                    st.warning(result.get("message", "We couldn't identify that company. Check the spelling or add an industry hint."))
                else:
                    st.session_state.briefing = result
                    st.session_state["_go_results"] = True
                    st.rerun()
            except Exception as e:
                loader.empty()
                st.error(f"Couldn't complete the analysis: {e}")

# ================= RESULTS =================
if is_results:
    b = st.session_state.briefing
    if not b:
        st.info("No results yet. Run an analysis from the **Home** tab.")
        st.stop()

    st.title(b.get("target_company", "Briefing"))
    meta = "  ·  ".join(filter(None, [
        b.get("inferred_industry"),
        f"Focus: {b['focus_area']}" if b.get("focus_area") else None,
        b.get("generated_at", "")[:10]
    ]))
    st.caption(meta)
    if b.get("parse_error"):
        st.warning(f"Parse note: {b['parse_error']}")

    # --- fallback: company not recognised ---
    if not b.get("target_company") or not b.get("competitors"):
        st.markdown("""
        <div style="text-align:center;padding:48px 24px;background:#fff8f0;
                    border:1px solid #fcd9b0;border-radius:16px;margin:16px 0;">
          <div style="font-size:3rem;">🤷</div>
          <h3 style="color:#b45309;font-family:Inter,sans-serif;margin:12px 0 6px;">
            We couldn't find this company
          </h3>
          <p style="color:#92400e;max-width:480px;margin:0 auto;line-height:1.6;">
            The agent couldn't confidently identify <strong>{company}</strong> or find direct competitors.
            This usually means the name is ambiguous or very niche.
          </p>
          <p style="color:#92400e;margin:16px auto 0;max-width:480px;font-weight:600;">
            💡 Try again with an <em>industry hint</em> — e.g. "life sciences" or "SaaS analytics"
          </p>
        </div>
        """.format(company=b.get("target_company", "this company")), unsafe_allow_html=True)
        if st.button("← Try again"):
            st.session_state["_go_home"] = True
            st.rerun()
        st.stop()

    st.markdown(f'<div class="summary-box">{b.get("summary","—")}</div>', unsafe_allow_html=True)
    st.write(""); st.divider()

    # heatmap first
    st.subheader("Feature Heatmap")
    fs = b.get("feature_scores", [])
    if fs:
        df = scores_to_df({x["competitor"]: x["scores"] for x in fs})
        st.plotly_chart(heatmap_chart(df), use_container_width=True)
    else:
        st.info("No feature scores in this briefing — re-run synthesis with the updated prompt.")
    st.divider()

    # competitor cards
    st.subheader("Competitors")
    competitors = b.get("competitors", [])
    strengths_map = {s["competitor"]: s.get("strengths", []) for s in b.get("competitor_strengths", [])}
    cols = st.columns(2)
    for i, comp in enumerate(competitors):
        name = comp.get("name", "Unnamed")
        with cols[i % 2]:
            st.markdown(f"""
            <div class="comp-card">
              <div class="comp-head">
                <div class="comp-avatar">{initials(name)}</div>
                <div><p class="comp-name">{name}</p>{badge(comp.get('threat_level'))}</div>
              </div>
              <div class="field-val">{comp.get('positioning','')}</div>
              <div class="field-label">Pricing</div>
              <div class="field-val">{comp.get('pricing','Not publicly available')}</div>
              <div class="field-label">Digital / Ecommerce</div>
              <div class="field-val">{comp.get('digital_presence','Not assessed')}</div>
            </div>
            """, unsafe_allow_html=True)
            s = strengths_map.get(name, [])
            if s:
                with st.expander(f"Strengths · {name}"):
                    for x in s: st.markdown(f"- {x}")
            if comp.get("key_features") or comp.get("recent_news"):
                with st.expander("Features & recent news"):
                    if comp.get("key_features"):
                        st.markdown("**Key features**")
                        for f in comp["key_features"]: st.markdown(f"- {f}")
                    if comp.get("recent_news"):
                        st.markdown("**Recent news**")
                        for n in comp["recent_news"]: st.markdown(f"- {n}")
            if comp.get("sources"):
                with st.expander("Sources"):
                    for u in comp["sources"]: st.markdown(f"- {u}")
    st.divider()

    # gaps
    st.subheader("Gaps & Recommendations")
    for g in b.get("gaps_and_recommendations", []):
        st.markdown(f"""
        <div class="gap-card">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;">
            <span class="gap-title">{g.get('gap','')}</span> {badge(g.get('priority'))}
          </div>
          <div class="field-label">Evidence</div><div class="field-val">{g.get('evidence','')}</div>
          <div class="field-label">Recommendation</div><div class="field-val">{g.get('recommendation','')}</div>
          <div style="font-size:.78rem;color:#98a2b3;margin-top:8px;">Driven by: {g.get('competitor_driving_it','—')}</div>
        </div>
        """, unsafe_allow_html=True)

    # digital gaps
    st.subheader("Digital / Ecommerce Gaps")
    for d in b.get("digital_gaps", []):
        st.markdown(f"""
        <div class="gap-card" style="border-left-color:#0ea5e9;">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;">
            <span class="gap-title">{d.get('observation','')}</span> {badge(d.get('priority'))}
          </div>
          <div class="field-label">Evidence</div><div class="field-val">{d.get('evidence','')}</div>
          <div class="field-label">Recommendation</div><div class="field-val">{d.get('recommendation','')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write(""); st.divider()
    if st.button("← New analysis"):
        st.session_state["_go_home"] = True
        st.rerun()
