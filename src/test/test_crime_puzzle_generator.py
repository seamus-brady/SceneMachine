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

import unittest

from src.scenemachine.app.crime_puzzle_generator import (
    CosyCrimePuzzle,
    CosyCrimePuzzleGenerator,
    CosyCrimePuzzleScenario,
    ReviewedCosyCrimePuzzle,
)


class TestCrimePuzzleGenerator(unittest.TestCase):

    def test_random_crime(self) -> None:
        generator = CosyCrimePuzzleGenerator()
        crime = generator.random_crime()
        self.assertIn(crime, generator.crime_pool, "The crime is not in the crime pool.")

    def test_random_motive(self) -> None:
        generator = CosyCrimePuzzleGenerator()
        motive = generator.random_motive()
        self.assertIn(motive, generator.motive_pool, "The motive is not in the motive pool.")

    def test_run_generate_seed(self) -> None:
        crime_puzzle_seed: str = CosyCrimePuzzleGenerator().generate_random_crime_seed()
        print(crime_puzzle_seed)
        self.assertIsInstance(crime_puzzle_seed, str)

    def test_run_generate_scenario(self) -> None:
        crime_puzzle_seed: str = CosyCrimePuzzleGenerator().generate_random_crime_seed()
        print(crime_puzzle_seed)
        crime_puzzle_scenario: CosyCrimePuzzleScenario = (
            CosyCrimePuzzleGenerator().generate_puzzle_scenario(crime_seed=crime_puzzle_seed)
        )
        print(crime_puzzle_scenario)
        self.assertIsInstance(crime_puzzle_scenario, CosyCrimePuzzleScenario)
        self.assertIsInstance(crime_puzzle_scenario.crime, str)
        self.assertIsInstance(crime_puzzle_scenario.location, str)
        self.assertTrue(len(crime_puzzle_scenario.participants) > 0)

    def test_run_generate_puzzle(self) -> None:
        crime_puzzle_seed: str = CosyCrimePuzzleGenerator().generate_random_crime_seed()
        crime_puzzle_scenario: CosyCrimePuzzleScenario = (
            CosyCrimePuzzleGenerator().generate_puzzle_scenario(crime_seed=crime_puzzle_seed)
        )
        crime_puzzle: CosyCrimePuzzle = CosyCrimePuzzleGenerator().generate_puzzle(
            crime_puzzle_scenario
        )
        print(crime_puzzle.narrative)
        print(crime_puzzle.solution)
        self.assertIsInstance(crime_puzzle, CosyCrimePuzzle)
        self.assertIsInstance(crime_puzzle.narrative, str)
        self.assertIsInstance(crime_puzzle.solution, str)

    def test_run_review_puzzle(self) -> None:
        crime_puzzle_seed: str = CosyCrimePuzzleGenerator().generate_random_crime_seed()
        crime_puzzle_scenario: CosyCrimePuzzleScenario = (
            CosyCrimePuzzleGenerator().generate_puzzle_scenario(crime_seed=crime_puzzle_seed)
        )
        crime_puzzle: CosyCrimePuzzle = CosyCrimePuzzleGenerator().generate_puzzle(
            crime_puzzle_scenario
        )
        reviewed_puzzle: ReviewedCosyCrimePuzzle = CosyCrimePuzzleGenerator().review_puzzle(
            crime_puzzle
        )
        self.assertIsInstance(reviewed_puzzle, ReviewedCosyCrimePuzzle)
        self.assertEqual(reviewed_puzzle.case_title, crime_puzzle.case_title)
        self.assertIsInstance(reviewed_puzzle.detective_notes, str)
        self.assertGreater(len(reviewed_puzzle.detective_notes), 0)
        self.assertIsInstance(reviewed_puzzle.analysis, str)


if __name__ == "__main__":
    unittest.main()
