#!/usr/bin/env python3
"""Builds the static SOLO Agency site. Run from the repo root: python3 tools/build.py"""
import html, os, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = "solo.studios.co@gmail.com"
SITE = "SOLO Agency"

ICONS = {
 "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
 "music": '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
 "trend": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
 "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
 "camera": '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/>',
 "sparkles": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 3v4M17 5h4"/>',
 "book": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
 "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
 "mic": '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10v1a7 7 0 0 0 14 0v-1"/><path d="M12 18v4"/>',
 "star": '<polygon points="12 2 15.1 8.3 22 9.3 17 14.1 18.2 21 12 17.8 5.8 21 7 14.1 2 9.3 8.9 8.3"/>',
 "plane": '<path d="M2 12l20-8-8 20-3-9z"/>',
 "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
 "palette": '<circle cx="13.5" cy="6.5" r=".5"/><circle cx="17.5" cy="10.5" r=".5"/><circle cx="8.5" cy="7.5" r=".5"/><circle cx="6.5" cy="12.5" r=".5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.9 0 1.7-.8 1.7-1.7 0-.4-.2-.8-.5-1.1-.3-.3-.4-.7-.4-1.1 0-.9.8-1.7 1.7-1.7H16c3.3 0 6-2.7 6-6 0-4.9-4.5-9-10-9z"/>',
 "chart": '<path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>',
 "clipboard": '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
 "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
 "bar": '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>',
 "bot": '<rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><path d="M8 16h.01M16 16h.01"/>',
 "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
 "money": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01M18 12h.01"/>',
 "share": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/>',
 "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
 "pin": '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
 "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
}
def icon(name, cls="", gold=False):
    return f'<div class="icon{" gold" if gold else ""}"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg></div>'

NAV = [("index.html","Home"),("models.html","Models"),("artists.html","Artists"),("brand-scaling.html","Brand Scaling"),
       ("companies.html","Companies"),("work.html","Work"),("pricing.html","Pricing"),("join.html","Join the Network"),("contact.html","Contact")]

def apply_url(t=None):
    return "apply.html" + ("?type=" + urllib.parse.quote(t) if t else "")

def header(cur):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{l}</a>' for h,l in NAV)
    mlinks = "".join(f'<a href="{h}">{l}</a>' for h,l in NAV)
    return f'''<header class="site-header"><div class="wrap nav-row">
  <a class="brand" href="index.html" aria-label="SOLO Marketing Agency"><img src="assets/img/solo-logo.png" alt="SOLO" width="97" height="30"><span>Marketing Agency</span></a>
  <nav class="nav-links" aria-label="Main">{links}</nav>
  <a class="btn btn-gold nav-cta" href="apply.html">Apply</a>
  <button class="menu-btn" id="menuBtn" aria-label="Menu" aria-expanded="false" aria-controls="mobileNav"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">{ICONS["menu"]}</svg></button>
</div>
<div class="mobile-nav" id="mobileNav">{mlinks}<a class="btn btn-gold" href="apply.html">Apply</a></div></header>'''

def footer():
    return f'''<footer class="site-footer"><div class="wrap foot-grid">
  <div><img src="assets/img/solo-logo.png" alt="SOLO" width="110" height="34"><p class="note" style="max-width:340px;margin-top:0">Talent management and brand growth, under one roof. London, remote-friendly.</p>
  <p style="margin-top:14px"><a href="mailto:{EMAIL}" style="text-decoration:underline">{EMAIL}</a></p></div>
  <div><h4>Talent</h4><ul><li><a href="models.html">Models</a></li><li><a href="artists.html">Artists</a></li><li><a href="join.html">Join the Network</a></li></ul></div>
  <div><h4>Business</h4><ul><li><a href="brand-scaling.html">Brand Scaling</a></li><li><a href="companies.html">Companies</a></li><li><a href="pricing.html">Pricing</a></li></ul></div>
  <div><h4>Agency</h4><ul><li><a href="work.html">Work</a></li><li><a href="about.html">About</a></li><li><a href="apply.html">Apply</a></li><li><a href="contact.html">Contact</a></li><li><a href="privacy.html">Privacy</a></li></ul></div>
</div><div class="foot-bottom"><div class="wrap">&copy; <span id="yr"></span> SOLO Agency. Talent management and brand growth, under one roof.</div></div></footer>
<script>document.getElementById("yr").textContent=new Date().getFullYear();</script>'''

def page(fn, title, desc, body, cur=None, og=None):
    og = og or title
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(og)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@1,500&family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css?v=4">
</head>
<body>
{header(cur or fn)}
<main>
{body}
</main>
{footer()}
<script src="assets/main.js?v=1" defer></script>
</body>
</html>
'''
    open(os.path.join(ROOT, fn), "w").write(doc)

def head(eyebrow, title, sub=""):
    return f'''<section class="page-head wrap reveal"><div class="eyebrow">{eyebrow}</div><h1>{title}</h1>{f'<p class="lead">{sub}</p>' if sub else ''}</section>'''

def cards(items, cols="g2", gold=True, numbered=False):
    out = f'<div class="grid {cols}">'
    for it in items:
        out += f'<div class="card reveal">{icon(it[0], gold=gold)}<h3>{it[1]}</h3><p>{it[2]}</p></div>'
    return out + "</div>"

def steps(items, goldnum=False):
    out = '<div class="grid g4">'
    for i,(t,b) in enumerate(items):
        out += f'<div class="card reveal"><div class="num{" gold" if goldnum else ""}">0{i+1}</div><h3>{t}</h3><p>{b}</p></div>'
    return out + "</div>"

def faq(items):
    return '<div class="faq">' + "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in items) + '</div>'

def cta(title, sub="", primary_label="Apply", primary_href="apply.html", secondary=("Contact","contact.html")):
    sec = f'<a class="btn btn-ghost" href="{secondary[1]}">{secondary[0]}</a>' if secondary else ""
    return f'''<section class="section wrap" style="padding-block:40px 40px"><div class="band center reveal"><h2>{title}</h2>{f'<p class="lead" style="margin-top:12px">{sub}</p>' if sub else ''}<div class="btn-row" style="justify-content:center"><a class="btn btn-gold" href="{primary_href}">{primary_label}</a>{sec}</div></div></section>'''

def statcards(items):
    out = '<div class="grid g4">'
    for end,suf,dec,label in items:
        out += f'<div class="card reveal"><div class="stat" data-count="{end}" data-suffix="{suf}" data-dec="{dec}">{end}{suf}</div><div class="stat-label">{label}</div></div>'
    return out + "</div>"

CREATORS = [("@sturdythoughts","Uni and student life","31.6K","13M+"),("@danny_correia04","Art and entertainment","51.5K","2.6M+"),
            ("@jnr.certi","Men's lifestyle","48.9K","2.9M+"),("@dxya_x1","Fashion and beauty","72.2K","1.9M+")]
def creator_cards(n):
    out = '<div class="grid g3">'
    for h,niche,f,l in CREATORS[:n]:
        out += f'<div class="card reveal"><div class="creator"><div class="avatar"></div><div><strong style="font-family:var(--display)">{h}</strong><div class="note" style="margin:0">{niche}</div></div></div><div class="mini"><div><small>Followers</small>{f}</div><div><small>Likes</small>{l}</div></div></div>'
    return out + "</div>"

# ---------------- HOME ----------------
home = f'''
<section class="hero"><div class="wrap">
  <div class="eyebrow reveal">Models &middot; Artists &middot; Brands &middot; Companies</div>
  <h1 class="reveal">Talent, brands, and the <span class="serif">campaigns</span> that connect them.</h1>
  <p class="lead reveal">Representation for models and artists. Growth for brands and companies. <strong style="color:var(--ink);font-weight:600">Proof over pitch.</strong></p>
  <div class="btn-row reveal"><a class="btn btn-gold" href="apply.html">Apply to work with us</a><a class="btn btn-ghost" href="#divisions">See what we do</a></div>
</div></section>

<section class="section wrap" id="divisions">
  <div class="reveal" style="max-width:640px"><div class="eyebrow">Divisions</div><h2>Four divisions. One agency.</h2></div>
  <div class="grid g4" style="margin-top:44px">
    <a class="card reveal" href="models.html">{icon("users")}<h3>Models</h3><p>Mother-agency representation, casting, and portfolio development.</p><span class="more">Learn more &rarr;</span></a>
    <a class="card reveal" href="artists.html">{icon("music")}<h3>Artists</h3><p>Paid gigs, brand deals, and tour logistics.</p><span class="more">Learn more &rarr;</span></a>
    <a class="card reveal" href="brand-scaling.html">{icon("trend")}<h3>Brand Scaling</h3><p>Paid ads and creative direction for clothing brands.</p><span class="more">Learn more &rarr;</span></a>
    <a class="card reveal" href="companies.html">{icon("building")}<h3>Companies</h3><p>Content, paid ads, and HR automation.</p><span class="more">Learn more &rarr;</span></a>
  </div>
</section>

<section class="section wrap" style="padding-block:40px 72px">
  <div class="head-row reveal"><div><div class="eyebrow">Proof</div><h2>The numbers.</h2></div><a href="work.html">See full results &rarr;</a></div>
  {statcards([(1.5,"M+",1,"Views across 4 flagship videos for one client"),(20,"K",0,"Instagram followers, zero to 20K in 2 months"),(259,"",0,"Leads from 2 lead-gen campaigns we ran for our own brand"),(23.76,"%",2,"Peak lead conversion rate")])}
</section>

<section class="section wrap" style="padding-block:40px 72px">
  <div class="head-row reveal"><div><div class="eyebrow">Creator network</div><h2>A live roster.</h2></div><a href="work.html">Meet the network &rarr;</a></div>
  {creator_cards(2)}
</section>
<section class="section wrap" style="padding-block:20px 40px"><div class="band reveal" style="display:grid;gap:28px;align-items:center;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr))"><div><div class="eyebrow">The founder</div><h2 style="font-size:1.9rem">You work with the person who runs your campaign.</h2><p class="lead" style="margin-top:12px;font-size:1rem">Tommaso Cristoni has grown accounts from zero, run lead-gen campaigns end to end, and sold out a retreat with Meta ads.</p><div class="btn-row"><a class="btn btn-ghost" href="about.html">About SOLO</a><a class="btn btn-ghost" href="work.html">See the work</a></div></div></div></section>
{cta("Tell us where you are.","Every business is at a different stage. Apply and we will build a plan around yours.")}
'''
page("index.html", "SOLO Agency | Talent management and brand growth in London", "Mother-agency representation for models and artists, plus paid ads, content and digital growth for brands. London, remote-friendly.", home)

# ---------------- MODELS ----------------
models = head("Model Management","Booked, not just noticed.","Mother-agency representation: scouting, development, bookings.") + f'''
<section class="section wrap" style="padding-top:20px"><h2 class="reveal">What is included</h2><div style="margin-top:40px">{cards([
 ("camera","Show and casting bookings","Direct submissions to casting directors, never an open call."),
 ("sparkles","Paid shoot placement","Vetted editorial and commercial work, contracted before you are on set."),
 ("book","Portfolio and book development","Digitals, comp card, and web book, planned and directed by us."),
 ("briefcase","Client liaison and contract negotiation","Rates, usage rights, invoices. You focus on the work.")])}</div></section>
<section class="section wrap" style="padding-top:0"><h2 class="reveal">How it works</h2><div style="margin-top:40px">{steps([("Application and scouting","Apply or get scouted."),("Portfolio development","Digitals, test shoots, comp card."),("Active representation","Castings, shoots, shows, negotiated for you."),("Ongoing career management","Long-term strategy and market expansion.")])}</div></section>
<section class="section wrap" style="padding-top:0"><div class="band reveal"><h2 style="font-size:1.8rem">Who this is for</h2><p class="lead" style="margin-top:14px">Every level, especially models without representation. Work ethic first; height, look, and market second.</p></div></section>
<section class="section wrap narrow" style="padding-top:0"><h2 class="reveal">Common questions</h2><div style="margin-top:24px">{faq([
 ("Do I need a portfolio already?","No. Many models we sign start with phone digitals. Portfolio development is part of the process."),
 ("Is there a fee to apply?","Applying is always free. We are commission-based, so we earn when you earn."),
 ("What areas do you book in?","London-based, booking UK-wide with placements into European markets."),
 ("How do payments work?","SOLO invoices the client, deducts commission, and pays you out with a full breakdown.")])}</div></section>
''' + cta("Ready to apply for representation?","", "Apply for representation", apply_url("Model"), ("Or contact us","contact.html"))
page("models.html","Models | SOLO Agency mother-agency representation","Mother-agency representation for models: casting bookings, paid shoots, portfolio development, and contract negotiation.", models)

# ---------------- ARTISTS ----------------
artists = head("Artist Management","Less admin. More stages.","Booking and brand management for musicians and performers.") + f'''
<section class="section wrap" style="padding-top:20px"><h2 class="reveal">What is included</h2><div style="margin-top:40px">{cards([
 ("mic","Paid gig booking","Festivals, headline sets, venues, with contracts and deposits handled."),
 ("briefcase","Brand deal negotiation","Rates, usage, and exclusivity negotiated to match your reach."),
 ("star","Opening-show placement","Support slots with touring artists that fit your sound."),
 ("plane","Tour and travel logistics","Routing, travel, backline, per-diems, coordinated end to end.")])}</div></section>
<section class="section wrap" style="padding-top:0"><h2 class="reveal">How it works</h2><div style="margin-top:40px">{steps([("Discovery","We listen to the music, review your live footage, and map audience and market."),("Booking pipeline setup","Rider, one-sheet, and outreach targets defined."),("Active bookings and deals","Ongoing gig and brand outreach with contract negotiation."),("Tour support","Full logistics coordination when a run of dates is on.")])}</div></section>
<section class="section wrap" style="padding-top:0"><div class="reveal"><div class="eyebrow">Artists on the roster</div><h2>The artists we represent.</h2></div>
<div class="grid g3" style="margin-top:36px"><a class="card reveal" href="https://open.spotify.com/track/3gPPdMcV8HIvZsWk2pVEbT" target="_blank" rel="noopener"><div class="creator"><div class="avatar"></div><div><strong style="font-family:var(--display)">thaticekidd</strong><div class="note" style="margin:0">Rap and hip-hop</div></div></div><div class="mini"><div><small>Debut album</small>ICEMANN</div><div><small>Location</small>Birmingham, UK</div></div><span class="more">Listen on Spotify &rarr;</span></a></div></section>
<section class="section wrap narrow" style="padding-top:0"><h2 class="reveal">Common questions</h2><div style="margin-top:24px">{faq([
 ("What genres and types of artists do you work with?","Genre-agnostic. We look for an active release cadence and a growing live audience."),
 ("Do you take a commission?","Yes. We take an agreed share of booked gigs and negotiated brand deals, set out clearly in your contract before you sign anything."),
 ("Can you help with an upcoming tour specifically?","Yes. Send us your dates and we will scope routing, opening slots, and travel as a standalone engagement.")])}</div></section>
''' + cta("Get booked.","", "Apply as an artist", apply_url("Artist or musician"), ("Contact us","contact.html"))
page("artists.html","Artists | SOLO Agency booking and brand management","Paid gig booking, brand deal negotiation, opening-show placement, and tour logistics for artists.", artists)

# ---------------- BRAND SCALING ----------------
brand = head("Brand Scaling","Paid ads for clothing brands.","Ads, creative, and reporting, measured on results rather than impressions.") + f'''
<section class="section wrap" style="padding-top:20px"><h2 class="reveal">What is included</h2><div style="margin-top:40px">{cards([
 ("target","Paid Meta and social ads","Full-funnel Meta Ads management, measured on cost per lead and return on ad spend."),
 ("palette","Creative direction","Ad concepts, hooks, and scripts built for the feed. You film simple clips on your phone, we direct, edit and launch them."),
 ("chart","Campaign optimisation","Weekly cycles: cut underperformers, scale winners."),
 ("users","Audience segmentation and testing","Structured A/B tests across audiences, hooks, and placements.")], gold=False)}</div></section>
<section class="section wrap" style="padding-top:0"><div class="band reveal"><div class="eyebrow">Meta Ads results from our own lead-gen campaigns</div>
<h2>259 leads. 23.76% peak conversion. Best cost per lead of &pound;2.34.</h2>
<div class="grid g3" style="margin-top:34px"><div><div class="stat" data-count="259" data-dec="0">259</div><div class="stat-label">Leads across 2 Meta campaigns</div></div><div><div class="stat" data-count="23.76" data-suffix="%" data-dec="2">23.76%</div><div class="stat-label">Peak lead conversion rate</div></div><div><div class="stat">&pound;2.89 to &pound;2.96</div><div class="stat-label">Blended cost per lead, 162K+ impressions</div></div></div>
<p class="note">These campaigns were run for our own brand, Final Judgment. Every client is different, so we never promise the same numbers.</p></div></section>
<section class="section wrap" style="padding-top:0"><h2 class="reveal">Our process</h2><div style="margin-top:40px">{steps([("Discovery call","Goals, margins, offer, and current channel mix."),("Strategy and audience research","Persona work, competitor teardown, hook and offer angles."),("Campaign launch","Account build, pixel and conversion tracking, creative, structured launch."),("Ongoing optimisation","Weekly reporting, creative refresh, and a scale plan.")], True)}</div></section>
''' + cta("Ready to scale?","Tell us where your brand is today and we will tell you honestly if we can help.", "Apply", apply_url("Clothing or product brand"), ("See how pricing works","pricing.html"))
page("brand-scaling.html","Brand Scaling | Paid Meta ads for clothing brands | SOLO Agency","Paid Meta ads and creative direction for clothing brands ready to scale.", brand)

# ---------------- COMPANIES ----------------
companies = head("For Companies","Full digital presence for businesses.","Social, content, and the HR automation behind it.") + f'''
<section class="section wrap" style="padding-top:20px"><h2 class="reveal">Services</h2><div style="margin-top:40px">{cards([
 ("clipboard","Campaign management and contracts","Briefs, contracts, usage rights, deliverables, handled end to end."),
 ("camera","Content production and direction","Direction and editing built for each platform."),
 ("megaphone","Paid Meta ads amplification","Best-performing organic content, amplified with Meta Ads."),
 ("bar","Reporting and performance tracking","Monthly dashboards: reach, engagement, cost per lead, revenue."),
 ("bot","HR chatbot automation","An AI chatbot trained on your HR policy: leave requests, FAQs, onboarding.")], "g3", gold=False)}</div></section>
<section class="section wrap" style="padding-top:0"><div class="band reveal"><div class="eyebrow">Featured</div><h2>Numbers from client work.</h2>
<div class="grid g2" style="margin-top:34px"><div><div class="stat" data-count="1.5" data-suffix="M+" data-dec="1">1.5M+</div><div class="stat-label">Views across 4 flagship videos, one client</div></div><div><div class="stat" data-count="20" data-suffix="K" data-dec="0">20K</div><div class="stat-label">Followers, zero to 20K in two months</div></div></div>
<div class="eyebrow" style="margin-top:34px;color:var(--muted)">Clients</div><div class="chips"><span class="chip">Royal Mail</span><span class="chip">Luvvette</span><span class="chip">POCUS Frimley</span></div></div></section>
''' + cta("Find out what a partnership looks like for you.","There is no price list. We build the plan around your business.", "Apply", apply_url("Company or service business"), ("How pricing works","pricing.html"))
page("companies.html","Companies | Full digital presence and HR chatbot | SOLO Agency","Campaign management, content production, paid ads, reporting, and HR chatbot automation for businesses.", companies)

# ---------------- WORK (case studies) ----------------
gal = [("influencers-portfolio.jpg","Creator network overview"),("results-analytics.jpg","Meta Ads analytics dashboard"),("results-growth.jpg","Instagram growth, 0 to 20K"),("client-sample-videos.jpg","Short-form video content samples")]
tt = [("7458033527137832224","652K","tt-1"),("7457654119650692385","401K","tt-2"),("7460706638161349920","329K","tt-3"),("7458677421143870753","116K","tt-4")]
tt_html = "".join(f'<a class="tt-card reveal" href="https://www.tiktok.com/@luvvettefashion/video/{v}" target="_blank" rel="noopener" aria-label="Watch the {n} view TikTok on TikTok"><img src="assets/img/tiktok/{i}.jpg?v=2" alt="Luvvette TikTok with {n} views" width="540" height="960" loading="lazy"><span class="tt-meta"><em>Watch on TikTok &rarr;</em></span></a>' for v,n,i in tt)
pp_imgs = [("group.jpg","Purpose Path retreat group on a guided walk"),("venue.jpg","The retreat venue in the hills above M&aacute;laga"),("guided-walk.jpg","Coaching session on a guided walk"),("sound-bath.jpg","Breathwork and sound bath room set up"),("dinner.jpg","Retreat guests at dinner")]
pp_gal = "".join(f'<figure class="{"g-main" if i==0 else ""}"><img src="assets/img/purpose-path/{f}" alt="{c}" loading="lazy"></figure>' for i,(f,c) in enumerate(pp_imgs))
vids = "".join(f'<div class="vid reveal"><video controls playsinline preload="metadata"><source src="assets/video/final-judgment-0{i}.mp4" type="video/mp4"></video></div>' for i in (1,2,3))
work = head("Work","Live work, real numbers.","Case studies from client work and from our own brand. Every figure comes from an active or recent engagement.") + f"""
<section class="section wrap" style="padding-top:20px">{statcards([(1.5,"M+",1,"Views across 4 flagship videos (Luvvette)"),(20,"K",0,"Instagram followers, zero to 20K in 2 months (Luvvette)"),(44,"",0,"Leads from two retreat lead-gen campaigns (Purpose Path)"),(259,"",0,"Leads from 2 Meta campaigns (our own brand)")])}
<div class="chips reveal" style="margin-top:26px"><a class="chip" href="#purpose-path">Purpose Path</a><a class="chip" href="#luvvette">Luvvette</a><a class="chip" href="#keiran">Keiran McRae</a><a class="chip" href="#final-judgment">Final Judgment</a></div></section>

<section class="section wrap" id="purpose-path" style="padding-top:0"><div class="reveal"><div class="eyebrow">Case study 01</div><h2>Purpose Path</h2><p class="lead" style="margin-top:10px">Coaching and walking retreat &middot; M&aacute;laga, Spain &middot; Sep 2026 onwards</p></div>
<div class="grid g4" style="margin-top:34px">
<div class="card reveal"><div class="stat">100%</div><div class="stat-label">Remaining places booked on the October retreat</div></div>
<div class="card reveal"><div class="stat" data-count="44" data-dec="0">44</div><div class="stat-label">Leads from two lead-gen campaigns</div></div>
<div class="card reveal"><div class="stat">&euro;10.91</div><div class="stat-label">Blended cost per lead</div></div>
<div class="card reveal"><div class="stat" data-count="2651" data-dec="0">2,651</div><div class="stat-label">Landing page views at &euro;0.08 each</div></div></div>
<div class="grid g3 gallery pp-gallery" style="margin-top:30px">{pp_gal}</div>
<h3 class="reveal" style="font-size:1.7rem;margin-top:44px;max-width:760px">Selling out a high-ticket retreat with a focused Meta funnel.</h3>
<div class="grid g2" style="margin-top:26px">
<div class="card reveal"><div class="eyebrow">Overview</div><p>Purpose Path is a four-day coaching and walking retreat in the hills above M&aacute;laga, run by three coaches. With the October 2026 retreat approaching and places still open, they brought us in on a one-month trial to close the gap before the booking deadline.</p></div>
<div class="card reveal"><div class="eyebrow">The problem</div><p>Their Instagram was building trust, but organic reach alone was not filling a &euro;2,599 retreat in time. There was no paid acquisition, no landing page for cold traffic, and no system for tracking which leads turned into founder calls and bookings.</p></div></div>
<div class="card reveal" style="margin-top:22px"><div class="eyebrow">The solution</div><ul class="ticks">
<li><strong>Two Meta campaigns:</strong> a traffic campaign sending cold audiences to a dedicated landing page, and a lead-form campaign booking discovery calls.</li>
<li><strong>Four creative angles:</strong> the three coaches, a creator&rsquo;s UGC testimonial, a price-to-value reframe, and a final-week scarcity push. Weak concepts were paused and budget moved to the winners.</li>
<li><strong>Tight targeting:</strong> 35 to 60 year olds across the UK, Ireland and English-speaking Europe interested in coaching, leadership and wellness, plus a warm retargeting pool of profile visitors and engagers.</li>
<li><strong>Dedicated landing page:</strong> built and hosted for cold traffic, so no changes were needed on the client&rsquo;s own site.</li>
<li><strong>Lead tracking:</strong> every enquiry logged in a shared tracker within 24 hours, measured on attended founder calls and confirmed bookings, not clicks.</li></ul></div>
<div class="ads-table-wrap reveal"><p class="note" style="margin:26px 0 10px;text-transform:uppercase;letter-spacing:.08em">Campaign results from Meta Ads Manager, amounts in euros</p><div class="tbl-scroll"><table class="tbl"><thead><tr><th>Campaign</th><th>Spend</th><th>Results</th><th>Cost / result</th><th>Impressions</th><th>Reach</th></tr></thead><tbody>
<tr><td>October retreat &middot; Traffic to landing page</td><td>&euro;218.65</td><td>2,651 landing page views</td><td>&euro;0.08</td><td>74,996</td><td>55,877</td></tr>
<tr><td>October retreat &middot; Discovery call lead form</td><td>&euro;249.99</td><td>26 leads</td><td>&euro;9.62</td><td>7,790</td><td>5,015</td></tr>
<tr class="total"><td>April 2027 retreat &middot; Lead form (live)</td><td>&euro;230.00</td><td>18 leads</td><td>&euro;12.78</td><td>5,496</td><td>3,556</td></tr></tbody></table></div>
<p class="note">October campaigns: reporting window 16 Sep to 15 Oct 2026, ended 3 Oct. April 2027 campaign: running since 18 Oct, figures to 1 Nov 2026 and still updating.</p></div>
<div class="band reveal" style="margin-top:26px;padding:26px 30px"><div class="eyebrow">The result</div><p style="font-size:1.05rem">Every remaining place on the October retreat booked ahead of the retreat dates. The follow-on April 2027 campaign is live and has already generated 18 form leads at &euro;12.78 each.</p></div>
<!-- PURPOSE PATH TESTIMONIALS: two slots reserved. Fill in text, name and role, then delete the hidden attribute on .case-quotes and each figure you use. -->
<div class="case-quotes" hidden><div class="eyebrow" style="margin-top:30px">In their words</div><div class="grid g2">
<figure class="card pp-quote" hidden><blockquote>&ldquo;Testimonial one goes here.&rdquo;</blockquote><figcaption><strong>Name</strong><br><span class="note">Role, Purpose Path</span></figcaption></figure>
<figure class="card pp-quote" hidden><blockquote>&ldquo;Testimonial two goes here.&rdquo;</blockquote><figcaption><strong>Name</strong><br><span class="note">Role, Purpose Path</span></figcaption></figure></div></div></section>

<section class="section wrap" id="luvvette" style="padding-top:0"><div class="reveal"><div class="eyebrow">Case study 02</div><h2>Luvvette</h2><p class="lead" style="margin-top:10px">Social media management across TikTok and Instagram. Content planning, production and distribution for a fashion brand.</p></div>
<div class="grid g4" style="margin-top:34px"><div class="card reveal"><div class="stat" data-count="1.5" data-suffix="M+" data-dec="1">1.5M+</div><div class="stat-label">Combined views across 4 flagship TikToks</div></div><div class="card reveal"><div class="stat" data-count="20" data-suffix="K" data-dec="0">20K</div><div class="stat-label">Instagram followers, grown from 0 in 2 months</div></div><div class="card reveal"><div class="stat" data-count="24.6" data-suffix="K" data-dec="1">24.6K</div><div class="stat-label">Total TikTok likes across 52 videos</div></div><div class="card reveal"><div class="stat">4</div><div class="stat-label">Viral videos, each 100K+ views</div></div></div>
<div class="grid g4 tt-grid" style="margin-top:30px">{tt_html}</div>
<div class="btn-row"><a class="btn btn-ghost" href="https://www.tiktok.com/@luvvettefashion" target="_blank" rel="noopener">Luvvette on TikTok</a><a class="btn btn-ghost" href="https://www.instagram.com/luvvetteofficial/" target="_blank" rel="noopener">Luvvette on Instagram</a></div></section>

<section class="section wrap" id="keiran" style="padding-top:0"><div class="reveal"><div class="eyebrow">Case study 03</div><h2>Keiran McRae</h2><p class="lead" style="margin-top:10px">@sturdythoughts &middot; from 3,247 to 31.6K followers and 13M+ likes, with real brand partnerships including StockX and McDonald&rsquo;s secured through the account.</p></div>
<div class="grid g2 center-items" style="margin-top:34px"><div class="vid reveal" style="max-width:340px;margin-inline:auto"><video controls playsinline preload="metadata"><source src="assets/video/keiran-testimonial.mp4" type="video/mp4"></video></div>
<div class="card reveal"><blockquote style="margin:0;font-size:1.05rem;color:var(--ink)">&ldquo;I&rsquo;ve been working with SOLO for the last six months. He&rsquo;s been helping me grow my following, monetise my brand, and scale my content. SOLO gave me the system to actually monetise my personal brand, to get to a place where I&rsquo;m able to consistently get brand deals and earn from coaching products.&rdquo;</blockquote>
<p style="margin-top:18px"><strong>Keiran McRae</strong><br><span class="note">@sturdythoughts, creator</span></p>
<div class="mini" style="margin-top:18px"><div><small>Followers, from 3.2K</small>31.6K</div><div><small>Total likes</small>13M+</div></div>
<div class="chips"><span class="chip">StockX partnership</span><span class="chip">McDonald&rsquo;s partnership</span></div></div></div></section>

<section class="section wrap" id="final-judgment" style="padding-top:0"><div class="reveal"><div class="eyebrow">Our own brand</div><h2>Final Judgment</h2><p class="lead" style="margin-top:10px">A streetwear label founded and creative-directed end to end: a dark, gothic-script apocalyptic brand world built into hoodies, shot as street-style content, and turned into a paid lead-gen engine.</p></div>
<div class="grid g3 fj-grid" style="margin-top:34px">{vids}</div>
<p class="note reveal">Street-style lookbook content shot on location: the Final Judgement wordmark and leopard-print trim on black hoodies, cut against moody macro inserts and scripture-style overlays.</p>
<div class="reveal" style="margin-top:44px"><div class="eyebrow">Paid social</div><h3 style="font-size:1.6rem">Meta Ads performance</h3><p class="lead" style="margin-top:8px">Lead-generation campaigns built, tested and optimised end to end in Meta Ads Manager: audience segmentation, creative testing and budget allocation across ad sets.</p></div>
<div class="grid g4" style="margin-top:26px"><div class="card reveal"><div class="stat" data-count="259" data-dec="0">259</div><div class="stat-label">Leads across two lead-gen campaigns</div></div><div class="card reveal"><div class="stat" data-count="2.92" data-dec="2">2.92</div><div class="stat-label">Blended cost per lead in &pound;, best ad set &pound;2.34</div></div><div class="card reveal"><div class="stat" data-count="22" data-suffix="%+" data-dec="0">22%+</div><div class="stat-label">Average lead conversion rate</div></div><div class="card reveal"><div class="stat" data-count="162" data-suffix="K+" data-dec="0">162K+</div><div class="stat-label">Impressions delivered</div></div></div>
<div class="ads-table-wrap reveal"><p class="note" style="margin:26px 0 10px;text-transform:uppercase;letter-spacing:.08em">Ad set breakdown, live export from Meta Ads Manager</p><div class="tbl-scroll"><table class="tbl"><thead><tr><th>Amount spent</th><th>Results</th><th>Cost / result</th><th>Conv. rate (leads)</th><th>Impressions</th><th>Reach</th></tr></thead><tbody>
<tr><td>&pound;11.19</td><td>4</td><td>&pound;2.80</td><td>20.00%</td><td>2,383</td><td>1,527</td></tr>
<tr><td>&pound;84.19</td><td>29</td><td>&pound;2.90</td><td>25.22%</td><td>18,831</td><td>7,416</td></tr>
<tr><td>&pound;87.08</td><td>26</td><td>&pound;3.35</td><td>21.85%</td><td>19,868</td><td>7,979</td></tr>
<tr><td>&pound;51.18</td><td>15</td><td>&pound;3.41</td><td>18.29%</td><td>12,145</td><td>5,557</td></tr>
<tr><td>&pound;68.90</td><td>22</td><td>&pound;3.13</td><td>17.89%</td><td>15,145</td><td>6,963</td></tr>
<tr><td>&pound;112.20</td><td>48</td><td>&pound;2.34</td><td>22.64%</td><td>24,899</td><td>9,384</td></tr>
<tr class="total"><td>&pound;416.74</td><td>144</td><td>&pound;2.89</td><td>21.46%</td><td>93,533</td><td>15,895</td></tr></tbody></table></div>
<p class="note">Second campaign (not shown row by row): 115 leads &middot; &pound;2.96 cost per lead &middot; 23.76% conversion &middot; 69,048 impressions &middot; 20,186 reach. These campaigns were run for our own brand, so we never promise the same numbers for a client.</p></div></section>

<section class="section wrap" style="padding-top:0"><div class="reveal"><div class="eyebrow">Clients</div><h2>Brands and businesses we have worked with.</h2></div>
<div class="chips reveal" style="margin-top:26px"><span class="chip">Royal Mail</span><span class="chip">Luvvette</span><span class="chip">Purpose Path</span><span class="chip">POCUS Frimley</span></div></section>
<section class="section wrap" style="padding-top:0"><div class="reveal"><div class="eyebrow">Creator network</div><h2>4 active creators, 204.2K+ combined followers, 20.4M+ combined likes.</h2></div><div style="margin-top:36px">{creator_cards(4)}</div></section>
<section class="section wrap" style="padding-top:0"><div class="reveal"><div class="eyebrow">Portfolio</div><h2>Campaign and analytics gallery.</h2></div>
<div class="grid g3 gallery" style="margin-top:36px">{"".join(f'<figure class="reveal"><img src="assets/img/{f}" alt="{c}" loading="lazy" width="800" height="600"><figcaption>{c}</figcaption></figure>' for f,c in gal)}</div></section>
""" + cta("Want results like these?","Apply and tell us where you are today.")
page("work.html","Work | Case studies, results and creators | SOLO Agency","Case studies and real numbers: Purpose Path retreat lead-gen, Luvvette 1.5M+ views and 20K followers, Keiran McRae 13M+ likes, and Final Judgment Meta Ads results.", work)
# old results.html now redirects
open(os.path.join(ROOT,"results.html"),"w").write('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=work.html"><link rel="canonical" href="work.html"><title>Work | SOLO Agency</title></head><body><a href="work.html">Continue to our work</a></body></html>')

# ---------------- ABOUT ----------------
tl = [("Growth Marketing Consultant","Purpose Path","Sep 2026 to present","Coaching and walking retreat, M&aacute;laga, Spain",["Built and ran the retreat&rsquo;s Meta Ads campaigns end to end: targeting, ad creative, and a dedicated landing page.","Booked out every remaining space on the October 2026 retreat, and generated 44 leads at a &euro;10.91 blended cost per lead across two lead-gen campaigns."]),
      ("Talent Manager","thaticekidd and Madellina","Jul 2026 to present","Independent artist management",["Manage two independent creators end to end: bookings, content direction and career growth.","Secured a paid live show booking for thaticekidd."]),
      ("Social Media Manager","Luvvette","Sep 2023 to Feb 2025","Client account, managed via SAVED Marketing",["Owned social media management across TikTok and Instagram, from content planning to publishing.","Produced four flagship TikTok videos totalling 1.5M+ views and grew Instagram to 20K+ followers."]),
      ("Founder and Director","SAVED Marketing","Sep 2023 to Feb 2025","Digital marketing company for fashion and lifestyle clients",["Delivered social-first content and brand campaigns for clients including Luvvette and Royal Mail.","Directed and produced photoshoots across London studios and Canary Wharf."]),
      ("CEO and Creative Director","Final Judgment","Sep 2023 to present","Streetwear label",["Direct short-form video and editorial content across Instagram and TikTok.","Run paid social campaigns in Meta Ads Manager with A/B testing and audience segmentation."])]
tl_html = "".join(f'<div class="tl-item reveal"><div class="tl-top"><h3>{t} <span>{o}</span></h3><span class="note">{d}</span></div><p class="note" style="margin:4px 0 8px">{r}</p><ul class="ticks">' + "".join(f"<li>{x}</li>" for x in b) + '</ul></div>' for t,o,d,r,b in tl)
about = head("About","Built by a founder who runs the campaigns.","SOLO is run by Tommaso Cristoni. You work with the person who plans, builds and reports on your campaign.") + f"""
<section class="section wrap" style="padding-top:20px"><div class="grid g2 center-items"><div class="reveal"><img class="founder" src="assets/img/founder.jpg" alt="Tommaso Cristoni" width="768" height="1024" loading="lazy"></div>
<div class="reveal"><div class="eyebrow">Founder</div><h2 style="font-size:2rem">Tommaso Cristoni</h2><p class="lead" style="margin-top:14px;font-size:1rem">London-based. I have grown accounts from zero, directed shoots from concept to delivery, and turned single posts into 1.5M+ views. Today I run SOLO: talent management for artists and creators, and paid social growth for brands and businesses.</p>
<p class="note" style="margin-top:14px">BSc Business Management, University of Birmingham (2026). Languages: English and Italian (native), Spanish (professional).</p>
<div class="btn-row"><a class="btn btn-gold" href="apply.html">Apply to work with us</a><a class="btn btn-ghost" href="work.html">See the work</a></div></div></div></section>
<section class="section wrap narrow" style="padding-top:0"><div class="reveal"><div class="eyebrow">Experience</div><h2>What I have built.</h2></div><div class="timeline" style="margin-top:34px">{tl_html}</div></section>
<section class="section wrap" style="padding-top:0"><div class="reveal"><div class="eyebrow">Toolkit</div><h2>Skills and tools.</h2></div><div class="grid g4" style="margin-top:30px">
<div class="card reveal"><h3 style="font-size:1rem">Social and content</h3><p>Social media management, content creation, shoot direction, trend analysis, content distribution.</p></div>
<div class="card reveal"><h3 style="font-size:1rem">Paid and performance</h3><p>Meta Ads Manager, TikTok Creative Center, A/B testing, audience segmentation, ROAS optimisation.</p></div>
<div class="card reveal"><h3 style="font-size:1rem">Platforms and tools</h3><p>Shopify, Salesforce, HubSpot, advanced Excel, AI trend forecasting.</p></div>
<div class="card reveal"><h3 style="font-size:1rem">Languages</h3><p>Italian (native), English (native), Spanish (professional).</p></div></div></section>
""" + cta("Let's talk about your business.","Tell us where you are and we will tell you honestly if we can help.")
page("about.html","About | Tommaso Cristoni, founder of SOLO Agency","Meet the founder of SOLO Agency: experience in social media management, Meta Ads, talent management and creative direction.", about)

# ---------------- PRICING ----------------
pricing = f'''
<section class="page-head wrap reveal"><div class="eyebrow">Pricing</div><h1>Pricing that grows with you.</h1>
<p class="lead">There is no price list. What we charge depends on where your business is today and where you want to take it. We plan to work with you for years, so we set terms that fit your stage and grow as you do.</p>
<div class="btn-row" style="justify-content:center"><a class="btn btn-gold" href="apply.html">Tell us where you are</a></div></section>

<section class="section wrap" style="padding-top:30px"><div class="reveal"><div class="eyebrow">Our approach</div><h2>How we work out the fee</h2></div>
<div style="margin-top:36px">{cards([("trend","Your stage","Pre-revenue, early, growing, or scaling. We meet you where you are and only take on what we can move."),
 ("money","Your revenue and profit","Our fee is tied to what the business actually earns, so an early-stage brand is never priced out and a larger one is never underserved."),
 ("target","Your goals","We agree what success looks like first, then scope the work around it.")], "g3", gold=False)}</div></section>

<section class="section wrap" style="padding-top:0"><div class="reveal"><div class="eyebrow">Options</div><h2>Ways we can work together</h2></div>
<div style="margin-top:36px">{cards([("briefcase","Fixed monthly fee","A set monthly fee agreed from your revenue, reviewed as you grow."),
 ("share","Share of results","A share of the revenue or profit we help you generate. Ideal when cash is tight early on."),
 ("sparkles","A mix of both","A smaller fixed fee plus a share, so we are rewarded when you win.")], "g3")}</div>
<p class="note reveal" style="margin-top:22px">For artists, models and creators we take an agreed share of what we help you earn, set out clearly in your contract. We walk you through it on your first call.</p></section>

<section class="section wrap" style="padding-top:0"><div class="band reveal"><h2 style="font-size:1.9rem">What stays the same</h2>
<div class="grid g2" style="margin-top:24px"><p><strong>Ad spend is yours.</strong><br><span class="note">Always paid directly to Meta, in your own name.</span></p><p><strong>You own everything.</strong><br><span class="note">Your accounts, content and data stay yours.</span></p>
<p><strong>Clear terms.</strong><br><span class="note">Written terms before we start, with a short initial term.</span></p><p><strong>Honest reporting.</strong><br><span class="note">Monthly reports, and we revisit the fee against the results.</span></p></div></div></section>

<section class="section wrap narrow" style="padding-top:0"><h2 class="reveal">Common questions</h2><div style="margin-top:24px">{faq([
 ("Is ad spend included?","No. Ad spend is paid directly to Meta from your own account and is never marked up. Our fee covers strategy, creative, editing and management."),
 ("Can I start small?","Yes. Many of the businesses we work with are early stage. Tell us what you can comfortably invest and we will build around it."),
 ("How do you decide the fee?","From your application and a short call. We look at where your business is, its revenue and profit, and your goals, then propose terms that make sense for both sides."),
 ("Do I need to share my numbers?","Rough ranges on the form are enough. We go through detail on the call, in confidence."),
 ("What is the contract length?","A short initial term agreed in writing, then month to month."),
 ("Is it right for me?","The best way to find out is to apply. It takes two minutes.")])}</div></section>
''' + cta("Not sure where you fit?","Apply and we will tell you honestly.", "Apply now")
page("pricing.html","Pricing that grows with you | SOLO Agency","No fixed price list. SOLO Agency builds its fee around your stage, revenue, profit and goals, so early-stage businesses are never priced out.", pricing)

# ---------------- JOIN ----------------
join = head("Creator Network","Deals for uni students and fashion creators.","Paid campaigns, gifted product, and referral perks. No cold pitching.") + f'''
<section class="section wrap" style="padding-top:20px">{cards([("gift","Gifted partnerships","Free product from brand partners in exchange for content."),("money","Paid campaigns","Flat-fee and revenue-share campaigns, matched to your niche."),("share","Referral perks","Discount codes and affiliate links that pay a cut of every sale.")], "g3")}</section>
<section class="section wrap" style="padding-top:0"><h2 class="reveal">How to apply</h2><div style="margin-top:40px">{steps([("Apply","Send us your handles, niche, and audience. It takes two minutes."),("Review","We check fit against active brand briefs and audience overlap."),("Onboard","Sign our creator agreement: non-exclusive, no lock-in."),("Get matched","You start seeing paid and gifted campaigns matched to your niche.")])}</div></section>
''' + cta("Apply to join the network.","", "Apply to join", apply_url("Creator or influencer"), ("Or contact us","contact.html"))
page("join.html","Join the Network | Deals for uni students and fashion creators | SOLO","Paid brand campaigns, gifted product runs, and referral perks for uni students and fashion creators.", join)

# ---------------- CONTACT ----------------
contact = head("Get in touch","Talent, brand, or company. Let's talk.","Brands and companies: apply and we will set up a short call. Talent: apply for representation.") + f'''
<section class="section wrap" style="padding-top:20px"><div class="grid g2">
<div class="card reveal" style="border-color:rgba(217,169,63,.5);background:linear-gradient(135deg,rgba(217,169,63,.1),#fff 60%,var(--sky-soft))">{icon("sparkles", gold=True)}<h3 style="font-size:1.6rem">Fastest way in: apply</h3><p>Two minutes. We read every application and reply within 2 business days.</p><div class="btn-row"><a class="btn btn-gold" href="apply.html">Apply now</a></div></div>
<div class="card reveal">{icon("mail", gold=False)}<h3 style="font-size:1.6rem">Email us</h3><p>A brief, a portfolio, or a single question. Send anything.</p><div class="btn-row"><a class="btn btn-ghost" href="mailto:{EMAIL}">{EMAIL}</a></div><p class="note" style="margin-top:28px">London, UK &middot; Remote-friendly</p></div></div></section>
<section class="section wrap narrow" style="padding-top:0"><div class="reveal"><div class="eyebrow">Or send us a note</div><h2>Tell us what you need.</h2><p class="lead" style="margin-top:10px">We reply within 1 to 2 business days.</p></div>
<form class="form-card reveal" id="contactForm" style="margin-top:34px" novalidate>
<label class="field" for="c-name">Name<input id="c-name" name="name" type="text" autocomplete="name" required></label>
<label class="field" for="c-email">Email<input id="c-email" name="email" type="email" autocomplete="email" required></label>
<label class="field" for="c-role">I am a<select id="c-role" name="role" required><option value="">Select one</option><option>Brand or company</option><option>Model</option><option>Artist</option><option>Creator or influencer</option><option>Something else</option></select></label>
<label class="field" for="c-msg">Message<textarea id="c-msg" name="message" required placeholder="Tell us about the brief, timeline, or what you are looking for."></textarea></label>
<input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<p class="form-error" id="contactError" role="alert"></p>
<div class="form-nav" style="justify-content:flex-end"><button class="btn btn-gold" type="submit" id="contactSend">Send message</button></div>
<p class="note">Your details are used only to reply to you. See our <a href="privacy.html" style="text-decoration:underline">privacy note</a>.</p></form>
<div class="done form-card" id="contactDone"><h2 style="font-size:1.8rem">Thanks, message sent.</h2><p class="lead" style="margin-top:10px">We will reply within 1 to 2 business days.</p></div></section>
'''
page("contact.html","Contact | SOLO Agency | Talent, brands and companies","Talent, brand, or company. Apply or send us a brief. London, remote-friendly.", contact)

# ---------------- APPLY ----------------
def radios(name, opts, req=True):
    return '<div class="choices">' + "".join(f'<label class="choice"><input type="radio" name="{name}" value="{html.escape(o)}"{" required" if req else ""}><span>{o}</span></label>' for o in opts) + '</div>'
def checks(name, opts):
    return '<div class="choices">' + "".join(f'<label class="choice"><input type="checkbox" name="{name}" value="{html.escape(o)}" data-any><span>{o}</span></label>' for o in opts) + '</div>'
apply = head("Apply","Tell us where you are.","Five short steps. We read every application and reply within 2 business days. Rough answers are fine.") + f'''
<section class="section wrap narrow" style="padding-top:10px">
<form class="form-card" id="applyForm" novalidate>
<div class="progress"><span id="bar"></span></div><div class="step-count"><span id="stepCount">Step 1 of 5</span><span id="stepPct">20%</span></div>

<fieldset class="active"><legend>Who are you?</legend><p class="hint">So we know who to reply to.</p>
<label class="field" for="a-name">Full name<input id="a-name" name="name" type="text" autocomplete="name" required></label>
<label class="field" for="a-email">Email<input id="a-email" name="email" type="email" autocomplete="email" required></label>
<label class="field" for="a-phone">Phone or WhatsApp (with country code)<input id="a-phone" name="phone" type="tel" autocomplete="tel" placeholder="+44 7..." required></label>
<label class="field" for="a-biz">Business, brand or artist name<input id="a-biz" name="business" type="text" autocomplete="organization" required></label>
<label class="field" for="a-links">Website or Instagram/TikTok handle<input id="a-links" name="links" type="text" placeholder="@yourbrand or yourwebsite.com" required></label></fieldset>

<fieldset><legend>Which best describes you?</legend><p class="hint">Pick one.</p>{radios("type",["Clothing or product brand","Company or service business","Creator or influencer","Artist or musician","Model","Something else"])}</fieldset>

<fieldset><legend>Where are you right now?</legend><p class="hint">There is no wrong answer. Early stage is welcome, and rough ranges are fine.</p>
<div class="sub-q">Stage</div>{radios("stage",["Just an idea","Pre-revenue","Early, first customers","Growing steadily","Scaling"])}
<div class="sub-q">Average monthly revenue</div>{radios("revenue",["None yet","Under £1k","£1k to £5k","£5k to £20k","£20k to £50k","£50k+","Prefer to discuss"])}
<div class="sub-q">Average monthly profit</div>{radios("profit",["Not profitable yet","Break-even","Under £1k","£1k to £5k","£5k+","Not sure"])}
<div class="sub-q">Current monthly marketing spend</div>{radios("spend",["None","Under £250","£250 to £1k","£1k to £3k","£3k+"])}
<div class="sub-q">What could you comfortably invest each month to grow?</div>{radios("invest",["Not sure yet, happy to start small","Under £250","£250 to £1k","£1k to £3k","£3k+"])}</fieldset>

<fieldset><legend>What do you need?</legend><p class="hint">Pick as many as you like.</p>{checks("needs",["Meta ads","Content creation","Social media management","Website","Artist or talent management","Creator brand deals","Not sure, advise me"])}
<label class="field" for="a-block">What is the biggest thing holding you back right now?<textarea id="a-block" name="blocker" required></textarea></label>
<label class="field" for="a-goal">What would a great next 12 months look like?<textarea id="a-goal" name="goal" required></textarea></label></fieldset>

<fieldset><legend>Last bits</legend>
<div class="sub-q" style="margin-top:0">When do you want to start?</div>{radios("start",["As soon as possible","Within a month","In 1 to 3 months","Just exploring"])}
<label class="field" for="a-heard">How did you hear about us?<input id="a-heard" name="heard" type="text"></label>
<label class="consent"><input type="checkbox" name="consent" data-need required><span>I agree to SOLO Agency contacting me about my application. My details are used only for this and are never sold. See the <a href="privacy.html" style="text-decoration:underline">privacy note</a>.</span></label></fieldset>

<input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
<p class="form-error" id="formError" role="alert"></p>
<div class="form-nav" id="formNav"><button type="button" class="btn btn-ghost" id="back" style="visibility:hidden">Back</button><button type="button" class="btn btn-dark" id="next">Next</button><button type="submit" class="btn btn-gold" id="submit" hidden>Send application</button></div>
</form>
<div class="done form-card" id="done"><div class="eyebrow">Application received</div><h2>Thanks, we have it.</h2><p class="lead" style="margin-top:12px">We will read it properly and reply within 2 business days. In the meantime, have a look at our <a href="work.html" style="text-decoration:underline">results</a>.</p></div>
</section>
'''
page("apply.html","Apply | SOLO Agency","Apply to work with SOLO Agency. A quick five-step form so we can understand where you are and how we can help.", apply, "contact.html")

# ---------------- PRIVACY ----------------
privacy = head("Privacy","How we use your details.") + f'''
<section class="section wrap narrow" style="padding-top:0"><div class="card"><p>SOLO Agency is run by Tommaso Cristoni, London, UK. This note explains what we do with the details you send through this website. It is a plain-language summary, not legal advice.</p>
<h3 style="margin-top:24px">What we collect</h3><p>When you apply or contact us: your name, email, phone number, business or brand name, website or social handles, and your answers about your business (such as stage, revenue and profit ranges, what you need, and your goals).</p>
<h3 style="margin-top:24px">Why</h3><p>To understand where you are, reply to you, and decide whether and how we can work together. We do not sell your details and do not use them for unrelated marketing.</p>
<h3 style="margin-top:24px">How it is handled</h3><p>Form submissions are sent to us by email through a form service (FormSubmit). We keep applications only as long as needed to reply and to run any work that follows, and delete them on request.</p>
<h3 style="margin-top:24px">Your rights</h3><p>You can ask to see, correct or delete your details at any time by emailing <a href="mailto:{EMAIL}" style="text-decoration:underline">{EMAIL}</a>.</p></div></section>
'''
page("privacy.html","Privacy | SOLO Agency","How SOLO Agency uses the details you send through this website.", privacy)

# ---------------- 404 ----------------
nf = head("404","Page not found.","The page you are looking for does not exist.") + '<section class="wrap center" style="padding-bottom:80px"><a class="btn btn-gold" href="index.html">Back to home</a></section>'
page("404.html","Page not found | SOLO Agency","Page not found.", nf)

# sitemap + robots
base = "https://soloplaier.github.io/solo-agency/"
pages = ["index","models","artists","brand-scaling","companies","work","about","pricing","join","contact","apply","privacy"]
open(os.path.join(ROOT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{base}{p}.html</loc></url>\n" for p in pages) + "</urlset>\n")
open(os.path.join(ROOT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n")
print("built", len(pages)+1, "pages")
