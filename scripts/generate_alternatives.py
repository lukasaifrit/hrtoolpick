"""
HRToolPick — Alternatives Page Generator
=========================================
Generates "[Tool] alternatives" pages for top HR software tools.
These pages target high-intent buyers looking to switch tools.

Usage:
    python scripts/generate_alternatives.py
"""

import json
import os
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

BASE_DIR    = Path(__file__).parent.parent
DATA_FILE   = BASE_DIR / "data" / "tools.json"
TEMPLATE_DIR = BASE_DIR / "templates"
OUTPUT_DIR  = BASE_DIR / "output"

CURRENT_YEAR  = datetime.now().year
CURRENT_MONTH = datetime.now().strftime("%B")
MONTH_NUM     = datetime.now().strftime("%m")

# Tools to generate alternatives pages for (highest search volume)
TARGET_TOOLS = [
    "gusto", "bamboohr", "rippling", "deel", "remote",
    "adp-workforce-now", "paychex", "justworks", "paycom",
    "paycor", "workday-hcm", "ukg-pro", "hibob", "personio",
    "onpay", "zoho-people", "quickbooks-payroll", "zenefits",
    "multiplier", "oyster-hr",
]

# Color map for tool initials
COLORS = {
    "gusto": "#f04e37", "bamboohr": "#73ac39", "rippling": "#ff5c28",
    "deel": "#111", "remote": "#6c2bd9", "adp-workforce-now": "#d0021b",
    "paychex": "#005baa", "justworks": "#1f4aab", "paycom": "#00a550",
    "paycor": "#e31937", "workday-hcm": "#f36e21", "ukg-pro": "#005f9e",
    "hibob": "#7c3aed", "personio": "#1a56db", "onpay": "#2563eb",
    "zoho-people": "#e42527", "quickbooks-payroll": "#2ca01c",
    "zenefits": "#f59e0b", "multiplier": "#0ea5e9", "oyster-hr": "#0d9488",
    "adp-run": "#b91c1c", "remofirst": "#8b5cf6", "papaya-global": "#7c3aed",
    "sage-hr": "#00b050", "factorial": "#059669", "namely": "#0891b2",
    "trinet-hr": "#e11d48", "square-payroll": "#111", "wave-payroll": "#0056d2",
    "ceridian-dayforce": "#0072ce", "paylocity": "#1e40af",
    "patriot-payroll": "#dc2626", "adp-totalsource": "#991b1b",
    "keka": "#0891b2", "freshteam": "#16a34a", "lattice": "#7c3aed",
    "workable": "#d97706", "greenhouse": "#15803d", "rippling-peo": "#ea580c",
    "paychex-flex-hr": "#1d4ed8", "homebase": "#db2777",
    "borderless-ai": "#6d28d9", "velocity-global": "#0f766e",
    "bambee": "#b45309", "humi": "#0369a1", "employment-hero": "#dc2626",
    "deputy": "#4f46e5", "sprout-solutions": "#065f46",
    "sesame-hr": "#9f1239", "workforce-com": "#1e3a8a",
}

# Why choose each tool (for alternatives pages)
WHY_CHOOSE = {
    "gusto": "Best all-in-one US payroll with automated tax filing and great employee experience.",
    "bamboohr": "Excellent HRIS for US mid-market with strong onboarding and performance tools.",
    "rippling": "Unique HR+IT+Finance unified platform with 500+ integrations.",
    "deel": "Best for global hiring — pay employees and contractors in 150+ countries compliantly.",
    "remote": "Transparent pricing for global payroll with strong EOR services in 170+ countries.",
    "adp-workforce-now": "Industry veteran with deep compliance tools and global payroll for enterprises.",
    "paychex": "Trusted US payroll brand with dedicated specialist support.",
    "justworks": "Access Fortune 500-level benefits for small teams via PEO model.",
    "paycom": "Single database for all HR with employee self-service payroll verification.",
    "paycor": "Strong analytics and talent management alongside core payroll.",
    "workday-hcm": "Best-in-class HCM analytics for large enterprises needing deep workforce insights.",
    "ukg-pro": "Comprehensive HCM suite with strong workforce management for complex organizations.",
    "hibob": "Modern, employee-first HR platform with excellent engagement and culture tools.",
    "personio": "All-in-one HR built natively for European compliance and GDPR.",
    "onpay": "Highest-rated US payroll for simplicity — perfect for small teams on a budget.",
    "zoho-people": "Generous free plan and tight Zoho ecosystem integration for budget-conscious teams.",
    "quickbooks-payroll": "Seamless integration with QuickBooks accounting — zero duplicate data entry.",
    "zenefits": "Affordable all-in-one HR with benefits admin for US small businesses.",
    "multiplier": "Fast global onboarding in days with competitive EOR pricing in 150+ countries.",
    "oyster-hr": "Ethical, B-Corp certified EOR with transparent pricing across 180+ countries.",
    "adp-run": "Trusted ADP brand for very small businesses (under 50 employees).",
    "remofirst": "Most affordable global EOR at $199/employee — ideal for budget-conscious remote teams.",
    "papaya-global": "Enterprise-grade global payroll automation with deep Workday/SAP integration.",
    "sage-hr": "Modular, affordable HR for small businesses with great leave management.",
    "factorial": "Very affordable HR for European SMBs with transparent per-employee pricing.",
    "namely": "Mid-market HRIS built specifically for 50-1000 employee companies.",
    "trinet-hr": "Full PEO services with industry-specific plans for US SMBs.",
    "homebase": "Best scheduling and time tracking for hourly/shift-based businesses.",
    "paylocity": "Modern HR platform with strong employee engagement tools for growing businesses.",
    "patriot-payroll": "Cheapest full-service US payroll — perfect for micro businesses under 25 employees.",
    "workable": "Best ATS for SMBs with AI-powered candidate sourcing.",
    "lattice": "Best-in-class performance management and OKR tracking.",
    "keka": "Modern HR for Asia-Pacific businesses with strong payroll compliance.",
    "employment-hero": "Best all-in-one HR for Australian and NZ businesses.",
    "deputy": "Best shift scheduling with payroll integrations for hourly workers.",
    "bambee": "Dedicated HR manager service for small US businesses from $99/month.",
    "humi": "Built for Canadian compliance with bilingual EN/FR support.",
    "borderless-ai": "AI-powered global EOR with fast onboarding in 170+ countries.",
    "velocity-global": "Enterprise global employment platform covering 185+ countries.",
    "greenhouse": "Best structured hiring process for scaling tech companies.",
    "freshteam": "Free plan available with great ATS features for startup hiring.",
}

# Switch reasons for each tool
SWITCH_REASONS = {
    "gusto": "Common reasons include limited international payroll (US-only), pricing that increases significantly with employee count, or needing more advanced HR features beyond payroll.",
    "bamboohr": "Teams often switch due to expensive add-on pricing for payroll and performance features, limited customization, or needing stronger international hiring support.",
    "rippling": "Main reasons include high cost for smaller teams, complexity of the platform, and the lack of a free trial before committing.",
    "deel": "Users sometimes switch due to high EOR fees for larger headcounts, limited time tracking features, or preferring a platform with stronger US domestic payroll.",
    "remote": "Teams switch when they need stronger domestic US payroll features, more integrations, or find the pricing high for large international teams.",
    "adp-workforce-now": "Common complaints include outdated UI, mixed customer support experiences, steep learning curve, and complex pricing.",
    "paychex": "Users switch due to the dated interface, additional per-payroll-run fees, and customer support inconsistency.",
    "justworks": "Main reasons include US-only coverage, lack of contractor payment support, no API access, and higher cost versus alternatives.",
    "paycom": "Teams switch due to US-only coverage, quote-based pricing opacity, long implementation timelines, and steep learning curve.",
    "paycor": "Common reasons include US-only coverage, implementation fees, and customer support inconsistency reported by some users.",
    "workday-hcm": "Teams switch when they scale down or find Workday too complex and expensive for their size.",
    "ukg-pro": "Users switch due to high cost, outdated UI in some modules, and complexity for smaller organizations.",
    "hibob": "Main reasons include no built-in payroll (requires integration), higher cost versus alternatives, and limited reporting.",
    "personio": "Users switch when expanding beyond Europe or needing stronger global payroll capabilities.",
    "onpay": "Teams switch when they need stronger HR features beyond payroll, international capabilities, or more integrations.",
    "zoho-people": "Users sometimes switch when they need built-in payroll, stronger performance management, or a less complex setup.",
    "quickbooks-payroll": "Teams switch when they move away from QuickBooks accounting or need stronger HR features.",
    "zenefits": "Common reasons include past reputation concerns and limited enterprise features.",
    "multiplier": "Teams switch when needing stronger time tracking, a mobile app, or more established platform history.",
    "oyster-hr": "Users switch when needing a mobile app, stronger US domestic features, or a platform with longer track record.",
}

def generate_quick_answer(tool, alternatives):
    """Generate a quick answer summary."""
    top3 = alternatives[:3]
    names = [t["name"] for t in top3]
    return (
        f"The best {tool['name']} alternatives are {names[0]}, {names[1]}, and {names[2]}. "
        f"{names[0]} is our top pick — it offers {top3[0]['tagline'].lower()} "
        f"with a G2 rating of {top3[0]['ratings']['g2']}/5. "
        f"If you need global payroll, consider {names[1] if top3[1]['features']['international_payroll'] else names[2]}."
    )

def get_best_alternatives(tool, all_tools, count=8):
    """Get the best alternatives for a given tool."""
    others = [t for t in all_tools if t["id"] != tool["id"]]
    
    # Score each alternative by relevance
    def score(alt):
        s = 0
        s += alt["ratings"]["g2"] * 10
        # Prefer tools in similar category
        if any(c in alt["category"] for c in tool["category"]):
            s += 20
        # Prefer tools with affiliate
        if alt["affiliate"].get("link"):
            s += 15
        # Prefer tools targeting similar company size
        if tool.get("company_size") and alt.get("company_size"):
            if tool["company_size"] == alt["company_size"]:
                s += 10
        return s
    
    # Sort and return top N
    scored = sorted(others, key=score, reverse=True)
    return scored[:count]

def generate_alternatives_page(env, tool, all_tools, output_dir):
    """Generate a single alternatives page."""
    template = env.get_template("alternatives.html")
    
    alternatives = get_best_alternatives(tool, all_tools, count=8)
    
    # Build color map for alternatives
    alt_colors = {alt["slug"]: COLORS.get(alt["slug"], "#3b82f6") for alt in alternatives}
    
    # Build why_choose map
    why_choose = {alt["slug"]: WHY_CHOOSE.get(alt["slug"], alt["tagline"]) for alt in alternatives}
    
    context = {
        "tool": tool,
        "alternatives": alternatives,
        "alt_colors": alt_colors,
        "why_choose": why_choose,
        "quick_answer": generate_quick_answer(tool, alternatives),
        "switch_reason": SWITCH_REASONS.get(tool["id"], f"Common reasons include pricing, missing features, or needing better international support."),
        "year": CURRENT_YEAR,
        "month": CURRENT_MONTH,
        "month_num": MONTH_NUM,
    }
    
    # Create output directory
    page_dir = output_dir / "alternatives" / tool["slug"]
    page_dir.mkdir(parents=True, exist_ok=True)
    
    html = template.render(**context)
    (page_dir / "index.html").write_text(html, encoding="utf-8")
    return tool["slug"]

def main():
    print("=" * 52)
    print("  HRToolPick — Alternatives Page Generator")
    print("=" * 52)
    
    with open(DATA_FILE, encoding="utf-8") as f:
        all_tools = json.load(f)
    
    # Build slug lookup
    slug_map = {t["slug"]: t for t in all_tools}
    id_map = {t["id"]: t for t in all_tools}
    
    print(f"\n✅ Loaded {len(all_tools)} tools")
    
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    env.filters["selectattr"] = lambda items, attr: [i for i in items if i.get(attr)]
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    generated = []
    skipped = []
    
    print(f"\n📄 Generating alternatives pages...\n")
    
    for target_id in TARGET_TOOLS:
        # Find tool by slug or id
        tool = slug_map.get(target_id) or id_map.get(target_id)
        if not tool:
            skipped.append(target_id)
            print(f"  ✗ Not found: {target_id}")
            continue
        
        slug = generate_alternatives_page(env, tool, all_tools, OUTPUT_DIR)
        generated.append(slug)
        print(f"  ✓ /alternatives/{slug}/")
    
    # Update sitemap to include alternatives pages
    sitemap_path = OUTPUT_DIR / "sitemap.xml"
    with open(sitemap_path, encoding="utf-8") as f:
        sitemap = f.read()
    
    # Add alternatives URLs to sitemap
    new_urls = ""
    for slug in generated:
        new_urls += f'  <url><loc>https://hrtoolpick.com/alternatives/{slug}/</loc><lastmod>{CURRENT_YEAR}-{MONTH_NUM}-01</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>\n'
    
    sitemap = sitemap.replace('</urlset>', new_urls + '</urlset>')
    sitemap_path.write_text(sitemap, encoding="utf-8")
    
    print(f"\n{'=' * 52}")
    print(f"  Done! Generated {len(generated)} alternatives pages")
    if skipped:
        print(f"  Skipped: {skipped}")
    print(f"  Sitemap updated: {len(generated)} new URLs added")
    print(f"  Output: {OUTPUT_DIR}/alternatives/")
    print("=" * 52)

if __name__ == "__main__":
    main()
