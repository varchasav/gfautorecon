from datetime import datetime
from discovery.crawler import Crawler
from core.gf_engine import GFEngine
from core.pattern_manager import PatternManager
from core.evidence import EvidenceCollector
from core.verifier import FindingVerifier


# ============================================================
# BANNER
# ============================================================

print("=" * 60)
print("                 GF-AutoRecon")
print("=" * 60)


# ============================================================
# TARGET
# ============================================================

target = input(
    "\nEnter authorized target URL: "
).strip()


if not target:

    print("[-] No URL entered.")
    exit()


# ============================================================
# START SCAN TIMER
# ============================================================

scan_start = datetime.now()


# ============================================================
# UPDATE GF PATTERNS
# ============================================================

print("\n" + "=" * 60)
print("                 GF PATTERNS")
print("=" * 60)


pattern_manager = PatternManager()

pattern_manager.update_patterns()


# ============================================================
# START CRAWLER
# ============================================================

print("\n" + "=" * 60)
print("                 CRAWLER")
print("=" * 60)


print("\n[*] Starting crawler...")
print(f"[*] Target: {target}")


crawler = Crawler(
    target,
    max_depth=2,
    max_pages=50,
    delay=0.5
)


results = crawler.crawl()


# ============================================================
# EXTRACT RESULTS
# ============================================================

urls = results.get(
    "urls",
    set()
)

parameters = results.get(
    "parameters",
    {}
)

forms = results.get(
    "forms",
    []
)

javascript = results.get(
    "javascript",
    set()
)

endpoints = results.get(
    "endpoints",
    set()
)

http_info = results.get(
    "http_info",
    {}
)


# ============================================================
# DISCOVERY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("                 DISCOVERY RESULTS")
print("=" * 60)


# ------------------------------------------------------------
# URLs
# ------------------------------------------------------------

print(
    f"\n[+] URLs discovered: "
    f"{len(urls)}"
)


for url in sorted(urls):

    print(
        f"    {url}"
    )


# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------

total_parameters = sum(
    len(parameter_list)
    for parameter_list in parameters.values()
)


print(
    f"\n[+] URLs with parameters: "
    f"{len(parameters)}"
)

print(
    f"[+] Parameters discovered: "
    f"{total_parameters}"
)


for url, parameter_list in parameters.items():

    print(
        f"\n    URL: {url}"
    )

    for parameter in parameter_list:

        print(
            f"        Parameter: "
            f"{parameter}"
        )


# ------------------------------------------------------------
# FORMS
# ------------------------------------------------------------

print(
    f"\n[+] Forms discovered: "
    f"{len(forms)}"
)


for index, form in enumerate(forms, 1):

    print(
        f"\n    Form #{index}"
    )

    print(
        f"        Page: "
        f"{form.get('page', '')}"
    )

    print(
        f"        Action: "
        f"{form.get('action', '')}"
    )

    print(
        f"        Method: "
        f"{form.get('method', '')}"
    )

    fields = form.get(
        "fields",
        []
    )

    print(
        f"        Fields: "
        f"{', '.join(fields)}"
    )


# ------------------------------------------------------------
# JAVASCRIPT
# ------------------------------------------------------------

print(
    f"\n[+] JavaScript files discovered: "
    f"{len(javascript)}"
)


if javascript:

    for js in sorted(javascript):

        print(
            f"    {js}"
        )

else:

    print(
        "    No JavaScript files discovered."
    )


# ------------------------------------------------------------
# ENDPOINTS
# ------------------------------------------------------------

print(
    f"\n[+] Endpoints discovered: "
    f"{len(endpoints)}"
)


if endpoints:

    for endpoint in sorted(endpoints):

        print(
            f"    {endpoint}"
        )

else:

    print(
        "    No endpoint candidates found."
    )


# ------------------------------------------------------------
# HTTP INFORMATION
# ------------------------------------------------------------

print(
    "\n[+] HTTP information:"
)


for url, info in http_info.items():

    print(
        f"\n    URL: {url}"
    )

    print(
        f"        Status: "
        f"{info.get('status', '')}"
    )

    print(
        f"        Content-Type: "
        f"{info.get('content_type', '')}"
    )

    print(
        f"        Final URL: "
        f"{info.get('final_url', '')}"
    )


# ============================================================
# GF ENGINE
# ============================================================

print("\n" + "=" * 60)
print("                 GF ANALYSIS")
print("=" * 60)


gf_engine = GFEngine()

gf_engine.load_patterns()


gf_results = gf_engine.analyze(
    urls,
    parameters,
    forms,
    javascript
)


# ============================================================
# GF MATCH RESULTS
# ============================================================

url_matches = gf_results.get(
    "url_matches",
    []
)

parameter_matches = gf_results.get(
    "parameter_matches",
    []
)

form_matches = gf_results.get(
    "form_matches",
    []
)

javascript_matches = gf_results.get(
    "javascript_matches",
    []
)


# ------------------------------------------------------------
# URL MATCHES
# ------------------------------------------------------------

print(
    f"\n[+] URL pattern matches: "
    f"{len(url_matches)}"
)


for finding in url_matches:

    print(
        f"\n    [{finding['category']}]"
    )

    print(
        f"    Source: "
        f"{finding['source']}"
    )

    print(
        f"    Matches: "
        f"{', '.join(finding['matches'])}"
    )


# ------------------------------------------------------------
# PARAMETER MATCHES
# ------------------------------------------------------------

print(
    f"\n[+] Parameter pattern matches: "
    f"{len(parameter_matches)}"
)


for finding in parameter_matches:

    print(
        f"\n    [{finding['category']}]"
    )

    print(
        f"    Source: "
        f"{finding['source']}"
    )

    print(
        f"    Matches: "
        f"{', '.join(finding['matches'])}"
    )


# ------------------------------------------------------------
# FORM MATCHES
# ------------------------------------------------------------

print(
    f"\n[+] Form pattern matches: "
    f"{len(form_matches)}"
)


for finding in form_matches:

    print(
        f"\n    [{finding['category']}]"
    )

    print(
        f"    Source: "
        f"{finding['source']}"
    )

    print(
        f"    Matches: "
        f"{', '.join(finding['matches'])}"
    )


# ------------------------------------------------------------
# JAVASCRIPT MATCHES
# ------------------------------------------------------------

print(
    f"\n[+] JavaScript pattern matches: "
    f"{len(javascript_matches)}"
)


for finding in javascript_matches:

    print(
        f"\n    [{finding['category']}]"
    )

    print(
        f"    Source: "
        f"{finding['source']}"
    )

    print(
        f"    Matches: "
        f"{', '.join(finding['matches'])}"
    )


# ============================================================
# FINDING CLASSIFICATION
# ============================================================

print("\n" + "=" * 60)
print("                 FINDING CLASSIFICATION")
print("=" * 60)


verifier = FindingVerifier()


classified_findings = verifier.classify_all(
    gf_results.get(
        "findings",
        []
    )
)


finding_summary = verifier.summary(
    classified_findings
)


print(
    f"\n[+] Total findings: "
    f"{finding_summary['total']}"
)


for finding in classified_findings:

    print(
        f"\n    [{finding['category']}]"
    )

    print(
        f"    Type: "
        f"{finding['type']}"
    )

    print(
        f"    Source Type: "
        f"{finding['source_type']}"
    )

    print(
        f"    Source: "
        f"{finding['source']}"
    )

    print(
        f"    Status: "
        f"{finding['status']}"
    )

    print(
        f"    Confidence: "
        f"{finding['confidence']}"
    )

    print(
        f"    Verification: "
        f"{finding['verification']}"
    )

    print(
        f"    Reason: "
        f"{finding['reason']}"
    )


# ============================================================
# SCAN SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("                 SCAN SUMMARY")
print("=" * 60)


print(
    f"\n[+] URLs discovered       : "
    f"{len(urls)}"
)

print(
    f"[+] Parameter URLs        : "
    f"{len(parameters)}"
)

print(
    f"[+] Parameters discovered : "
    f"{total_parameters}"
)

print(
    f"[+] Forms discovered      : "
    f"{len(forms)}"
)

print(
    f"[+] JavaScript files      : "
    f"{len(javascript)}"
)

print(
    f"[+] Endpoints discovered  : "
    f"{len(endpoints)}"
)

print(
    f"[+] GF patterns loaded    : "
    f"{len(gf_engine.patterns)}"
)

print(
    f"[+] GF URL matches        : "
    f"{len(url_matches)}"
)

print(
    f"[+] GF parameter matches  : "
    f"{len(parameter_matches)}"
)

print(
    f"[+] GF form matches       : "
    f"{len(form_matches)}"
)

print(
    f"[+] GF JavaScript matches : "
    f"{len(javascript_matches)}"
)

print(
    f"[+] Classified findings   : "
    f"{len(classified_findings)}"
)


# ============================================================
# SAVE SCAN EVIDENCE
# ============================================================

scan_end = datetime.now()


print("\n" + "=" * 60)
print("                 SAVING EVIDENCE")
print("=" * 60)


evidence = EvidenceCollector()


scan_record = evidence.create_scan_record(
    target=target,
    start_time=scan_start,
    end_time=scan_end,
    results=results,
    gf_results=gf_results,
    pattern_count=len(
        gf_engine.patterns
    ),
    classified_findings=classified_findings,
    finding_summary=finding_summary
)


saved_file = evidence.save_json(
    scan_record
)


print(
    "\n[+] Scan evidence saved:"
)

print(
    f"    {saved_file}"
)


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 60)

print(
    "[+] GF-AutoRecon scan completed successfully."
)

print(
    "[+] Pattern matches are candidates, "
    "not confirmed vulnerabilities."
)

print("=" * 60)