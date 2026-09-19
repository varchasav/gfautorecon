import json
from pathlib import Path
import re


class GFEngine:

    def __init__(self, pattern_directory="patterns"):
        self.pattern_directory = Path(pattern_directory)
        self.patterns = {}

    # ---------------------------------------------------------
    # LOAD ALL GF PATTERNS
    # ---------------------------------------------------------

    def load_patterns(self):

        if not self.pattern_directory.exists():

            print(
                "[-] Pattern directory not found: "
                f"{self.pattern_directory}"
            )

            return

        json_files = sorted(
            self.pattern_directory.glob("*.json")
        )

        print(
            f"[+] Found {len(json_files)} "
            "GF pattern files"
        )

        for file_path in json_files:

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

                name = file_path.stem

                self.patterns[name] = data

                print(
                    f"    [+] Loaded: {name}"
                )

            except (
                json.JSONDecodeError,
                OSError
            ) as error:

                print(
                    f"    [-] Failed to load "
                    f"{file_path.name}: {error}"
                )

    # ---------------------------------------------------------
    # GET PATTERNS
    # ---------------------------------------------------------

    def get_pattern_list(self, pattern_data):

        patterns = pattern_data.get(
            "patterns",
            []
        )

        if isinstance(patterns, list):
            return patterns

        return []

    # ---------------------------------------------------------
    # MATCH TEXT AGAINST A GF PATTERN
    # ---------------------------------------------------------

    def match_text(self, text, pattern_data):

        matches = []

        if not text:
            return matches

        patterns = self.get_pattern_list(
            pattern_data
        )

        for pattern in patterns:

            if not isinstance(pattern, str):
                continue

            try:

                if re.search(
                    pattern,
                    text,
                    re.IGNORECASE
                ):

                    matches.append(pattern)

            except re.error:

                if pattern.lower() in text.lower():

                    matches.append(pattern)

        return matches

    # ---------------------------------------------------------
    # ANALYZE A SINGLE TEXT SOURCE
    # ---------------------------------------------------------

    def analyze_text(
        self,
        text,
        source_type,
        source_value
    ):

        findings = []

        for category, pattern_data in self.patterns.items():

            matches = self.match_text(
                text,
                pattern_data
            )

            if matches:

                findings.append({

                    "category": category,

                    "source_type": source_type,

                    "source": source_value,

                    "matches": matches

                })

        return findings

    # ---------------------------------------------------------
    # ANALYZE URLS
    # ---------------------------------------------------------

    def analyze_urls(self, urls):

        findings = []

        for url in urls:

            findings.extend(
                self.analyze_text(
                    url,
                    "URL",
                    url
                )
            )

        return findings

    # ---------------------------------------------------------
    # ANALYZE PARAMETERS
    # ---------------------------------------------------------

    def analyze_parameters(self, parameters):

        findings = []

        for url, parameter_list in parameters.items():

            for parameter in parameter_list:

                findings.extend(
                    self.analyze_text(
                        parameter,
                        "PARAMETER",
                        f"{url} -> {parameter}"
                    )
                )

        return findings

    # ---------------------------------------------------------
    # ANALYZE FORMS
    # ---------------------------------------------------------

    def analyze_forms(self, forms):

        findings = []

        for index, form in enumerate(forms):

            action = form.get(
                "action",
                ""
            )

            method = form.get(
                "method",
                "GET"
            )

            fields = form.get(
                "fields",
                []
            )

            form_text = (
                f"{action} "
                f"{method} "
                f"{' '.join(fields)}"
            )

            findings.extend(
                self.analyze_text(
                    form_text,
                    "FORM",
                    f"Form #{index + 1}"
                )
            )

        return findings

    # ---------------------------------------------------------
    # ANALYZE JAVASCRIPT
    # ---------------------------------------------------------

    def analyze_javascript(self, javascript):

        findings = []

        for js_url in javascript:

            findings.extend(
                self.analyze_text(
                    js_url,
                    "JAVASCRIPT",
                    js_url
                )
            )

        return findings

    # ---------------------------------------------------------
    # COMPLETE ANALYSIS
    # ---------------------------------------------------------

    def analyze(
        self,
        urls,
        parameters,
        forms=None,
        javascript=None
    ):

        print(
            "\n[*] Running universal GF analysis..."
        )

        if forms is None:
            forms = []

        if javascript is None:
            javascript = set()

        all_findings = []

        # URLs
        all_findings.extend(
            self.analyze_urls(urls)
        )

        # Parameters
        all_findings.extend(
            self.analyze_parameters(parameters)
        )

        # Forms
        all_findings.extend(
            self.analyze_forms(forms)
        )

        # JavaScript
        all_findings.extend(
            self.analyze_javascript(
                javascript
            )
        )

        return {

            "findings": all_findings,

            "url_matches": [
                finding
                for finding in all_findings
                if finding["source_type"] == "URL"
            ],

            "parameter_matches": [
                finding
                for finding in all_findings
                if finding["source_type"] == "PARAMETER"
            ],

            "form_matches": [
                finding
                for finding in all_findings
                if finding["source_type"] == "FORM"
            ],

            "javascript_matches": [
                finding
                for finding in all_findings
                if finding["source_type"] == "JAVASCRIPT"
            ]

        }