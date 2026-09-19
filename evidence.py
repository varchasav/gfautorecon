import json
from datetime import datetime
from pathlib import Path


class EvidenceCollector:

    def __init__(
        self,
        output_directory="output"
    ):

        self.output_directory = Path(
            output_directory
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    def create_scan_record(
        self,
        target,
        start_time,
        end_time,
        results,
        gf_results,
        pattern_count,
        classified_findings=None,
        finding_summary=None
    ):

        if classified_findings is None:
            classified_findings = []

        if finding_summary is None:
            finding_summary = {}

        duration = (
            end_time - start_time
        ).total_seconds()

        urls = results.get(
            "urls",
            set()
        )

        javascript = results.get(
            "javascript",
            set()
        )

        endpoints = results.get(
            "endpoints",
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

        http_info = results.get(
            "http_info",
            {}
        )

        record = {

            "scanner": {
                "name":
                    "GF-AutoRecon",

                "version":
                    "0.1"
            },

            "target":
                target,

            "scan": {

                "started":
                    start_time.isoformat(),

                "completed":
                    end_time.isoformat(),

                "duration_seconds":
                    duration
            },

            "discovery": {

                "urls":
                    sorted(urls),

                "parameters":
                    parameters,

                "forms":
                    forms,

                "javascript":
                    sorted(javascript),

                "endpoints":
                    sorted(endpoints),

                "http_info":
                    http_info
            },

            "gf_analysis": {

                "pattern_count":
                    pattern_count,

                "url_matches":
                    gf_results.get(
                        "url_matches",
                        []
                    ),

                "parameter_matches":
                    gf_results.get(
                        "parameter_matches",
                        []
                    ),

                "form_matches":
                    gf_results.get(
                        "form_matches",
                        []
                    ),

                "javascript_matches":
                    gf_results.get(
                        "javascript_matches",
                        []
                    )
            },

            "finding_classification": {

                "summary":
                    finding_summary,

                "findings":
                    classified_findings
            }
        }

        return record

    def save_json(
        self,
        record
    ):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            f"scan_{timestamp}.json"
        )

        filepath = (
            self.output_directory /
            filename
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                record,
                file,
                indent=4,
                ensure_ascii=False,
                default=str
            )

        return filepath