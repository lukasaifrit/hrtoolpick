"""
HR Payroll Comparison Site — Page Generator
============================================
Generates comparison, alternatives, and best-for pages
from tools.json database using Jinja2 templates.

Usage:
    pip install jinja2
    python generate_pages.py

Output: /output/ folder with all HTML pages
"""

import json
import os
import itertools
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, pass_environment


# ─── CONFIG ────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent.parent
DATA_FILE   = BASE_DIR / "data" / "tools.json"
TEMPLATE_DIR = BASE_DIR / "templates"
OUTPUT_DIR  = BASE_DIR / "output"

CURRENT_YEAR  = datetime.now().year
CURRENT_MONTH = datetime.now().strftime("%B")
MONTH_NUM     = datetime.now().strftime("%m")

FEATURES_TO_COMPARE = [
    ("payroll_processing",   "Payroll processing"),
    ("tax_filing",           "Automated tax filing"),
    ("direct_deposit",       "Direct deposit"),
    ("benefits_admin",       "Benefits administration"),
    ("time_tracking",        "Time tracking"),
    ("onboarding",           "Employee onboarding"),
    ("pto_management",       "PTO management"),
    ("contractor_payments",  "Contractor payments"),
    ("international_payroll","International payroll"),
    ("mobile_app",           "Mobile app"),
    ("api_access",           "API access"),
]


# ─── JINJA2 CUSTOM FILTERS ────────────────────────────────
def star_html(rating):
    """Convert numeric rating to star emoji string."""
    full  = int(rating)
    half  = 1 if (rating - full) >= 0.4 else 0
    empty = 5 - full - half
    return "★" * full + "☆" * half + "☆" * empty

def price_display(tool):
    """Format pricing for display."""
    p = tool["pricing"]
    if p["free_plan"]:
        return "Free plan available"
    if not p["starting_price"]:
        return "Contact for pricing"
    s = f"${p['starting_price']}/mo"
    if p.get("per_employee"):
        s += f" + ${p['per_employee']}/employee"
    return s


# ─── LOGIC HELPERS ────────────────────────────────────────
def generate_verdict(a, b):
    """Auto-generate a one-line verdict comparing two tools."""
    verdicts = []

    # Pricing comparison
    pa = a["pricing"]["starting_price"]
    pb = b["pricing"]["starting_price"]
    if pa and pb:
        cheaper = a["name"] if pa < pb else b["name"]
        pricier = b["name"] if pa < pb else a["name"]
        verdicts.append(
            f"{cheaper} is more affordable for small teams starting out, "
            f"while {pricier} offers more advanced features for growing businesses."
        )
    elif pa and not pb:
        verdicts.append(
            f"{a['name']} has transparent pricing starting at ${pa}/month, "
            f"while {b['name']} requires a custom quote — better for larger organizations."
        )
    else:
        verdicts.append(
            f"Both {a['name']} and {b['name']} are strong HR platforms "
            f"targeting different business sizes and use cases."
        )

    # Global vs US
    a_global = any("+" in c or len(a["countries_supported"]) > 2 for c in a["countries_supported"])
    b_global = any("+" in c or len(b["countries_supported"]) > 2 for c in b["countries_supported"])
    if a_global and not b_global:
        verdicts.append(f"If you hire internationally, {a['name']} is the clear winner.")
    elif b_global and not a_global:
        verdicts.append(f"If you hire internationally, {b['name']} is the clear winner.")

    return " ".join(verdicts[:2])


def generate_use_cases(a, b):
    """Generate who-should-use-what scenarios."""
    cases = []

    # Price sensitivity
    pa = a["pricing"]["starting_price"]
    pb = b["pricing"]["starting_price"]
    if pa and pb and pa != pb:
        cheaper = a if pa < pb else b
        cases.append({
            "winner": cheaper["name"],
            "reason": f"You're a small team on a tight budget and want the most affordable option with solid core features."
        })

    # International
    a_intl = a["features"]["international_payroll"]
    b_intl = b["features"]["international_payroll"]
    if a_intl and not b_intl:
        cases.append({"winner": a["name"], "reason": "You have remote employees or contractors in multiple countries."})
    elif b_intl and not a_intl:
        cases.append({"winner": b["name"], "reason": "You have remote employees or contractors in multiple countries."})

    # Rating
    if a["ratings"]["g2"] > b["ratings"]["g2"]:
        cases.append({
            "winner": a["name"],
            "reason": f"User satisfaction matters most — {a['name']} holds a higher G2 rating ({a['ratings']['g2']} vs {b['ratings']['g2']})."
        })
    elif b["ratings"]["g2"] > a["ratings"]["g2"]:
        cases.append({
            "winner": b["name"],
            "reason": f"User satisfaction matters most — {b['name']} holds a higher G2 rating ({b['ratings']['g2']} vs {a['ratings']['g2']})."
        })

    # Free trial
    if a["pricing"]["free_trial"] and not b["pricing"]["free_trial"]:
        cases.append({"winner": a["name"], "reason": "You want to try before you buy — only one of them offers a free trial."})
    elif b["pricing"]["free_trial"] and not a["pricing"]["free_trial"]:
        cases.append({"winner": b["name"], "reason": "You want to try before you buy — only one of them offers a free trial."})

    # Contractor payments
    if a["features"]["contractor_payments"] and not b["features"]["contractor_payments"]:
        cases.append({"winner": a["name"], "reason": "You work with freelancers or contractors and need to pay them through the platform."})
    elif b["features"]["contractor_payments"] and not a["features"]["contractor_payments"]:
        cases.append({"winner": b["name"], "reason": "You work with freelancers or contractors and need to pay them through the platform."})

    # Fallback
    if len(cases) < 2:
        cases.append({
            "winner": a["name"],
            "reason": f"You prioritize {a['best_for'][0]} needs and value {a['pros'][0].lower()}."
        })
        cases.append({
            "winner": b["name"],
            "reason": f"You need {b['best_for'][0]} capabilities and value {b['pros'][0].lower()}."
        })

    return cases[:5]


def generate_faqs(a, b):
    """Generate FAQ section for the comparison page."""
    faqs = [
        {
            "q": f"Is {a['name']} better than {b['name']}?",
            "a": (
                f"It depends on your needs. {a['name']} is generally better for "
                f"{', '.join(a['best_for'][:2])}, while {b['name']} shines for "
                f"{', '.join(b['best_for'][:2])}. Both have strong ratings on G2 and Capterra."
            )
        },
        {
            "q": f"How much does {a['name']} cost compared to {b['name']}?",
            "a": (
                f"{price_display(a)} vs {price_display(b)}. "
                f"Always check each vendor's official pricing page as rates may have changed."
            )
        },
        {
            "q": f"Can I switch from {a['name']} to {b['name']}?",
            "a": (
                f"Yes, both platforms support data export. Most businesses complete a migration in 2–4 weeks. "
                f"It's best to run both in parallel for one payroll cycle before fully switching."
            )
        },
        {
            "q": f"Does {a['name']} or {b['name']} offer a free trial?",
            "a": (
                f"{'Yes, ' + a['name'] + ' offers a free trial.' if a['pricing']['free_trial'] else a['name'] + ' does not currently offer a free trial.'} "
                f"{'Yes, ' + b['name'] + ' offers a free trial.' if b['pricing']['free_trial'] else b['name'] + ' does not currently offer a free trial.'}"
            )
        },
        {
            "q": f"Which is better for international payroll — {a['name']} or {b['name']}?",
            "a": (
                f"{'Both support international payroll.' if a['features']['international_payroll'] and b['features']['international_payroll'] else ''}"
                f"{a['name'] + ' supports international payroll; ' + b['name'] + ' is primarily US-focused.' if a['features']['international_payroll'] and not b['features']['international_payroll'] else ''}"
                f"{b['name'] + ' supports international payroll; ' + a['name'] + ' is primarily US-focused.' if b['features']['international_payroll'] and not a['features']['international_payroll'] else ''}"
                f"{'Neither currently offers international payroll — consider Deel or Remote for global hiring.' if not a['features']['international_payroll'] and not b['features']['international_payroll'] else ''}"
            )
        },
    ]
    return faqs


# ─── PAGE GENERATORS ──────────────────────────────────────
def generate_comparison_page(env, a, b, output_dir):
    """Generate a single A vs B comparison page."""
    template    = env.get_template("comparison.html")
    total_reviews = a["ratings"]["review_count"] + b["ratings"]["review_count"]

    context = {
        "tool_a":       a,
        "tool_b":       b,
        "year":         CURRENT_YEAR,
        "month":        CURRENT_MONTH,
        "month_num":    MONTH_NUM,
        "features":     FEATURES_TO_COMPARE,
        "verdict":      generate_verdict(a, b),
        "use_cases":    generate_use_cases(a, b),
        "faqs":         generate_faqs(a, b),
        "total_reviews": f"{total_reviews:,}",
    }

    slug     = f"{a['slug']}-vs-{b['slug']}"
    page_dir = output_dir / "compare" / slug
    page_dir.mkdir(parents=True, exist_ok=True)

    html = template.render(**context)
    (page_dir / "index.html").write_text(html, encoding="utf-8")
    return slug


def generate_all_pages(tools):
    """Generate all comparison page combinations."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    env.filters["star_html"]     = star_html
    env.filters["price_display"] = price_display

    # ── Comparison pages (A vs B) ──────────────────────────
    pairs     = list(itertools.combinations(tools, 2))
    generated = []

    print(f"\n📄 Generating comparison pages ({len(pairs)} pairs)...\n")
    for a, b in pairs:
        slug = generate_comparison_page(env, a, b, OUTPUT_DIR)
        generated.append(slug)
        print(f"  ✓ /compare/{slug}/")

    # ── Sitemap ────────────────────────────────────────────
    sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for slug in generated:
        sitemap_lines.append(
            f'  <url><loc>https://yoursite.com/compare/{slug}/</loc>'
            f'<lastmod>{CURRENT_YEAR}-{MONTH_NUM}-01</lastmod>'
            f'<changefreq>monthly</changefreq><priority>0.8</priority></url>'
        )
    sitemap_lines.append('</urlset>')
    (OUTPUT_DIR / "sitemap.xml").write_text("\n".join(sitemap_lines), encoding="utf-8")

    return generated


# ─── MAIN ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 52)
    print("  HR Payroll Site — Programmatic Page Generator")
    print("=" * 52)

    with open(DATA_FILE, encoding="utf-8") as f:
        tools = json.load(f)

    print(f"\n✅ Loaded {len(tools)} tools from database")

    generated = generate_all_pages(tools)

    print(f"\n{'=' * 52}")
    print(f"  Done! Generated {len(generated)} comparison pages")
    print(f"  Output: {OUTPUT_DIR}/")
    print(f"  Sitemap: {OUTPUT_DIR}/sitemap.xml")
    print("=" * 52)
