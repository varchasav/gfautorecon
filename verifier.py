from collections import Counter


class FindingVerifier:

    """
    Safe finding classification layer.

    IMPORTANT:
    A GF pattern match is NOT automatically a vulnerability.

    This module classifies findings based on the evidence
    already collected by the crawler and GF engine.
    """

    STATUS_PATTERN_MATCH = "PATTERN_MATCH"
    STATUS_CANDIDATE = "CANDIDATE"
    STATUS_NOT_VERIFIED = "NOT_VERIFIED"

    def __init__(self):

        self.category_info = {

            "xss": {
                "type": "Cross-Site Scripting",
                "confidence": "LOW"
            },

            "sqli": {
                "type": "SQL Injection",
                "confidence": "LOW"
            },

            "ssrf": {
                "type": "Server-Side Request Forgery",
                "confidence": "LOW"
            },

            "lfi": {
                "type": "Local File Inclusion",
                "confidence": "LOW"
            },

            "rce": {
                "type": "Remote Code Execution",
                "confidence": "LOW"
            },

            "ssti": {
                "type": "Server-Side Template Injection",
                "confidence": "LOW"
            },

            "idor": {
                "type": "Insecure Direct Object Reference",
                "confidence": "LOW"
            },

            "redirect": {
                "type": "Open Redirect Candidate",
                "confidence": "LOW"
            },

            "debug_logic": {
                "type": "Debug / Logic Exposure",
                "confidence": "LOW"
            },

            "interestingparams": {
                "type": "Interesting Parameter",
                "confidence": "INFO"
            },

            "interestingsubs": {
                "type": "Interesting Subdomain",
                "confidence": "INFO"
            },

            "jsvar": {
                "type": "JavaScript Variable",
                "confidence": "INFO"
            }
        }

    def normalize_category(self, category):

        return category.lower().strip()

    def get_category_info(self, category):

        category = self.normalize_category(
            category
        )

        return self.category_info.get(
            category,
            {
                "type": category.upper(),
                "confidence": "LOW"
            }
        )

    def classify_finding(self, finding):

        category = finding.get(
            "category",
            "unknown"
        )

        source_type = finding.get(
            "source_type",
            "UNKNOWN"
        )

        source = finding.get(
            "source",
            ""
        )

        matches = finding.get(
            "matches",
            []
        )

        info = self.get_category_info(
            category
        )

        classification = {

            "category": category,

            "type": info["type"],

            "source_type": source_type,

            "source": source,

            "matches": matches,

            "status":
                self.STATUS_CANDIDATE,

            "confidence":
                info["confidence"],

            "verification":
                "NOT_PERFORMED",

            "reason":
                (
                    "The source matched one or more "
                    "GF reconnaissance patterns. "
                    "This is a candidate and does not "
                    "confirm a vulnerability."
                )
        }

        return classification

    def classify_all(self, findings):

        classified = []

        for finding in findings:

            classified.append(
                self.classify_finding(
                    finding
                )
            )

        return classified

    def summary(self, classified_findings):

        status_counts = Counter()

        category_counts = Counter()

        for finding in classified_findings:

            status_counts[
                finding.get(
                    "status",
                    "UNKNOWN"
                )
            ] += 1

            category_counts[
                finding.get(
                    "category",
                    "unknown"
                )
            ] += 1

        return {

            "total": len(
                classified_findings
            ),

            "status_counts": dict(
                status_counts
            ),

            "category_counts": dict(
                category_counts
            )
        }