"""
HRToolPick — Best Picks Page Generator
=======================================
Generates "best [category]" pages targeting high-intent buyers.
These pages convert better than comparison pages because
visitors already know they want a solution — just not which one.

Usage:
    python scripts/generate_best_picks.py
"""

import json
import os
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

BASE_DIR     = Path(__file__).parent.parent
DATA_FILE    = BASE_DIR / "data" / "tools.json"
TEMPLATE_DIR = BASE_DIR / "templates"
OUTPUT_DIR   = BASE_DIR / "output"

CURRENT_YEAR  = datetime.now().year
CURRENT_MONTH = datetime.now().strftime("%B")
MONTH_NUM     = datetime.now().strftime("%m")

# Color map
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
    "patriot-payroll": "#dc2626", "homebase": "#db2777",
    "borderless-ai": "#6d28d9", "bambee": "#b45309", "humi": "#0369a1",
    "employment-hero": "#dc2626", "deputy": "#4f46e5", "lattice": "#7c3aed",
    "workable": "#d97706", "greenhouse": "#15803d", "keka": "#0891b2",
    "freshteam": "#16a34a", "velocity-global": "#0f766e",
    "workforce-com": "#1e3a8a", "sesame-hr": "#9f1239",
}

# Best picks page definitions
BEST_PICKS_PAGES = [
    {
        "slug": "payroll-software-small-business",
        "page_title": "Best Payroll Software for Small Business",
        "category_label": "payroll software for small business",
        "meta_description": "The 7 best payroll software for small businesses in 2026 — ranked by price, ease of use, and tax filing. Find the right payroll tool for your team.",
        "intro": "We tested and ranked the top payroll platforms for small businesses based on pricing transparency, ease of use, automated tax filing, and customer support.",
        "quick_pick": "Gusto is our top pick for most small businesses — transparent pricing, automated tax filing, and a great employee experience. OnPay is the best budget option at $40/mo base.",
        "tool_slugs": ["gusto", "onpay", "patriot-payroll", "quickbooks-payroll", "adp-run", "paychex", "wave-payroll"],
        "pick_labels": {
            "gusto": "Best overall",
            "onpay": "Best value",
            "patriot-payroll": "Best for micro teams",
            "quickbooks-payroll": "Best for QuickBooks users",
            "adp-run": "Best for scaling up",
            "paychex": "Best customer support",
            "wave-payroll": "Best budget pick",
        },
        "pick_why": {
            "gusto": "Gusto combines full-service payroll, automated tax filing, and HR tools in one intuitive platform. With transparent pricing starting at $40/mo + $6/employee, it's the best all-in-one solution for most small businesses.",
            "onpay": "OnPay consistently earns the highest user ratings (4.8/5 on G2) for simplicity and value. At $40/mo + $6/employee with all features included, it's the most affordable full-service option.",
            "patriot-payroll": "At $17/mo + $4/employee, Patriot is the cheapest full-service payroll software available. Perfect for businesses under 25 employees who don't need complex HR features.",
            "quickbooks-payroll": "If your accounting lives in QuickBooks, adding QuickBooks Payroll eliminates duplicate data entry completely. The seamless sync saves hours every pay run.",
            "adp-run": "ADP RUN is built to scale — start as a small business and grow without switching platforms. The trusted ADP brand brings robust compliance tools.",
            "paychex": "Paychex assigns a dedicated payroll specialist to your account, making it the best choice for businesses that want human support alongside their software.",
            "wave-payroll": "At $20/mo base, Wave is ideal for tiny teams already using free Wave accounting. Contractor-only mode is just $6/month per contractor.",
        },
        "faqs": [
            {"q": "What is the easiest payroll software for small business?", "a": "Gusto and OnPay are consistently rated the easiest to use, with most businesses running their first payroll within 24 hours of signing up. Both offer step-by-step setup and unlimited customer support."},
            {"q": "Does small business payroll software file taxes automatically?", "a": "Yes — all platforms on this list offer automated federal, state, and local tax filing. This includes calculating withholdings, filing returns, and paying taxes on your behalf."},
            {"q": "How much does payroll software cost for a small business?", "a": "Most payroll software charges a base fee ($17-$59/month) plus a per-employee fee ($4-$12/employee/month). For 5 employees, expect to pay $40-$100/month total."},
            {"q": "Can I run payroll myself without an accountant?", "a": "Yes — modern payroll software is designed for non-experts. Gusto, OnPay, and Patriot all guide you through setup and automate the complex tax calculations."},
        ],
        "related_pages": [
            {"label": "Gusto alternatives", "url": "/alternatives/gusto/"},
            {"label": "OnPay alternatives", "url": "/alternatives/onpay/"},
            {"label": "Gusto vs OnPay", "url": "/compare/gusto-vs-onpay/"},
            {"label": "Best HR software for remote teams", "url": "/best/hr-software-remote-teams/"},
        ],
    },
    {
        "slug": "hr-software-remote-teams",
        "page_title": "Best HR Software for Remote Teams",
        "category_label": "HR software for remote teams",
        "meta_description": "The 7 best HR software platforms for remote and distributed teams in 2026. Compare global payroll, EOR services, and remote HR tools.",
        "intro": "Managing a remote or distributed team requires HR software that handles global compliance, multi-currency payroll, and async collaboration. Here are the best options in 2026.",
        "quick_pick": "Rippling is our top pick for remote teams needing HR, IT, and payroll in one platform. For pure global payroll, Deel and Remote are the strongest options.",
        "tool_slugs": ["rippling", "deel", "remote", "gusto", "multiplier", "oyster-hr", "bamboohr"],
        "pick_labels": {
            "rippling": "Best all-in-one",
            "deel": "Best for global contractors",
            "remote": "Best for EOR transparency",
            "gusto": "Best for US remote teams",
            "multiplier": "Best fast onboarding",
            "oyster-hr": "Best ethical EOR",
            "bamboohr": "Best US-focused HRIS",
        },
        "pick_why": {
            "rippling": "Rippling uniquely combines HR, IT (device management, app provisioning), and payroll in one platform — perfect for remote teams where IT provisioning is as important as payroll.",
            "deel": "Deel operates in 150+ countries with automated compliance, multi-currency payments, and a free HRIS. The best option if you regularly hire contractors across borders.",
            "remote": "Remote owns its legal entities in 70+ countries (rather than using partners), giving better compliance guarantees. Transparent pricing with no hidden fees.",
            "gusto": "For US-based remote teams working across multiple states, Gusto handles multi-state tax compliance automatically — a significant pain point for distributed US teams.",
            "multiplier": "Multiplier onboards employees in under 2 days in 150+ countries. The fastest option if you need to hire internationally at speed.",
            "oyster-hr": "Oyster is a B-Corp certified EOR committed to fair employment practices globally. Best for companies that care about ethical global employment.",
            "bamboohr": "For US-only remote teams, BambooHR provides excellent HRIS with strong onboarding, performance management, and e-signatures — without paying for global features you don't need.",
        },
        "faqs": [
            {"q": "What HR software is best for a fully remote company?", "a": "Rippling is the most complete solution for fully remote companies, combining HR, IT, and payroll. For international teams, Deel and Remote are the strongest for global compliance."},
            {"q": "Do I need an EOR for remote international employees?", "a": "Yes, if you're hiring employees (not contractors) in countries where you don't have a legal entity. EOR services like Deel, Remote, and Oyster HR act as the legal employer on your behalf."},
            {"q": "How much does global HR software cost?", "a": "EOR services typically cost $299-$599/employee/month for full-time employees. Contractor management is cheaper at $29-$49/contractor/month. US-only HR software like BambooHR starts around $10/employee/month."},
            {"q": "Can remote teams use free HR software?", "a": "Zoho People and Freshteam offer free plans, but they're limited. Remote and Oyster HR offer free contractor management. For serious global employment, paid EOR services are necessary for legal compliance."},
        ],
        "related_pages": [
            {"label": "Deel alternatives", "url": "/alternatives/deel/"},
            {"label": "Remote alternatives", "url": "/alternatives/remote/"},
            {"label": "Deel vs Remote", "url": "/compare/deel-vs-remote/"},
            {"label": "Best global payroll software", "url": "/best/global-payroll-software/"},
        ],
    },
    {
        "slug": "global-payroll-software",
        "page_title": "Best Global Payroll Software",
        "category_label": "global payroll software",
        "meta_description": "The 7 best global payroll software platforms in 2026. Compare EOR services, multi-country payroll, and international HR tools for distributed teams.",
        "intro": "Global payroll software handles multi-currency payments, local tax compliance, and employee benefits across borders. Here are the top platforms for international teams in 2026.",
        "quick_pick": "Deel is our top pick for most companies starting global payroll — it covers 150+ countries, has transparent pricing, and includes a free HRIS. Remote is the best for compliance purists who want owned legal entities.",
        "tool_slugs": ["deel", "remote", "multiplier", "oyster-hr", "remofirst", "papaya-global", "rippling"],
        "pick_labels": {
            "deel": "Best overall",
            "remote": "Best compliance",
            "multiplier": "Best speed",
            "oyster-hr": "Best ethical",
            "remofirst": "Best budget",
            "papaya-global": "Best enterprise",
            "rippling": "Best US+global combo",
        },
        "pick_why": {
            "deel": "Deel operates in 150+ countries with automated compliance, contractor and employee payments, and a free HRIS for teams under 200. The most complete global payroll platform.",
            "remote": "Remote owns its legal entities in 70+ countries — unlike most competitors who use local partners. This means better compliance guarantees and faster hiring timelines.",
            "multiplier": "Multiplier onboards international employees in under 48 hours in 150+ countries. The fastest EOR for teams that need to hire at speed.",
            "oyster-hr": "Oyster HR is a B-Corp certified EOR that focuses on equitable global employment. Best for companies that prioritize ethical hiring practices worldwide.",
            "remofirst": "At $199/employee/month, RemoFirst is the most affordable full EOR service available — covering 180+ countries. Best for startups watching costs.",
            "papaya-global": "Papaya Global is built for enterprise finance teams, with deep integrations into Workday, SAP, and Oracle. Best for large companies consolidating global payroll.",
            "rippling": "Rippling handles both US domestic HR+IT and global payroll in one platform — the best choice for companies that started in the US and are expanding internationally.",
        },
        "faqs": [
            {"q": "What is global payroll software?", "a": "Global payroll software processes employee and contractor payments across multiple countries, handling local tax calculations, compliance requirements, currency conversions, and statutory benefits automatically."},
            {"q": "What is the difference between EOR and global payroll?", "a": "An Employer of Record (EOR) acts as the legal employer in countries where you don't have a legal entity, handling all compliance. Global payroll software processes payments but requires you to have local entities. Most modern platforms offer both."},
            {"q": "How much does global payroll cost?", "a": "EOR services cost $199-$599/employee/month. Contractor management runs $29-$49/contractor/month. Enterprise global payroll aggregators use custom pricing based on headcount and countries."},
            {"q": "Which global payroll software is easiest to use?", "a": "Deel and Multiplier consistently earn the highest ease-of-use scores. Both offer self-serve onboarding and can have your first international employee set up within days."},
        ],
        "related_pages": [
            {"label": "Deel vs Remote", "url": "/compare/deel-vs-remote/"},
            {"label": "Deel vs Multiplier", "url": "/compare/deel-vs-multiplier/"},
            {"label": "Remote alternatives", "url": "/alternatives/remote/"},
            {"label": "Best HR software for remote teams", "url": "/best/hr-software-remote-teams/"},
        ],
    },
    {
        "slug": "payroll-software-startups",
        "page_title": "Best Payroll Software for Startups",
        "category_label": "payroll software for startups",
        "meta_description": "The 7 best payroll software platforms for startups in 2026. Compare pricing, features, and scalability for growing teams.",
        "intro": "Startups need payroll software that's fast to set up, affordable, and scales with growth. Here are the best options for seed-stage to Series B companies in 2026.",
        "quick_pick": "Gusto is the go-to for US startups — it handles payroll, benefits, and basic HR in one place with transparent pricing. For global-first startups, Rippling or Deel are stronger choices.",
        "tool_slugs": ["gusto", "rippling", "deel", "justworks", "remote", "onpay", "bamboohr"],
        "pick_labels": {
            "gusto": "Best US startup pick",
            "rippling": "Best for tech startups",
            "deel": "Best for global-first",
            "justworks": "Best PEO for benefits",
            "remote": "Best transparent global",
            "onpay": "Best budget startup",
            "bamboohr": "Best HRIS for growing teams",
        },
        "pick_why": {
            "gusto": "Gusto is designed for startups — fast setup, automated compliance, and integrated benefits administration without enterprise complexity or pricing.",
            "rippling": "For tech startups, Rippling uniquely handles HR, IT (laptop provisioning, SSO, app access), and payroll in one system — critical for remote-first engineering teams.",
            "deel": "Global-first startups hiring contractors or employees across borders should start with Deel. Free for contractor management and transparent EOR pricing.",
            "justworks": "Justworks gives startups access to Fortune 500-level benefits (better health insurance rates) through its PEO model — a huge advantage for recruiting talent.",
            "remote": "Remote is ideal for startups hiring their first international employees, with owned legal entities and no hidden fees in the pricing.",
            "onpay": "For budget-conscious startups with simple US payroll needs, OnPay's flat pricing and 4.8/5 G2 rating make it the best value option.",
            "bamboohr": "As startups scale past 50 employees, BambooHR provides the HRIS depth needed for performance management, onboarding workflows, and org chart visibility.",
        },
        "faqs": [
            {"q": "What payroll software do most startups use?", "a": "Gusto is the most popular payroll software among US startups, particularly at seed and Series A stage. Rippling is common among tech startups for its HR+IT integration. Deel is standard for global-first startups."},
            {"q": "When should a startup switch from spreadsheets to payroll software?", "a": "As soon as you hire your first W-2 employee. Manual payroll is error-prone and non-compliance carries significant penalties. Most platforms take under an hour to set up."},
            {"q": "Does payroll software help with startup equity compensation?", "a": "Rippling and Gusto integrate with equity management platforms like Carta and Pulley. They handle RSU vesting payroll taxes automatically, which is critical for startup equity programs."},
            {"q": "What is the cheapest payroll software for a 2-person startup?", "a": "Wave Payroll ($20/mo base) or Patriot ($17/mo base) are the most affordable. For just 2 employees, OnPay at $40/mo + $12 ($52 total) is excellent value with better features."},
        ],
        "related_pages": [
            {"label": "Gusto vs Rippling", "url": "/compare/gusto-vs-rippling/"},
            {"label": "Gusto alternatives", "url": "/alternatives/gusto/"},
            {"label": "Best payroll for small business", "url": "/best/payroll-software-small-business/"},
            {"label": "Best HR software for remote teams", "url": "/best/hr-software-remote-teams/"},
        ],
    },
    {
        "slug": "hris-software",
        "page_title": "Best HRIS Software",
        "category_label": "HRIS software",
        "meta_description": "The 7 best HRIS software platforms in 2026. Compare HR information systems for employee records, onboarding, performance, and payroll integration.",
        "intro": "An HRIS (Human Resource Information System) is the central database for all employee data. Here are the best HRIS platforms for businesses of all sizes in 2026.",
        "quick_pick": "BambooHR is the best HRIS for most SMBs — clean UI, strong onboarding, and excellent customer support. Rippling is best if you need HR and IT in one system.",
        "tool_slugs": ["bamboohr", "rippling", "hibob", "personio", "workday-hcm", "ukg-pro", "zoho-people"],
        "pick_labels": {
            "bamboohr": "Best for SMBs",
            "rippling": "Best HR+IT unified",
            "hibob": "Best modern UX",
            "personio": "Best for Europe",
            "workday-hcm": "Best for enterprise",
            "ukg-pro": "Best workforce mgmt",
            "zoho-people": "Best free option",
        },
        "pick_why": {
            "bamboohr": "BambooHR is the gold standard HRIS for SMBs — intuitive UI, strong onboarding workflows, e-signatures, and excellent support. Most teams are fully set up within a week.",
            "rippling": "Rippling uniquely connects HR data with IT provisioning — when you onboard a new hire, it automatically sets up their laptop, installs apps, and grants system access.",
            "hibob": "HiBob's modern, employee-first design drives the highest adoption rates. Strong culture and engagement tools make it ideal for people-centric companies.",
            "personio": "Built specifically for European compliance (GDPR, local labor laws), Personio is the best HRIS for companies headquartered or operating in Europe.",
            "workday-hcm": "Workday is the enterprise standard for large organizations needing deep analytics, complex approval workflows, and global coverage across 100+ countries.",
            "ukg-pro": "UKG Pro excels at workforce management for complex scheduling environments — best for industries like healthcare, manufacturing, and retail with hourly workers.",
            "zoho-people": "Zoho People's free plan covers up to 5 users with core HRIS features. For budget-conscious teams already in the Zoho ecosystem, it's the obvious choice.",
        },
        "faqs": [
            {"q": "What is HRIS software?", "a": "HRIS (Human Resource Information System) software is a database system that manages employee information — personal records, job history, time off, performance reviews, and org charts — in one place."},
            {"q": "What is the difference between HRIS, HRMS, and HCM?", "a": "HRIS focuses on employee data management. HRMS (HR Management System) adds process automation like payroll and benefits. HCM (Human Capital Management) is the broadest category, covering talent management, workforce planning, and analytics."},
            {"q": "Do I need an HRIS if I already have payroll software?", "a": "Yes — payroll software handles payment processing but lacks HR features like org charts, performance reviews, onboarding workflows, and document management. Most companies use both together."},
            {"q": "What is the best free HRIS?", "a": "Zoho People offers the most generous free plan (up to 5 users). Freshteam also has a free plan for up to 50 employees. Both cover core HRIS needs without a payroll module."},
        ],
        "related_pages": [
            {"label": "BambooHR alternatives", "url": "/alternatives/bamboohr/"},
            {"label": "BambooHR vs HiBob", "url": "/compare/bamboohr-vs-hibob/"},
            {"label": "Best HR software for remote teams", "url": "/best/hr-software-remote-teams/"},
            {"label": "HiBob alternatives", "url": "/alternatives/hibob/"},
        ],
    },
]


def load_tools():
    with open(DATA_FILE, encoding="utf-8") as f:
        tools = json.load(f)
    return {t["slug"]: t for t in tools}


def generate_best_picks_page(env, page_def, tool_map, output_dir):
    template = env.get_template("best-picks.html")

    # Get tools for this page
    picks = []
    for slug in page_def["tool_slugs"]:
        tool = tool_map.get(slug)
        if tool:
            picks.append(tool)
        else:
            print(f"    ⚠ Tool not found: {slug}")

    if not picks:
        return None

    # Build color map
    pick_colors = {t["slug"]: COLORS.get(t["slug"], "#3b82f6") for t in picks}

    context = {
        "slug": page_def["slug"],
        "page_title": page_def["page_title"],
        "category_label": page_def["category_label"],
        "meta_description": page_def["meta_description"],
        "intro": page_def["intro"],
        "quick_pick": page_def["quick_pick"],
        "picks": picks,
        "pick_labels": page_def["pick_labels"],
        "pick_why": page_def["pick_why"],
        "pick_colors": pick_colors,
        "faqs": page_def["faqs"],
        "related_pages": page_def["related_pages"],
        "year": CURRENT_YEAR,
        "month": CURRENT_MONTH,
        "month_num": MONTH_NUM,
    }

    page_dir = output_dir / "best" / page_def["slug"]
    page_dir.mkdir(parents=True, exist_ok=True)
    html = template.render(**context)
    (page_dir / "index.html").write_text(html, encoding="utf-8")
    return page_def["slug"]


def main():
    print("=" * 52)
    print("  HRToolPick — Best Picks Page Generator")
    print("=" * 52)

    tool_map = load_tools()
    print(f"\n✅ Loaded {len(tool_map)} tools")

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    env.filters["selectattr"] = lambda items, attr: [i for i in items if i.get(attr)]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    generated = []
    print(f"\n📄 Generating best picks pages...\n")

    for page_def in BEST_PICKS_PAGES:
        slug = generate_best_picks_page(env, page_def, tool_map, OUTPUT_DIR)
        if slug:
            generated.append(slug)
            print(f"  ✓ /best/{slug}/")

    # Update sitemap
    sitemap_path = OUTPUT_DIR / "sitemap.xml"
    with open(sitemap_path, encoding="utf-8") as f:
        sitemap = f.read()

    new_urls = ""
    for slug in generated:
        new_urls += f'  <url><loc>https://hrtoolpick.com/best/{slug}/</loc><lastmod>{CURRENT_YEAR}-{MONTH_NUM}-01</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>\n'

    sitemap = sitemap.replace('</urlset>', new_urls + '</urlset>')
    sitemap_path.write_text(sitemap, encoding="utf-8")

    print(f"\n{'=' * 52}")
    print(f"  Done! Generated {len(generated)} best picks pages")
    print(f"  Sitemap updated: {len(generated)} new URLs added")
    print(f"  Output: {OUTPUT_DIR}/best/")
    print("=" * 52)


if __name__ == "__main__":
    main()
