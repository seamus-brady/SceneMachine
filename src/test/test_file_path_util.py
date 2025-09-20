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
import os
import unittest

from src.scenemachine.util.file_path_util import FilePathUtil


class TestFilePathUtil(unittest.TestCase):
    def test_prompt_folder_path(self):
        expected_path = os.path.join(FilePathUtil.repo_root_path(), "config", "prompts")
        self.assertEqual(FilePathUtil.prompt_folder_path(), expected_path)


if __name__ == "__main__":
    unittest.main()
