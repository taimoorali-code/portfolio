#!/usr/bin/env python3
"""Static site generator for Taimoor Ali — Shopify Operations & Automation.
Emits plain HTML/CSS/JS. No runtime framework. Run: python3 build.py"""
import os, json, html

SITE = "https://taimoorproject.site"
ROOT = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# Shared chrome
# ----------------------------------------------------------------------------
SERVICES = [
    ("/services/operations-audit/", "Operations Audit", "Start here — map the leaks"),
    ("/services/inventory-sync/", "Inventory & Data Sync", "One source of truth"),
    ("/services/erp-integrations/", "ERP & Integrations", "End manual data entry"),
    ("/services/subscription-automation/", "Subscription Operations", "Tame subscription chaos"),
    ("/services/order-fulfillment-automation/", "Order & Fulfillment", "Checkout to doorstep"),
    ("/services/shopify-apps/", "Custom Apps & API", "When no app fits"),
    ("/services/operations-partner/", "Operations Partner", "Ongoing, on retainer"),
]

def _crumb_name(segment):
    names = {
        "services": "Services",
        "results": "Results",
        "about": "About",
        "book": "Book a Call",
        "operations-audit": "Operations Audit",
        "inventory-sync": "Inventory Sync",
        "erp-integrations": "ERP Integrations",
        "subscription-automation": "Subscription Automation",
        "order-fulfillment-automation": "Order & Fulfillment Automation",
        "shopify-apps": "Custom Shopify Apps",
        "operations-partner": "Operations Partner",
        "whispersheet": "WhisperSheet",
        "ink": "INK",
        "neesh": "Neesh",
    }
    return names.get(segment, segment.replace("-", " ").title())


def breadcrumb_schema(canonical):
    if canonical == "/":
        return None
    parts = [p for p in canonical.strip("/").split("/") if p]
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
    path = ""
    for i, part in enumerate(parts, start=2):
        path += "/" + part
        items.append({"@type": "ListItem", "position": i, "name": _crumb_name(part), "item": SITE + path + "/"})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def head(title, desc, canonical, schema=None, og_type="website"):
    schemas = []
    if schema:
        schemas.extend(schema if isinstance(schema, list) else [schema])
    bc = breadcrumb_schema(canonical)
    if bc:
        schemas.append(bc)
    s = ""
    if schemas:
        s = '\n  <script type="application/ld+json">%s</script>' % json.dumps(schemas if len(schemas) > 1 else schemas[0])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <link rel="canonical" href="{SITE}{canonical}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:url" content="{SITE}{canonical}">
  <meta property="og:site_name" content="Taimoor Ali">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#f7f7f7">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/styles.css">{s}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

def header():
    drop = ""
    drop += '<div class="drop-group-label">Start here</div>'
    drop += f'<a href="{SERVICES[0][0]}">{SERVICES[0][1]}<span>{SERVICES[0][2]}</span></a>'
    drop += '<div class="drop-group-label">Builds</div>'
    for href, name, sub in SERVICES[1:6]:
        drop += f'<a href="{href}">{name}<span>{sub}</span></a>'
    drop += '<div class="drop-group-label">Ongoing</div>'
    drop += f'<a href="{SERVICES[6][0]}">{SERVICES[6][1]}<span>{SERVICES[6][2]}</span></a>'

    mobile = '<a href="/services/" >Services overview</a><div class="mlabel">Services</div>'
    for href, name, sub in SERVICES:
        mobile += f'<a href="{href}">{name}</a>'
    mobile += '<div class="mlabel">More</div><a href="/results/">Results</a><a href="/about/">About</a>'
    mobile += '<a class="btn btn--primary" href="/book/">Book a Call</a>'

    return f"""<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="/"><span class="dot"></span>Taimoor Ali</a>
    <nav class="nav-links" aria-label="Primary">
      <div class="has-drop">
        <button class="drop-toggle" aria-haspopup="true">Services
          <svg class="chev" viewBox="0 0 12 8" fill="none"><path d="M1 1l5 5 5-5" stroke="currentColor" stroke-width="1.5"/></svg>
        </button>
        <div class="drop">{drop}</div>
      </div>
      <a href="/results/">Results</a>
      <a href="/about/">About</a>
    </nav>
    <div class="nav-cta">
      <a class="btn btn--primary" href="/book/">Book a Call</a>
      <button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <div class="mobile-menu">{mobile}</div>
</header>
"""

def cta_band(h2="Ready to stop running your operations by hand?",
             lead="Book a call. In one conversation we'll find where your back office is leaking time and money — and exactly what it takes to fix it.",
             micro="30 minutes. No pitch, no hard sell. You'll leave with clarity either way."):
    return f"""<section class="section section--dark">
  <div class="wrap cta-band reveal">
    <p class="eyebrow">Let's talk</p>
    <h2 class="h2">{h2}</h2>
    <p class="lead">{lead}</p>
    <a class="btn btn--ondark btn--lg" href="/book/">Book a Call <span class="arw">→</span></a>
    <p class="cta-micro">{micro}</p>
  </div>
</section>
"""

def footer():
    flinks = "".join(f'<a href="{h}">{n}</a>' for h, n, _ in SERVICES)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="brand" href="/"><span class="dot"></span>Taimoor Ali</a>
        <p>Shopify integration &amp; ecommerce automation specialist. I replace operational chaos with systems that run themselves.</p>
      </div>
      <div class="foot-col">
        <h5>Services</h5>
        {flinks}
      </div>
      <div class="foot-col">
        <h5>Company</h5>
        <a href="/results/">Results</a>
        <a href="/about/">About</a>
        <a href="/book/">Book a Call</a>
        <a href="https://www.linkedin.com/in/taimoor-ali-8694a52ba/" rel="noopener">LinkedIn</a>
        <a href="https://github.com/taimoorali-code" rel="noopener">GitHub</a>
        <a href="https://www.upwork.com/freelancers/~019281523908b93a20" rel="noopener">Upwork (5.0)</a>
      </div>
    </div>
    <div class="foot-base">
      <span>Working remotely with brands across the US, UK, Canada &amp; Australia.</span>
      <span>© <span data-year></span> Taimoor Ali</span>
    </div>
  </div>
</footer>
<script src="/assets/main.js" defer></script>
</body>
</html>"""

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)

# ----------------------------------------------------------------------------
# Homepage
# ----------------------------------------------------------------------------
def hero_svg():
    return """<svg class="hero-visual reveal" viewBox="0 0 460 360" role="img" aria-label="Diagram: Shopify, ERP, 3PL and Google Sheets connected to one source of truth">
  <line class="sys-link" x1="120" y1="64" x2="230" y2="180"/>
  <line class="sys-link" x1="340" y1="64" x2="230" y2="180"/>
  <line class="sys-link" x1="120" y1="296" x2="230" y2="180"/>
  <line class="sys-link" x1="340" y1="296" x2="230" y2="180"/>
  <g>
    <rect class="sys-node" x="48" y="40" width="144" height="48" rx="8"/>
    <text class="sys-label" x="120" y="69" text-anchor="middle">Shopify</text>
    <rect class="sys-node" x="268" y="40" width="144" height="48" rx="8"/>
    <text class="sys-label" x="340" y="69" text-anchor="middle">ERP</text>
    <rect class="sys-node" x="48" y="272" width="144" height="48" rx="8"/>
    <text class="sys-label" x="120" y="301" text-anchor="middle">3PL / Warehouse</text>
    <rect class="sys-node" x="268" y="272" width="144" height="48" rx="8"/>
    <text class="sys-label" x="340" y="301" text-anchor="middle">Google Sheets</text>
  </g>
  <g>
    <rect class="sys-core" x="156" y="152" width="148" height="56" rx="10"/>
    <text class="sys-core-label" x="230" y="177" text-anchor="middle">ONE SOURCE</text>
    <text class="sys-core-label" x="230" y="193" text-anchor="middle">OF TRUTH</text>
  </g>
</svg>"""

def homepage():
    schema = {
        "@context": "https://schema.org", "@type": "ProfessionalService",
        "name": "Taimoor Ali — Shopify Integration & Automation",
        "description": "Shopify integration, ecommerce automation and operations consulting for growing Shopify, Plus, DTC and subscription brands.",
        "url": SITE + "/", "areaServed": ["US", "GB", "CA", "AU"],
        "founder": {"@type": "Person", "name": "Taimoor Ali",
                    "jobTitle": "Shopify Integration & Ecommerce Automation Specialist",
                    "sameAs": ["https://www.linkedin.com/in/taimoor-ali-8694a52ba/",
                               "https://github.com/taimoorali-code",
                               "https://www.upwork.com/freelancers/~019281523908b93a20"]}
    }
    h = head("Shopify Integration & Automation Specialist | Taimoor Ali",
             "I help growing Shopify and DTC brands replace operational chaos with systems that run themselves — inventory sync, ERP, subscriptions, and order automation. Book a call.",
             "/", schema)
    h += header()
    h += '<main id="main">'

    # hero
    h += f"""<section class="hero">
  <div class="wrap hero-grid">
    <div class="reveal">
      <div class="hero-byline"><img class="hero-avatar" src="/assets/images/avatar.png" alt="Taimoor Ali" width="42" height="42"><span>Taimoor Ali</span></div>
      <p class="eyebrow">Shopify operations · Integrations · Automation</p>
      <h1 class="h1">Growing brands don't break on marketing. They break on operations.</h1>
      <p class="lead">I'm Taimoor Ali — a Shopify integration and ecommerce automation specialist. I design and build the systems that connect Shopify, ERP, 3PL, subscriptions, and your back office into one operation that runs without manual work — so your team scales output, not headcount.</p>
      <div class="hero-cta">
        <a class="btn btn--primary btn--lg" href="/book/">Book a Call <span class="arw">→</span></a>
        <a class="btn btn--ghost btn--lg" href="#results">See the results ↓</a>
      </div>
      <p class="hero-trustline">Trusted by DTC, subscription &amp; B2B brands · <b>Limited engagements each quarter</b></p>
    </div>
    {hero_svg()}
  </div>
</section>"""

    # trust bar
    h += """<section class="trustbar"><div class="wrap section--tight" style="padding-bottom:1.7rem">
    <div class="trust-brands reveal">
      <span class="tlabel">Selected work delivered for</span>
      <span class="bname">Elie Saab</span><span class="bname">Neesh</span><span class="bname">ZERO</span>
      <span class="bname">Hayalma</span><span class="bname">INK</span><span class="bname">WhisperSheet</span>
    </div>
    <div class="stats reveal">
      <div class="stat"><div class="num"><span data-count="80" data-suffix="%">80%</span></div><div class="lbl">less manual inventory work</div></div>
      <div class="stat"><div class="num"><span data-count="90" data-suffix="%">90%</span></div><div class="lbl">fewer fulfillment disputes</div></div>
      <div class="stat"><div class="num"><span data-count="20" data-prefix="" data-suffix="+">20+</span></div><div class="lbl">hrs / week returned to teams</div></div>
      <div class="stat"><div class="num"><span data-count="5.0">5.0</span></div><div class="lbl">rating on Upwork</div></div>
    </div>
  </div></section>"""

    # problem
    h += """<section class="section section--paper2"><div class="wrap measure reveal">
    <p class="eyebrow">The problem</p>
    <h2 class="h2" style="margin-top:.7rem">If this is your operation, we should talk.</h2>
    <ul class="symptom-list">
      <li>Your inventory is never quite right across channels.</li>
      <li>Orders get copied by hand between Shopify and your ERP or 3PL.</li>
      <li>Your subscription setup is held together with workarounds nobody wants to touch.</li>
      <li>Someone on your team is in a spreadsheet at midnight, again.</li>
      <li>No two systems ever seem to agree on the same number.</li>
    </ul>
    <p class="lead">Every one of these is a tax on your margin and a ceiling on your growth. You don't have a marketing problem. You have an operations problem — and unlike most of what slows a brand down, <span class="emph">this one is completely solvable.</span></p>
  </div></section>"""

    # shift
    h += """<section class="section"><div class="wrap measure reveal">
    <p class="eyebrow">The shift</p>
    <h2 class="h2" style="margin-top:.7rem">I build the systems that make the manual work disappear.</h2>
    <p class="lead" style="margin-top:1.1rem">Most brands try to fix operational chaos by hiring more people or bolting on another app. Both make it worse — more humans and more tools mean more glue to maintain. The durable fix is architecture: systems engineered to talk to each other so data flows on its own.</p>
    <p style="margin-top:1rem;color:var(--ink-soft)">I do both halves of that. I diagnose what's actually broken in your operation, then I engineer the integrations and automations that fix it. No strategy deck handed off to someone else to build. No developer building exactly what you spec'd without telling you the spec was the problem. <span class="emph">One person who owns the outcome from diagnosis to deployment.</span></p>
  </div></section>"""

    # services ladder
    h += """<section class="section section--surface" id="services"><div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">How I help</p><h2 class="h2">Three ways to work with me.</h2></div>
    <div class="ladder">
      <div class="lad-card feature reveal">
        <span class="lad-num">01 / Start here</span>
        <h3>Operations Audit &amp; Automation Roadmap</h3>
        <p>I map your systems end to end, find every place a human is doing what software should, and hand you a prioritized roadmap with effort, impact, and ROI.</p>
        <p class="lad-meta">Fixed fee · 1–2 weeks</p>
        <a class="textlink" href="/services/operations-audit/">View the audit <span class="arw">→</span></a>
      </div>
      <div class="lad-card reveal">
        <span class="lad-num">02 / Builds</span>
        <h3>Integration &amp; Automation Builds</h3>
        <p>Fixed-scope systems that end the manual work: inventory &amp; data sync, ERP integration, subscription operations, order &amp; fulfillment automation, and custom apps.</p>
        <p class="lad-meta">Priced on the value of the problem — not the hours</p>
        <a class="textlink" href="/services/">View build services <span class="arw">→</span></a>
      </div>
      <div class="lad-card reveal">
        <span class="lad-num">03 / Ongoing</span>
        <h3>Operations Partner (Retainer)</h3>
        <p>Your fractional ecommerce automation engineer: ongoing automation, monitoring, integration upkeep, and architecture on call as you scale.</p>
        <p class="lad-meta">Tiered monthly retainer</p>
        <a class="textlink" href="/services/operations-partner/">Explore retainers <span class="arw">→</span></a>
      </div>
    </div>
  </div></section>"""

    # results
    h += """<section class="section" id="results"><div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Selected results</p><h2 class="h2">Results, not screenshots.</h2><p class="lead">Every build started with a real business problem. Here's what changed — outcome first, stack second.</p></div>
    <div class="results-grid">
      <a class="res-card reveal" href="/results/whispersheet/">
        <span class="res-brand">WhisperSheet</span>
        <h3>Cut manual inventory work 80% for multi-store brands.</h3>
        <p>A Shopify inventory sync system that keeps stores, Google Sheets, and channels in perfect lockstep.</p>
        <div class="res-tags"><span>Inventory Sync</span><span>Google Sheets API</span><span>SaaS</span></div>
        <span class="textlink">Read the case study <span class="arw">→</span></span>
      </a>
      <a class="res-card reveal" href="/results/ink/">
        <span class="res-brand">INK</span>
        <h3>Eliminated fake deliveries, cut fulfillment disputes 90%.</h3>
        <p>A verified-delivery system that keeps inventory airtight from pack to doorstep.</p>
        <div class="res-tags"><span>Fulfillment</span><span>NFC Verification</span><span>Warehouse App</span></div>
        <span class="textlink">Read the case study <span class="arw">→</span></span>
      </a>
      <a class="res-card reveal" href="/results/neesh/">
        <span class="res-brand">Neesh</span>
        <h3>Turned a print magazine into a thriving B2B marketplace.</h3>
        <p>Multi-vendor Shopify architecture connecting publishers, retailers, and inventory under one storefront.</p>
        <div class="res-tags"><span>Multi-vendor</span><span>Shopify API</span><span>Node.js</span></div>
        <span class="textlink">Read the case study <span class="arw">→</span></span>
      </a>
    </div>
    <div class="mt-sm"><a class="textlink" href="/results/">See all results <span class="arw">→</span></a></div>
  </div></section>"""

    # differentiator
    h += """<section class="section section--paper2"><div class="wrap measure reveal">
    <p class="eyebrow">Why me</p>
    <h2 class="h2" style="margin-top:.7rem">Most brands have to choose. With me, you don't.</h2>
    <div class="diff-grid">
      <div class="diff-card muted"><span class="role">A Shopify developer</span><p>Builds what you spec — but won't tell you your architecture is the real problem.</p></div>
      <div class="diff-card muted"><span class="role">An operations consultant</span><p>Hands you a strategy — then hands the build to someone else, and the gap between the two is where projects die.</p></div>
    </div>
    <div class="diff-final"><h3 class="h3">I'm both.</h3><p style="margin-top:.6rem;color:var(--accent-ink)">I diagnose the operational chaos <em>and</em> engineer the system that ends it. One person, one line of accountability, no handoff.</p></div>
  </div></section>"""

    # social proof
    h += """<section class="section"><div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Client words</p><h2 class="h2">The work speaks — so do they.</h2></div>
    <p class="lead reveal" style="margin-top:1.4rem;max-width:42rem">Real client reviews are available on Upwork. I keep this section clean rather than showing unverified claims.</p>
    <div class="mt-sm"><a class="textlink" href="https://www.upwork.com/freelancers/~019281523908b93a20" rel="noopener">See all reviews on Upwork <span class="arw">→</span></a></div>
  </div></section>"""

    # fit
    h += """<section class="section section--surface"><div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Fit</p><h2 class="h2">Who I work best with.</h2></div>
    <div class="fit-grid">
      <div class="fit-card yes reveal"><span class="ftag">A fit if you're</span><p>a growing Shopify or Shopify Plus brand — DTC, subscription, or B2B/multi-vendor — where operations are starting to cap your growth, and you're a founder, COO, or ops lead who wants the manual work gone for good.</p></div>
      <div class="fit-card no reveal"><span class="ftag">Not a fit if you want</span><p>a cheap theme tweak, a logo, a one-off bug fix, or the lowest hourly rate you can find. If you're rate-shopping developers, I'm not your person — and that's by design.</p></div>
    </div>
  </div></section>"""

    # process
    h += """<section class="section"><div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Process</p><h2 class="h2">How engagements work.</h2></div>
    <div class="steps">
      <div class="step reveal"><span class="snum">Step 01</span><h4>Audit</h4><p>We map your operation and find the leaks.</p></div>
      <div class="step reveal"><span class="snum">Step 02</span><h4>Architect</h4><p>I design the system and scope the build.</p></div>
      <div class="step reveal"><span class="snum">Step 03</span><h4>Automate</h4><p>I build, deploy, and hand you operations that run themselves.</p></div>
      <div class="step opt reveal"><span class="snum">Step 04 · optional</span><h4>Partner</h4><p>Ongoing optimization as you grow.</p></div>
    </div>
  </div></section>"""

    h += cta_band()
    h += "</main>"
    h += footer()
    write("index.html", h)

# ----------------------------------------------------------------------------
# Service pages
# ----------------------------------------------------------------------------
def render_service(s):
    bc = f'<div class="breadcrumb"><a href="/">Home</a> / <a href="/services/">Services</a> / {s["crumb"]}</div>'
    symptoms = "".join(f"<li>{x}</li>" for x in s["symptoms"])
    included = "".join(f"<li>{x}</li>" for x in s["included"])
    systems = "".join(f'<div class="sys-item"><span style="color:var(--accent)">▸</span>{x}</div>' for x in s["systems"])
    process = "".join(f"<li>{x}</li>" for x in s["process"])
    faqs = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in s["faqs"])
    related = "".join(f'<a href="{h_}">{n}</a>' for h_, n in s["related"])

    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage",
                  "mainEntity": [{"@type": "Question", "name": q,
                                  "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faqs"]]}
    svc_schema = {"@context": "https://schema.org", "@type": "Service",
                  "serviceType": s["h1"], "provider": {"@type": "Person", "name": "Taimoor Ali"},
                  "areaServed": ["US", "GB", "CA", "AU"], "url": SITE + s["slug"],
                  "description": s["meta"]}
    schema = [svc_schema, faq_schema]

    out = head(s["seo_title"], s["meta"], s["slug"], schema)
    out += header()
    out += '<main id="main">'
    out += f"""<section class="page-hero"><div class="wrap measure reveal">
    {bc}
    <p class="eyebrow">{s["eyebrow"]}</p>
    <h1 class="h1">{s["h1"]}</h1>
    <p class="lead">{s["hero"]}</p>
    <div class="hero-cta"><a class="btn btn--primary btn--lg" href="/book/">Book a Call <span class="arw">→</span></a></div>
  </div></section>"""
    out += f"""<section class="section section--tight"><div class="wrap colset">
    <div class="prose reveal">
      <h2>You need this if…</h2>
      <ul>{symptoms}</ul>
      <h2>What I build</h2>
      <p>{s["what"]}</p>
      <h2>What's included</h2>
      <ul>{included}</ul>
      <h2>How it works</h2>
      <ol style="color:var(--ink-soft);padding-left:1.1rem;display:grid;gap:.5rem">{process}</ol>
    </div>
    <aside class="reveal"><div class="sidecard">
      <h4>Systems &amp; integrations</h4>
      {systems}
      <a class="btn btn--primary" href="/book/">Book a Call <span class="arw">→</span></a>
      <a class="textlink proof-link" href="{s["proof_url"]}">Proof: {s["proof"]} <span class="arw">→</span></a>
    </div></aside>
  </div></section>"""
    out += f"""<section class="section section--surface"><div class="wrap measure reveal">
    <p class="eyebrow">Questions</p><h2 class="h2" style="margin:.7rem 0 1.4rem">Common questions</h2>
    <div class="faq">{faqs}</div>
    <div class="related">{related}</div>
  </div></section>"""
    out += cta_band()
    out += "</main>" + footer()
    write(s["slug"].lstrip("/") + "index.html", out)


SERVICE_DATA = [
 {"slug":"/services/operations-audit/","crumb":"Operations Audit","eyebrow":"Start here",
  "seo_title":"Shopify Operations Audit & Automation Roadmap | Taimoor Ali",
  "meta":"A fixed-fee operations audit for growing Shopify brands. I map your systems, find every manual leak, and deliver a prioritized automation roadmap with ROI. Book a call.",
  "h1":"Shopify Operations Audit & Automation Roadmap",
  "hero":"Before you build anything, you need to know what's actually broken. The Operations Audit maps your entire ecommerce back office — Shopify, ERP, 3PL, subscriptions, spreadsheets, and every handoff between them — and hands you a prioritized roadmap of what to automate first, what it's worth, and what it takes.",
  "symptoms":["You're not sure where the manual work is costing you most.","You keep adding apps and the chaos grows.","Your headcount scales faster than your revenue.","You want to automate but don't know the right sequence.","You've been quoted for builds, but nobody diagnosed the problem first."],
  "what":"A complete operational map of your stack, a ranked list of automation opportunities (impact × effort × ROI), a target architecture, and a phased implementation roadmap you can execute with me or anyone.",
  "included":["Systems &amp; data-flow audit","Manual-work inventory","Integration gap analysis","Prioritized automation roadmap","Target architecture diagram","Written recommendations + a walkthrough call"],
  "systems":["Shopify / Shopify Plus","ERP (NetSuite, SAP, Dynamics)","3PL / WMS","Subscription platforms","Google Sheets","Marketplaces &amp; sales channels","Your existing app stack"],
  "process":["Intake &amp; least-privilege access","Systems mapping","Opportunity analysis","Roadmap delivery &amp; walkthrough"],
  "proof":"WhisperSheet","proof_url":"/results/whispersheet/",
  "faqs":[("What do I get at the end?","A roadmap document, a target architecture, and a walkthrough call — a clear, prioritized plan you own."),("Do I have to build with you afterwards?","No. The roadmap is yours to execute with me or any team."),("How long does it take?","Typically one to two weeks, depending on the size of your stack."),("What access do you need?","Read-only, least-privilege access, fully documented — nothing more than required."),("Is it worth it if I already know my problems?","The audit usually surfaces the expensive problems you can't see, and sequences the fixes by ROI.")],
  "related":[("/services/inventory-sync/","Inventory Sync"),("/services/erp-integrations/","ERP Integrations"),("/services/operations-partner/","Operations Partner")]},

 {"slug":"/services/inventory-sync/","crumb":"Inventory & Data Sync","eyebrow":"Flagship build",
  "seo_title":"Shopify Inventory Sync & Data Synchronization Systems | Taimoor Ali",
  "meta":"Stop fighting wrong inventory across channels. I build inventory and data sync systems that keep Shopify, ERP, 3PL, Sheets, and sales channels in perfect lockstep.",
  "h1":"Shopify Inventory Sync — One Source of Truth Across Every Channel",
  "hero":"When Shopify, your ERP, your 3PL, your spreadsheets, and your marketplaces all disagree about how much stock you have, someone pays for it — in oversells, stockouts, manual reconciliation, and lost trust. I build the sync systems that make every system agree, automatically.",
  "symptoms":["Inventory counts drift between channels.","Oversells and stockouts you can't explain.","Someone manually reconciles stock every day.","New SKUs take forever to propagate.","Multi-store or multi-warehouse counts never line up.","Google Sheets is your accidental inventory database."],
  "what":"Real-time or scheduled inventory and data synchronization across Shopify, ERP, 3PL/WMS, marketplaces, and Google Sheets — with conflict handling, error alerting, and a single authoritative source of truth.",
  "included":["Sync architecture design","Source-of-truth definition","One-way or two-way sync logic","Conflict resolution rules","Error handling &amp; alerting","Monitoring + documentation &amp; handover"],
  "systems":["Shopify Admin &amp; GraphQL APIs","Webhooks","ERP connectors","3PL / WMS APIs","Google Sheets API","Marketplace channels","Background job queues"],
  "process":["Audit your current inventory flows","Design the sync architecture","Build the sync engine","Test against edge cases","Deploy &amp; monitor","Document &amp; hand over"],
  "proof":"WhisperSheet — 80% less manual inventory work","proof_url":"/results/whispersheet/",
  "faqs":[("Real-time or scheduled?","It depends on your volume and risk tolerance — we decide in the audit. Both are supported."),("Which systems can you connect?","Anything with an API: Shopify, ERPs, 3PLs, marketplaces, and Google Sheets are the common ones."),("What happens on a conflict?","Defined rules — never a silent overwrite. You decide which system wins, per data type."),("Do you handle multi-store and multi-warehouse?","Yes. Multi-store, multi-location, and multi-warehouse sync are core to this work."),("Will it break when I scale?","It's built for scale — queues, idempotency, retries, and monitoring keep it reliable as volume grows.")],
  "related":[("/services/erp-integrations/","ERP Integrations"),("/services/order-fulfillment-automation/","Fulfillment Automation"),("/services/operations-audit/","Operations Audit")]},

 {"slug":"/services/erp-integrations/","crumb":"ERP & Integrations","eyebrow":"Build",
  "seo_title":"Shopify ERP Integration & Third-Party System Integrations | Taimoor Ali",
  "meta":"Connect Shopify to your ERP and the rest of your stack. I build ERP and third-party integrations that move orders, inventory, and customer data automatically.",
  "h1":"Shopify ERP Integration That Ends Manual Data Entry",
  "hero":"If your team is re-keying orders, inventory, or customers between Shopify and your ERP — or any other critical system — you're paying for errors and lost hours every single day. I build the integrations that move that data automatically and reliably.",
  "symptoms":["Orders manually entered into the ERP.","Inventory and fulfillment statuses out of sync.","Customer or financial data duplicated by hand.","Brittle one-off scripts that keep breaking.","Tools that simply don't talk to each other.","Growth blocked by back-office data entry."],
  "what":"Robust, monitored integrations between Shopify and ERP, accounting, CRM, 3PL, and other third-party systems — moving orders, inventory, customers, and fulfillment data automatically, with error handling and reconciliation.",
  "included":["Integration architecture","Field mapping","Sync direction &amp; triggers","Error handling &amp; retries","Reconciliation &amp; logging","Monitoring, alerts &amp; documentation"],
  "systems":["Shopify APIs &amp; webhooks","ERP (NetSuite, SAP, Dynamics)","Accounting &amp; CRM platforms","Middleware / queues","Customer-data synchronization","Third-party APIs"],
  "process":["Audit the systems and data flows","Map fields and directions","Build the integration","Test, including failure cases","Deploy &amp; monitor","Document &amp; hand over"],
  "proof":"Neesh — multi-vendor marketplace","proof_url":"/results/neesh/",
  "faqs":[("Which ERPs do you work with?","Any ERP with an API — NetSuite, SAP, Microsoft Dynamics, and others are common."),("What if a system has no API?","File-based or middleware approaches can bridge it. We confirm the right path in the audit."),("How do you handle failures?","Retries, alerts, and reconciliation — nothing fails silently or disappears."),("Custom or off-the-shelf?","Off-the-shelf connectors when they fit, custom when they don't. The audit decides.")],
  "related":[("/services/inventory-sync/","Inventory Sync"),("/services/shopify-apps/","Custom Apps & API"),("/services/operations-audit/","Operations Audit")]},

 {"slug":"/services/subscription-automation/","crumb":"Subscription Operations","eyebrow":"Build",
  "seo_title":"Shopify Subscription Operations & Automation | Taimoor Ali",
  "meta":"Tame subscription chaos. I automate the operations behind Shopify subscriptions — billing edge cases, fulfillment, churn flows, and data sync — so it scales itself.",
  "h1":"Shopify Subscription Operations & Automation",
  "hero":"Subscriptions are where operational complexity hides: failed payments, swaps, skips, dunning, fulfillment timing, and data that has to stay perfect across systems. I automate the operations underneath your subscription program so it scales without a person babysitting every edge case.",
  "symptoms":["Manual handling of failed payments, swaps, and skips.","Subscription data out of sync with fulfillment or ERP.","Churn from billing friction nobody has time to fix.","Custom subscription logic your app can't handle.","Reporting cobbled together by hand."],
  "what":"Automation around your subscription platform — billing edge-case handling, fulfillment orchestration, dunning and retry flows, data sync to ERP/3PL, and custom logic your subscription app doesn't support natively.",
  "included":["Subscription operations audit","Automation design","Billing &amp; fulfillment workflow build","Data sync","Custom logic / app extensions","Monitoring &amp; documentation"],
  "systems":["Recharge / Shopify subscription APIs","Shopify Admin API &amp; webhooks","Payment gateways","3PL / fulfillment","ERP","Notification systems"],
  "process":["Audit your subscription operations","Design the automations","Build the workflows","Test the edge cases","Deploy &amp; monitor"],
  "proof":"WhisperSheet & automation builds","proof_url":"/results/whispersheet/",
  "faqs":[("Which subscription apps do you work with?","Recharge and other Shopify subscription platforms via their APIs."),("Can you extend logic the app can't do?","Yes — through custom integration or a custom app where needed."),("Will this reduce churn?","It removes the operational friction — failed payments, delays — that causes avoidable churn."),("Does it sync to my ERP and 3PL?","Yes, keeping subscription, fulfillment, and finance data aligned.")],
  "related":[("/services/order-fulfillment-automation/","Fulfillment Automation"),("/services/erp-integrations/","ERP Integrations"),("/services/operations-partner/","Operations Partner")]},

 {"slug":"/services/order-fulfillment-automation/","crumb":"Order & Fulfillment","eyebrow":"Build",
  "seo_title":"Shopify Order & Fulfillment Automation | Taimoor Ali",
  "meta":"Stop processing orders by hand. I automate order routing, fulfillment, and 3PL/warehouse workflows so orders move from checkout to doorstep without manual steps.",
  "h1":"Shopify Order & Fulfillment Automation",
  "hero":"From checkout to doorstep — without anyone touching a spreadsheet. Every order your team processes by hand is a cost and a chance for error. I automate order routing, fulfillment workflows, 3PL and warehouse handoffs, and the exceptions that usually need a human.",
  "symptoms":["Orders manually sorted, tagged, or routed.","Fulfillment handoffs done by hand.","Exceptions and holds managed in spreadsheets.","Multi-location or multi-3PL routing that's all manual.","Disputes from delivery or fulfillment errors."],
  "what":"Automated order routing and fulfillment workflows — tagging, splitting, routing by location, 3PL, or rules, warehouse and 3PL integration, exception handling, and delivery verification where needed.",
  "included":["Workflow design","Routing &amp; tagging logic","3PL / WMS integration","Exception handling","Notifications","Monitoring &amp; documentation"],
  "systems":["Shopify Flow &amp; Admin API","Webhooks","3PL / WMS APIs","Shipping platforms","Warehouse apps","Custom rules engines"],
  "process":["Audit your order flows","Design the routing rules","Build the automations","Test the exceptions","Deploy &amp; monitor"],
  "proof":"INK — 90% fewer fulfillment disputes","proof_url":"/results/ink/",
  "faqs":[("Multi-3PL or multi-location?","Yes — rules-based routing handles multiple warehouses and 3PLs."),("Can you handle exceptions and holds?","Yes — defined exception flows, not silent failures."),("Native Shopify Flow or custom?","Both, depending on complexity. Simple rules use Flow; complex logic gets a custom build."),("Can you add delivery verification?","Yes — see the INK case study for a verified-delivery system.")],
  "related":[("/services/inventory-sync/","Inventory Sync"),("/services/subscription-automation/","Subscription Operations"),("/services/operations-audit/","Operations Audit")]},

 {"slug":"/services/shopify-apps/","crumb":"Custom Apps & API","eyebrow":"Build",
  "seo_title":"Custom Shopify App & API Development | Taimoor Ali",
  "meta":"When off-the-shelf apps can't do it, I build custom Shopify apps and API integrations engineered for your operation — not a generic plugin.",
  "h1":"Custom Shopify App & API Development",
  "hero":"When no app does what you need, I build the one that does. Sometimes the operational problem doesn't have an app — or the apps that exist create as much chaos as they solve. I design and build custom Shopify apps and API integrations engineered around your specific operation, owned by you, and built to scale.",
  "symptoms":["You're paying for five apps to do one job badly.","An app almost does what you need — but not quite.","You need logic no app supports.","App sprawl is creating data and performance problems.","You want to own the tool, not rent it."],
  "what":"Custom Shopify apps (public or custom/private), embedded admin tools, API integrations, and internal operations tooling — designed around your workflow and engineered for reliability at scale.",
  "included":["Requirements &amp; architecture","App / integration build","Shopify admin embedding where relevant","API integrations","Testing &amp; deployment","Documentation &amp; handover"],
  "systems":["Shopify App framework","Admin &amp; GraphQL APIs","Webhooks &amp; App Bridge","OAuth","Polaris (where embedded)","Node.js backends, databases, queues"],
  "process":["Scope and architect","Build the app","Test thoroughly","Deploy","Document &amp; hand over"],
  "proof":"WhisperSheet & INK","proof_url":"/results/whispersheet/",
  "faqs":[("Public or custom app?","Whichever fits — custom/private apps for internal operations, public where it makes sense."),("Do I own it?","Yes. The app and its code are yours."),("Will it pass Shopify review?","Public apps are built to Shopify's requirements."),("Can you maintain it afterwards?","Yes — via the Operations Partner retainer.")],
  "related":[("/services/erp-integrations/","ERP Integrations"),("/services/inventory-sync/","Inventory Sync"),("/services/operations-partner/","Operations Partner")]},

 {"slug":"/services/operations-partner/","crumb":"Operations Partner","eyebrow":"Ongoing · retainer",
  "seo_title":"Shopify Operations Partner — Fractional Automation Engineer | Taimoor Ali",
  "meta":"Ongoing Shopify operations and automation support on retainer. Your fractional automation engineer for monitoring, new builds, and integration upkeep as you scale.",
  "h1":"Your Fractional Shopify Operations & Automation Partner",
  "hero":"Operations don't stop evolving once a build ships — new channels, new tools, new edge cases, and the constant need to keep integrations healthy. The Operations Partner retainer gives growing brands ongoing access to the person who knows their systems.",
  "symptoms":["Your integrations need ongoing care.","You keep needing 'one more automation'.","You want a technical partner who already knows your stack.","You don't need a full-time hire, but you need more than one-off projects.","You want someone accountable for keeping operations healthy."],
  "what":"Ongoing automation development, integration monitoring and maintenance, priority builds, architecture advisory, and a known partner who understands your operation end to end.",
  "included":["Monthly allocation","Monitoring &amp; alerts on existing systems","New automation builds","Integration upkeep","Architecture &amp; strategy calls","Priority response"],
  "systems":["The full stack already in place","Plus whatever you add as you grow"],
  "process":["Onboarding &amp; systems handover","Monthly cadence: priorities, builds, reviews","Continuous monitoring"],
  "proof":"All case studies","proof_url":"/results/",
  "faqs":[("What's included each month?","A defined allocation tiered to your needs — monitoring, builds, and advisory."),("Is there a minimum term?","Retainer terms are scoped after the first audit or build, so the monthly support matches the systems you actually need maintained."),("Can I start here without an audit?","It works best after an audit or an initial build, once your systems are mapped."),("What's your response time?","Priority over project clients — defined per plan.")],
  "related":[("/services/operations-audit/","Operations Audit"),("/results/","Results"),("/services/","All services")]},
]

# ----------------------------------------------------------------------------
# Services overview
# ----------------------------------------------------------------------------
def services_overview():
    cards = ""
    labels = ["Start here","Build","Build","Build","Build","Build","Ongoing · retainer"]
    for (slug, name, sub), lab in zip(SERVICES, labels):
        cards += f"""<a class="lad-card reveal" href="{slug}" style="text-decoration:none">
        <span class="lad-num">{lab}</span><h3>{name}</h3><p>{sub}.</p>
        <span class="textlink" style="margin-top:1rem">Explore <span class="arw">→</span></span></a>"""
    schema = {"@context":"https://schema.org","@type":"CollectionPage","name":"Services","url":SITE+"/services/"}
    out = head("Shopify Operations & Automation Services | Taimoor Ali",
               "Three ways to work with me: a fixed-fee operations audit, fixed-scope integration and automation builds, and an ongoing operations partner retainer for growing Shopify brands.",
               "/services/", schema)
    out += header() + '<main id="main">'
    out += """<section class="page-hero"><div class="wrap measure reveal">
      <div class="breadcrumb"><a href="/">Home</a> / Services</div>
      <p class="eyebrow">Services</p>
      <h1 class="h1">Shopify Operations, Integration &amp; Automation Services</h1>
      <p class="lead">I help growing Shopify and DTC brands replace manual operations with systems that run themselves. Most engagements start with an audit, move into a fixed-scope build, and graduate into an ongoing partnership.</p>
    </div></section>"""
    out += f'<section class="section section--tight"><div class="wrap"><div class="ladder" style="margin-top:0">{cards}</div></div></section>'
    out += cta_band()
    out += "</main>" + footer()
    write("services/index.html", out)

# ----------------------------------------------------------------------------
# Case studies
# ----------------------------------------------------------------------------
def render_case(c):
    bc = f'<div class="breadcrumb"><a href="/">Home</a> / <a href="/results/">Results</a> / {c["brand"]}</div>'
    integ = "".join(f'<div class="sys-item"><span style="color:var(--accent)">▸</span>{x}</div>' for x in c["integrations"])
    related = "".join(f'<a href="{h_}">{n}</a>' for h_, n in c["related"])
    snap = c["snapshot"]
    schema = {"@context":"https://schema.org","@type":"Article","headline":c["outcome"],
              "author":{"@type":"Person","name":"Taimoor Ali"},"url":SITE+c["slug"],"description":c["meta"]}
    out = head(c["seo_title"], c["meta"], c["slug"], schema, og_type="article")
    out += header() + '<main id="main">'
    out += f"""<section class="page-hero"><div class="wrap measure reveal">
    {bc}
    <p class="eyebrow">{c["brand"]} · Case study</p>
    <h1 class="h1">{c["outcome"]}</h1>
  </div></section>"""
    out += f"""<section class="section--tight"><div class="wrap reveal">
    <div class="snapshot">
      <div class="cell"><div class="ck">Client</div><div class="cv">{snap[0]}</div></div>
      <div class="cell"><div class="ck">Result</div><div class="cv">{snap[1]}</div></div>
      <div class="cell"><div class="ck">Systems</div><div class="cv">{snap[2]}</div></div>
      <div class="cell"><div class="ck">Role</div><div class="cv">{snap[3]}</div></div>
    </div>
  </div></section>"""
    out += f"""<section class="section section--tight" style="padding-top:0"><div class="wrap colset">
    <div class="prose reveal">
      <h2>Context</h2><p>{c["context"]}</p>
      <h2>The problem</h2><p>{c["problem"]}</p>
      <h2>The operational bottleneck</h2><p>{c["bottleneck"]}</p>
      <h2>Solution architecture</h2><p>{c["architecture"]}</p>
      <h2>Results</h2>
      <div class="case-result"><div class="ck">Outcome</div><p>{c["results"]}</p></div>
      <h2>Business impact</h2><p>{c["impact"]}</p>
    </div>
    <aside class="reveal"><div class="sidecard">
      <h4>Integrations involved</h4>{integ}
      <a class="btn btn--primary" href="/book/">Book a Call <span class="arw">→</span></a>
    </div></aside>
  </div></section>"""
    out += f'<section class="section section--surface"><div class="wrap measure reveal"><p class="eyebrow">Keep exploring</p><h2 class="h2" style="margin:.7rem 0 0">Facing a similar problem?</h2><div class="related">{related}</div></div></section>'
    out += cta_band(h2="Have a problem like "+c["brand"]+"'s?")
    out += "</main>" + footer()
    write(c["slug"].lstrip("/") + "index.html", out)

CASE_DATA = [
 {"slug":"/results/whispersheet/","brand":"WhisperSheet",
  "seo_title":"WhisperSheet: Shopify Inventory Sync Case Study | Taimoor Ali",
  "meta":"How a Shopify inventory sync system kept stores and Google Sheets in perfect lockstep and cut manual inventory work 80% for multi-store brands.",
  "outcome":"Cut manual inventory work 80% for multi-store brands.",
  "snapshot":["SaaS · multi-store Shopify brands","80% less manual inventory work","Shopify, Google Sheets, background jobs","Lead architect &amp; developer (owned product)"],
  "context":"WhisperSheet is a SaaS product — built and owned by Taimoor — serving Shopify brands that run part of their operations out of Google Sheets and need those sheets and their stores to stay in perfect agreement.",
  "problem":"Brands managing inventory across multiple stores and spreadsheets faced constant drift — counts in Sheets and Shopify never matched, forcing late-night manual edits and risking oversells.",
  "bottleneck":"Inventory truth was split between Shopify and Google Sheets, with humans acting as the sync mechanism — slow, error-prone, and impossible to scale as store count grew.",
  "architecture":"A synchronization engine keeps Shopify and Google Sheets in lockstep: a defined source of truth, automated two-way updates, conflict handling, and error alerting — removing the human from the loop entirely.",
  "integrations":["Shopify Admin / GraphQL API","Webhooks","Google Sheets API","Background job queue","Monitoring &amp; alerting"],
  "results":"~80% reduction in manual inventory work, the end of midnight spreadsheet reconciliation, and reliable, scalable sync across multiple stores.",
  "impact":"Teams reclaimed 20+ hours a week, reduced oversell risk, and gained an inventory system that scales with store count instead of headcount.",
  "related":[("/services/inventory-sync/","Inventory & Data Sync"),("/services/shopify-apps/","Custom Apps & API")]},

 {"slug":"/results/ink/","brand":"INK",
  "seo_title":"INK: Shopify Fulfillment & Delivery Verification Case Study | Taimoor Ali",
  "meta":"How a verified-delivery system eliminated fake deliveries and cut fulfillment disputes 90% while keeping inventory airtight from pack to doorstep.",
  "outcome":"Eliminated fake deliveries and cut fulfillment disputes 90%.",
  "snapshot":["SaaS · Shopify app","~90% fewer fulfillment disputes","Shopify app, NFC verification, warehouse app","Development &amp; implementation lead"],
  "context":"INK is a verified-delivery system for Shopify brands — confirming real package handoffs and keeping inventory airtight from pack to doorstep.",
  "problem":"Brands faced disputed and fraudulent 'non-deliveries' that cost money and eroded trust, with no reliable proof of handoff.",
  "bottleneck":"There was no verifiable link between a shipped package and a confirmed real-world delivery, and inventory accuracy degraded between warehouse and doorstep.",
  "architecture":"NFC-tagged packages confirm genuine handoffs, while a warehouse app keeps inventory accurate from pack to delivery — closing the gap between digital records and physical reality.",
  "integrations":["Shopify app framework &amp; APIs","NFC tag verification","Warehouse / inventory app","Webhooks"],
  "results":"~90% reduction in fulfillment disputes, near-elimination of fake-delivery claims, and tighter inventory accuracy.",
  "impact":"Recovered revenue lost to disputes, protected brand trust, and gave operations verifiable delivery data.",
  "related":[("/services/order-fulfillment-automation/","Order & Fulfillment"),("/services/shopify-apps/","Custom Apps & API")]},

 {"slug":"/results/neesh/","brand":"Neesh",
  "seo_title":"Neesh: Shopify Multi-Vendor B2B Marketplace Case Study | Taimoor Ali",
  "meta":"How a custom Shopify integration with multi-vendor logic turned a print publisher into a thriving B2B marketplace connecting publishers, retailers, and inventory.",
  "outcome":"Turning a print magazine into a B2B Shopify marketplace.",
  "snapshot":["B2B marketplace","Launched multi-vendor marketplace","Shopify API, multi-vendor logic, Node.js","Lead developer, end to end"],
  "context":"Neesh transformed from a print publication into a digital B2B marketplace connecting publishers, retailers, and inventory under one storefront.",
  "problem":"A traditional publisher needed to become a multi-sided marketplace — connecting many vendors, retailers, and inventory sources in one Shopify-based platform.",
  "bottleneck":"There was no system to manage multi-vendor catalogs, inventory, and order routing across publishers and retailers at once.",
  "architecture":"A custom Shopify integration with multi-vendor logic links publishers, retailers, and inventory under a single storefront, with the order and inventory routing to support it.",
  "integrations":["Shopify API","Custom multi-vendor logic","Node.js backend","Inventory / order routing"],
  "results":"A functioning B2B marketplace serving multiple vendors and retailers.",
  "impact":"Opened a new digital revenue model for a legacy publisher and created a scalable multi-vendor platform.",
  "related":[("/services/erp-integrations/","ERP & Integrations"),("/services/shopify-apps/","Custom Apps & API")]},
]

def results_index():
    cards = ""
    for c in CASE_DATA:
        cards += f"""<a class="res-card reveal" href="{c['slug']}">
        <span class="res-brand">{c['brand']}</span>
        <h3>{c['outcome']}</h3>
        <p>{c['snapshot'][2]}</p>
        <span class="textlink" style="margin-top:1rem">Read the case study <span class="arw">→</span></span></a>"""
    schema = {"@context":"https://schema.org","@type":"CollectionPage","name":"Results","url":SITE+"/results/"}
    out = head("Shopify Automation & Integration Case Studies | Taimoor Ali",
               "Real outcomes from Shopify operations and automation work — inventory sync, fulfillment integrity, and multi-vendor marketplace builds.",
               "/results/", schema)
    out += header() + '<main id="main">'
    out += """<section class="page-hero"><div class="wrap measure reveal">
      <div class="breadcrumb"><a href="/">Home</a> / Results</div>
      <p class="eyebrow">Results</p>
      <h1 class="h1">Results — operations, integration &amp; automation.</h1>
      <p class="lead">Every project below started with a real business problem. Outcome first, technology second.</p>
    </div></section>"""
    out += f'<section class="section section--tight"><div class="wrap"><div class="results-grid" style="margin-top:0">{cards}</div></div></section>'
    out += cta_band()
    out += "</main>" + footer()
    write("results/index.html", out)

# ----------------------------------------------------------------------------
# About
# ----------------------------------------------------------------------------
def about():
    schema = {"@context":"https://schema.org","@type":"Person","name":"Taimoor Ali",
              "jobTitle":"Shopify Integration & Ecommerce Automation Specialist",
              "url":SITE+"/about/","description":"Shopify integration and ecommerce automation specialist who helps growing brands replace operational chaos with systems that run themselves.",
              "sameAs":["https://www.linkedin.com/in/taimoor-ali-8694a52ba/","https://github.com/taimoorali-code","https://www.upwork.com/freelancers/~019281523908b93a20"]}
    out = head("About Taimoor Ali — Shopify Integration & Automation Specialist",
               "Taimoor Ali is a Shopify integration and ecommerce automation specialist who helps growing brands replace operational chaos with systems that run themselves.",
               "/about/", schema)
    out += header() + '<main id="main">'
    out += """<section class="page-hero"><div class="wrap measure reveal">
      <div class="breadcrumb"><a href="/">Home</a> / About</div>
      <p class="eyebrow">About</p>
      <h1 class="h1">I'm Taimoor Ali — Shopify integration &amp; ecommerce automation specialist.</h1>
      <p class="lead">I help growing Shopify, Plus, DTC and subscription brands replace operational chaos with systems that run themselves.</p>
    </div></section>"""
    out += """<section class="section section--tight" style="padding-top:0"><div class="wrap colset">
      <div class="prose reveal">
        <h2>What I actually do</h2>
        <p>Most growing brands hit the same wall: the team becomes the glue holding operations together. Inventory drifts across channels. Orders get re-keyed between systems. Subscriptions run on workarounds. I build the integrations and automations that remove the human from that loop — so the back office runs on its own and the team scales output instead of headcount.</p>
        <h2>Why work with me instead of a developer or a consultant</h2>
        <p>A Shopify developer builds what you spec, but won't tell you the architecture is the real problem. An operations consultant hands you a strategy, then hands the build to someone else — and projects die in that gap. I'm both: I diagnose the operational chaos and engineer the system that ends it. One person, one line of accountability, no handoff.</p>
        <h2>How I work</h2>
        <p>Engagements usually start with an Operations Audit — a fixed-fee diagnosis that maps your systems and hands you a prioritized automation roadmap. From there, fixed-scope builds implement the roadmap, and an ongoing partnership keeps everything healthy as you grow. I price on the value of the problem solved, not the hours.</p>
        <h2>The work behind it</h2>
        <p>Selected work includes WhisperSheet (an owned inventory-sync SaaS that cut manual inventory work 80%), INK (a verified-delivery system that cut fulfillment disputes 90%), Neesh (a multi-vendor B2B marketplace), and Shopify Plus development and integrations for brands including Elie Saab, within my assigned scope. The throughline is the same: disconnected systems, made to run as one.</p>
        <div class="related">
          <a href="/results/">See the results</a>
          <a href="/services/">Explore services</a>
          <a href="/book/">Book a call</a>
        </div>
      </div>
      <aside class="reveal"><div class="sidecard">
        <div class="profile">
          <img class="profile-img" src="/assets/images/avatar.png" alt="Taimoor Ali" width="64" height="64">
          <div class="profile-meta"><span class="profile-name">Taimoor Ali</span><span class="profile-role">Shopify Operations &amp; Automation</span></div>
        </div>
        <h4>At a glance</h4>
        <div class="sys-item"><span style="color:var(--accent)">▸</span>Shopify &amp; Shopify Plus operations</div>
        <div class="sys-item"><span style="color:var(--accent)">▸</span>Inventory &amp; data synchronization</div>
        <div class="sys-item"><span style="color:var(--accent)">▸</span>ERP &amp; third-party integrations</div>
        <div class="sys-item"><span style="color:var(--accent)">▸</span>Subscription operations</div>
        <div class="sys-item"><span style="color:var(--accent)">▸</span>Order &amp; fulfillment automation</div>
        <div class="sys-item"><span style="color:var(--accent)">▸</span>Custom Shopify apps &amp; API</div>
        <a class="btn btn--primary" href="/book/">Book a Call <span class="arw">→</span></a>
        <a class="textlink proof-link" href="https://www.upwork.com/freelancers/~019281523908b93a20" rel="noopener">5.0 on Upwork <span class="arw">→</span></a>
      </div></aside>
    </div></section>"""
    out += cta_band()
    out += "</main>" + footer()
    write("about/index.html", out)

# ----------------------------------------------------------------------------
# Book a Call
# ----------------------------------------------------------------------------
def book():
    out = head("Book a Call | Shopify Operations & Automation | Taimoor Ali",
               "Book a 30-minute call to map your operational bottlenecks and see whether a Shopify Operations Audit is the right first step. No pitch.",
               "/book/")
    out += header() + '<main id="main">'
    out += """<section class="page-hero"><div class="wrap reveal">
      <div class="breadcrumb"><a href="/">Home</a> / Book a Call</div>
      <p class="eyebrow">Let's talk</p>
      <h1 class="h1">Let's find what's slowing your operations down.</h1>
    </div></section>"""
    out += """<section class="section section--tight" style="padding-top:0"><div class="wrap book-grid">
      <div class="reveal">
        <p class="lead">A 30-minute call to understand your operation and whether an Operations Audit is the right first step. No pitch — you'll leave with at least one clear next action.</p>
        <p class="eyebrow" style="margin-top:2rem">What to expect</p>
        <ul class="expect">
          <li>We map the problem at a high level.</li>
          <li>I tell you honestly whether I can help.</li>
          <li>If it's a fit, I explain how the Operations Audit works.</li>
        </ul>
        <p style="color:var(--muted);font-size:.9rem;margin-top:1.4rem">Working remotely across US, UK, Canada &amp; Australia time zones. I usually reply within one business day.</p>
      </div>
      <div class="reveal"><div class="form-card">
        <form id="bookingForm" novalidate data-mailto="bookings@taimoorproject.site">
          <div class="field"><label for="name">Name</label><input id="name" name="name" required></div>
          <div class="field"><label for="email">Work email</label><input id="email" name="email" type="email" required></div>
          <div class="field"><label for="brand">Brand / store name + URL</label><input id="brand" name="brand" required></div>
          <div class="field"><label for="platform">Platform</label>
            <select id="platform" name="platform"><option>Shopify</option><option>Shopify Plus</option><option>Other</option></select></div>
          <div class="field"><label for="rev">Approx. monthly revenue or order volume</label>
            <select id="rev" name="rev"><option>Under $50k / mo</option><option>$50k–$250k / mo</option><option>$250k–$1M / mo</option><option>$1M+ / mo</option></select></div>
          <div class="field"><label for="role">Your role</label>
            <select id="role" name="role"><option>Founder</option><option>COO</option><option>Operations</option><option>Other</option></select></div>
          <div class="field"><label for="problem">What operational problem are you trying to solve?</label><textarea id="problem" name="problem" required></textarea></div>
          <div class="field"><label for="timeline">Timeline</label>
            <select id="timeline" name="timeline"><option>Exploring</option><option>Next 1–3 months</option><option>Urgent</option></select></div>
          <button class="btn btn--primary btn--lg" type="submit" style="width:100%;justify-content:center">Request a Call <span class="arw">→</span></button>
          <p class="form-note">This sends a short intake request so I can review your stack before the call.</p>
          <div class="form-msg" id="formMsg" role="status"></div>
        </form>
      </div></div>
    </div></section>"""
    out += "</main>" + footer()
    write("book/index.html", out)

# ----------------------------------------------------------------------------
# sitemap + robots
# ----------------------------------------------------------------------------
def sitemap():
    urls = ["/","/services/","/results/","/about/","/book/"]
    urls += [s["slug"] for s in SERVICE_DATA]
    urls += [c["slug"] for c in CASE_DATA]
    body = "".join(f"<url><loc>{SITE}{u}</loc></url>" for u in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

# ----------------------------------------------------------------------------
if __name__ == "__main__":
    homepage()
    services_overview()
    for s in SERVICE_DATA:
        render_service(s)
    results_index()
    for c in CASE_DATA:
        render_case(c)
    about()
    book()
    sitemap()
    print("\nDone.")
