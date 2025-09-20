#  Copyright (c) 2025 Seamus Brady seamus@corvideon.ie, Corvideon Ltd.
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

import re

import os
import sys
from pathlib import Path
import threading

# path fix for imports ----------------------------------------------
path = Path(os.path.dirname(os.path.realpath(__file__)))
print(path.absolute().__str__())
sys.path.append(path.absolute().__str__())
sys.path.append(path.parent.absolute().__str__())
sys.path.append(path.parent.parent.absolute().__str__())
sys.path.append(path.parent.parent.parent.absolute().__str__())
# path fix for imports ----------------------------------------------

from src.scenemachine.app.crime_puzzle_generator import (
    CosyCrimePuzzle,
    CosyCrimePuzzleGenerator,
    CosyCrimePuzzleScenario,
    ReviewedCosyCrimePuzzle,
)


class App:
    """Main application class for SceneMachine."""

    def __init__(self):
        pass

    @staticmethod
    def generate_markdown(case: ReviewedCosyCrimePuzzle) -> str:
        """Generate markdown content for the case."""

        lines = []
        lines.append(f"# {case.case_title}\n")
        lines.append("## Inspector’s Case Notes\n")
        lines.append(case.detective_notes.strip())
        lines.append("\n")
        lines.append("## Narrative\n")
        lines.append(case.narrative.strip() + "\n")
        lines.append("## Solution (Answer Key)\n")
        lines.append(case.solution.strip() + "\n")
        lines.append("## Analysis\n")
        lines.append(case.analysis.strip())
        return "\n".join(lines)

    @staticmethod
    def slugify(title: str) -> str:
        """Convert case title to a clean filename."""
        slug = title.strip().lower()
        slug = re.sub(r"[^\w\s-]", "", slug)  # remove punctuation
        slug = re.sub(r"\s+", "_", slug)  # replace spaces with underscores
        return slug

    @staticmethod
    def write_markdown_file(case: ReviewedCosyCrimePuzzle) -> None:
        title = case.case_title
        base_filename = App.slugify(title)
        filename = f"{base_filename}.md"

        markdown = App.generate_markdown(case)

        filepath = os.path.join("/home/seamus/GitHub/SceneMachine/output", filename)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(markdown)

        print(f"Markdown file '{filename}' created successfully.")

    @staticmethod
    def run() -> None:
        """Run the main application logic."""

        print("Running SceneMachine application...")
        crime_generator = CosyCrimePuzzleGenerator()
        crime_puzzle_seed: str = crime_generator.generate_random_crime_seed()
        crime_puzzle_scenario: CosyCrimePuzzleScenario = crime_generator.generate_puzzle_scenario(
            crime_seed=crime_puzzle_seed
        )
        crime_puzzle: CosyCrimePuzzle = crime_generator.generate_puzzle(crime_puzzle_scenario)
        reviewed_puzzle: ReviewedCosyCrimePuzzle = crime_generator.review_puzzle(crime_puzzle)
        App.write_markdown_file(reviewed_puzzle)

        print("SceneMachine is running successfully.")


def run_app_in_threads(thread_count: int):
    """Run the App.run() method in multiple threads."""
    threads = []

    for _ in range(thread_count):
        thread = threading.Thread(target=App.run)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    for _ in range(10):
        run_app_in_threads(5)
