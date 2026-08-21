from __future__ import annotations

import subprocess
from collections.abc import Sequence


class CommandRunner:

    def run(
        self,
        command: Sequence[str],
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            list(command),
            check=True,
            capture_output=True,
            text=True,
        )
