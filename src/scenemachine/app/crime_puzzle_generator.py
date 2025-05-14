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
from pydantic import BaseModel, Field

from src.scenemachine.exceptions.app_exception import AppException
from src.scenemachine.llm.llm_facade import LLM
from src.scenemachine.llm.llm_messages import LLMMessages
from src.scenemachine.util.logging_util import LoggingUtil


class CrimePuzzle(BaseModel):
    """Request model"""
    Narrative: str = Field(
        ..., description="String giving the main body of the crime puzzle."
    )
    Solution: str = Field(
        ..., description="String giving the solution of the crime puzzle."
    )


class CrimePuzzleGenerator:
    """
    CrimePuzzleGenerator is a class that generates a crime puzzle based on a given user query.
    """

    LOGGER = LoggingUtil.instance("<CrimePuzzleGenerator>")

    def __init__(self) -> None:
        pass

    def generate(self) -> CrimePuzzle:
        """Creates a crime puzzle"""

        self.LOGGER.info("Generating a CrimePuzzle...")
        try:
            llm: LLM = LLM()
            llm_messages = LLMMessages()

            prompt: str = f"""
                === INSTRUCTIONS ===

                Write me a cozy short crime puzzle, set in England around 1925. 
                Inspector Diogenes Shannon is on the case of a whodunnit that the reader has to solve. 
                Give clues in the crime narrative and also a solution.
   
                """
            llm_messages = llm_messages.build(prompt, llm_messages.USER)
            response: CrimePuzzle = llm.do_instructor(
                messages=llm_messages.messages, response_model=CrimePuzzle
            )
            return response
        except Exception as error:
            self.LOGGER.error(str(error))
            raise AppException(str(error))
