import subprocess as sp
from pathlib import Path
import logging
import sys
from dataclasses import dataclass
import re

LOGGER = logging.getLogger("aoc")


@dataclass
class SolutionTarget:
    name: str
    full_name: str
    year: int
    day: int
    language: str

    @staticmethod
    def list_targets(build_directory: Path) -> list["SolutionTarget"] | None:
        if not build_directory.is_dir():
            LOGGER.error("%s is not a directory", build_directory)
            return None
        res = sp.run(
            ["cmake", "--build", str(build_directory), "--target", "help"],
            capture_output=True,
            encoding="utf-8",
        )
        if res.returncode != 0:
            LOGGER.error(
                "Could not list targets for %s (%s)",
                build_directory,
                res.stderr.strip(),
            )
            return None

        solution_name_re = re.compile(r"^aoc(\d{4})-(\d{2})-(\w+)$")
        result = []
        for target in res.stdout.splitlines():
            parts = target.strip().split(": ")
            if len(parts) != 2:
                continue

            full_name, target_type = parts
            if target_type != "CUSTOM_COMMAND":
                continue

            name = full_name.split("/")[-1]
            res = solution_name_re.fullmatch(name)
            if res is None:
                continue

            result.append(
                SolutionTarget(
                    name=name,
                    full_name=full_name,
                    year=int(res[1]),
                    day=int(res[2]),
                    language=res[3],
                )
            )
        return result

    def run(self, build_directory: Path) -> None:
        sp.run(
            ["cmake", "--build", str(build_directory), "--target", self.name],
        )


print(
    "\n".join(str(t) for t in SolutionTarget.list_targets(Path(sys.argv[1])))
)
