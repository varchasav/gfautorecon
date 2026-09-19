import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class PatternManager:

    REPOSITORY_API = (
        "https://api.github.com/repos/"
        "1ndianl33t/Gf-Patterns/contents/"
    )

    RAW_BASE = (
        "https://raw.githubusercontent.com/"
        "1ndianl33t/Gf-Patterns/master/"
    )

    def __init__(self, pattern_directory="patterns"):

        self.pattern_directory = Path(
            pattern_directory
        )

        self.pattern_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    def get_remote_patterns(self):

        request = Request(
            self.REPOSITORY_API,
            headers={
                "User-Agent": "GF-AutoRecon"
            }
        )

        try:

            with urlopen(
                request,
                timeout=15
            ) as response:

                data = json.loads(
                    response.read().decode(
                        "utf-8"
                    )
                )

        except (
            HTTPError,
            URLError,
            TimeoutError
        ) as error:

            print(
                f"[-] GitHub connection failed: {error}"
            )

            return []

        pattern_files = []

        for item in data:

            name = item.get("name", "")

            if name.lower().endswith(".json"):

                pattern_files.append(name)

        return sorted(pattern_files)

    def download_pattern(self, filename):

        url = self.RAW_BASE + filename

        request = Request(
            url,
            headers={
                "User-Agent": "GF-AutoRecon"
            }
        )

        try:

            with urlopen(
                request,
                timeout=15
            ) as response:

                content = response.read()

            # Validate JSON before saving
            data = json.loads(
                content.decode("utf-8")
            )

            if "patterns" not in data:

                print(
                    f"[-] Invalid GF pattern: "
                    f"{filename}"
                )

                return False

            destination = (
                self.pattern_directory /
                filename
            )

            with open(
                destination,
                "wb"
            ) as file:

                file.write(content)

            return True

        except (
            HTTPError,
            URLError,
            TimeoutError,
            json.JSONDecodeError,
            OSError
        ) as error:

            print(
                f"[-] Failed: "
                f"{filename} | {error}"
            )

            return False

    def update_patterns(self):

        print(
            "\n[*] Checking GitHub GF patterns..."
        )

        remote_patterns = (
            self.get_remote_patterns()
        )

        if not remote_patterns:

            print(
                "[-] No patterns retrieved."
            )

            return False

        print(
            f"[+] Found "
            f"{len(remote_patterns)} "
            "remote pattern files."
        )

        downloaded = 0

        for filename in remote_patterns:

            print(
                f"    [*] Downloading "
                f"{filename}"
            )

            if self.download_pattern(
                filename
            ):

                downloaded += 1

                print(
                    f"    [+] Saved "
                    f"{filename}"
                )

        print(
            f"\n[+] Pattern update complete."
        )

        print(
            f"[+] Available: "
            f"{len(remote_patterns)}"
        )

        print(
            f"[+] Downloaded: "
            f"{downloaded}"
        )

        return downloaded > 0

    def local_pattern_count(self):

        return len(
            list(
                self.pattern_directory.glob(
                    "*.json"
                )
            )
        )