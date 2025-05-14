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

from src.scenemachine.app.crime_puzzle_generator import CrimePuzzleGenerator, CrimePuzzle


class TestCrimePuzzleGenerator(unittest.TestCase):
    def test_run_diagnostic_test(self):
        crime_puzzle = CrimePuzzleGenerator().generate()
        self.assertIsInstance(crime_puzzle, CrimePuzzle)
        self.assertIsInstance(crime_puzzle.Narrative, str)
        self.assertIsInstance(crime_puzzle.Solution, str)


if __name__ == "__main__":
    unittest.main()
