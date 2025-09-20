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

import random  # nosec
from typing import List

from pydantic import (
    BaseModel,
    Field,
)

from src.scenemachine.exceptions.app_exception import AppException
from src.scenemachine.llm.llm_facade import LLM
from src.scenemachine.llm.llm_messages import LLMMessages
from src.scenemachine.modes.adaptive_request_mode import AdaptiveRequestMode
from src.scenemachine.util.file_path_util import FilePathUtil
from src.scenemachine.util.logging_util import LoggingUtil


class CosyCrimePuzzleParticipant(BaseModel):
    """Request model"""

    participant: str = Field(
        ..., description="String giving a description of a crime puzzle participant."
    )


class CosyCrimePuzzleScenario(BaseModel):
    """Request model"""

    location: str = Field(
        ..., description="String giving a description of where the crime takes place."
    )

    crime: str = Field(..., description="String giving a description of a crime.")

    additional_notes: str = Field(..., description="String giving extra notes if needed.")

    participants: list[CosyCrimePuzzleParticipant]


class CosyCrimePuzzle(BaseModel):
    """Request model"""

    case_title: str = Field(..., description="String giving the name of the crime case.")

    narrative: str = Field(..., description="String giving the main body of the crime puzzle.")

    solution: str = Field(..., description="String giving the solution of the crime puzzle.")


class ReviewedCosyCrimePuzzle(BaseModel):
    """Request model"""

    case_title: str = Field(..., description="String giving the name of the crime case.")

    detective_notes: str = Field(
        ..., description="String giving the main detectives notes on the crime."
    )

    narrative: str = Field(..., description="String giving the main body of the crime puzzle.")

    solution: str = Field(..., description="String giving the solution of the crime puzzle.")

    analysis: str = Field(..., description="String giving an analysis of the crime puzzle.")


class CosyCrimePuzzleGenerator:
    """
    CrimePuzzleGenerator is a class that generates a cosy crime puzzle based on a given user query.
    """

    LOGGER = LoggingUtil.instance("<CosyCrimePuzzleGenerator>")

    # prompt file paths
    COSY_CRIME_TIME_PERIOD_MD = "/cosy_crime/time_period.md"
    COSY_CRIME_VILLAGE_MD = "/cosy_crime/village.md"
    COSY_CRIME_DETECTIVE_MD = "/cosy_crime/detective.md"

    # crime list
    CRIME_POOL_LIST = [
        "murder",
        "attempted murder",
        "manslaughter",
        # "burglary",
        # "arson",
        # "theft from person",
        # "trespass with intent",
        "blackmail",
        # "bigamy",
        # "illegal gambling",
        # "impersonating a police officer",
        "poisoning",
        "grave robbery",
        "smuggling",
        "fraud",
        # "slander",
        # "receiving stolen goods",
        # "forgery",
        # "tampering with mail",
        # "theft of church funds",
        # "illegal sale of rationed goods",
        # "unlawful burial",
        # "operating without a license",
        # "bribery of a local official",
        # "desecration of church property",
        # "killing a protected animal",
        # "unauthorised use of herbal poisons"
    ]

    # motive list
    MOTIVE_POOL_LIST = [
        "inheritance gain",
        "revenge for wartime betrayal",
        "silencing a blackmailer",
        "elimination of a romantic rival",
        "obsession with control",
        "removal of a political opponent",
        "revenge for social humiliation",
        "concealing past wartime crimes",
        "revenge for loss of a loved one in war",
        "resentment over class or status",
        "cold-blooded sociopathy",
        "suppressing a scandal",
        "avoiding disgrace due to moral failing",
        "protecting the family name",
        "hiding a shameful past",
        "preventing a secret from coming out",
        "protecting a respectable facade",
        "fear of blackmail exposure",
        "gambling debt",
        "business failure",
        "loss of pension",
        "desperate poverty",
        "land or inheritance dispute",
        "fraud cover-up",
        "insurance fraud",
        "inheritance theft",
        "sabotaging a competitor",
        "avoiding bankruptcy",
        "economic jealousy",
        "PTSD-induced dissociation",
        "trauma-triggered blackout",
        "clinical depression",
        "delusions of persecution",
        "repressed guilt",
        "early dementia",
        "split identity",
        "chronic grief",
        "paranoia",
        "manic episode",
        "romantic jealousy",
        "love triangle",
        "protecting a child",
        "protecting a spouse",
        "maternal possessiveness",
        "sibling rivalry",
        "generational resentment",
        "abandonment by a partner",
        "controlling behaviour",
        "sexual jealousy",
        "unrequited love",
        "mercy killing",
        "preventing greater harm",
        "taking the fall for a loved one",
        "misguided sense of honour",
        "duty to protect the vulnerable",
        "atonement for past failure",
        "ideological commitment",
        "sacrificing self for another",
        "misinterpreted prophecy",
        "loyalty to the dead",
        "self-defence",
        "crime of passion",
        "blackmail gone wrong",
        "panic after accidental injury",
        "mistaken identity",
        "drunken altercation",
        "fight escalating unintentionally",
        "misplaced blame",
        "prank turned deadly",
        "weapon discharge during struggle",
    ]

    def __init__(self) -> None:
        self.crime_pool: List = CosyCrimePuzzleGenerator.CRIME_POOL_LIST
        self.motive_pool: list = CosyCrimePuzzleGenerator.MOTIVE_POOL_LIST
        self.time_period: str = self.load_time_period_file()
        self.detective: str = self.load_detective_file()
        self.village: str = self.load_village_file()

    def random_crime(self) -> str:
        """Returns a random crime from the crime pool."""
        return str(random.choice(self.crime_pool))  # nosec

    def random_motive(self) -> str:
        """Returns a random motive from the motive pool."""
        return str(random.choice(self.motive_pool))  # nosec

    def load_time_period_file(self) -> str:
        """Loads the detective file as a string."""
        file_path = FilePathUtil.prompt_folder_path() + self.COSY_CRIME_TIME_PERIOD_MD
        return FilePathUtil.load_file_as_string(file_path)

    def load_detective_file(self) -> str:
        """Loads the detective file as a string."""
        file_path = FilePathUtil.prompt_folder_path() + self.COSY_CRIME_DETECTIVE_MD
        return FilePathUtil.load_file_as_string(file_path)

    def load_village_file(self) -> str:
        """Loads the village file as a string."""
        file_path = FilePathUtil.prompt_folder_path() + self.COSY_CRIME_VILLAGE_MD
        return FilePathUtil.load_file_as_string(file_path)

    def generate_random_crime_seed(self) -> str:
        """Creates a random crime puzzle seed."""

        self.LOGGER.info("Generating a CrimePuzzleScenario...")
        try:
            llm: LLM = LLM()
            llm_messages = LLMMessages()

            prompt: str = f"""
            === INSTRUCTIONS ===
            
            - Generate a description of a crime using details below.
            - The description should be a single paragraph as if taken from a newspaper.
            - Please include as much detail as possible, including the time, place, and nature of the crime.
            
            === STEPS ===
            
            1. Review all provided background information.
            2. Create the crime description.
            3. Review your work and make sure it is coherent and consistent with the time period and setting.
            4. Update and correct any inconsistencies if needed.
            
            === CRIME YEAR ===
            
            {self.time_period}

            === CRIME SETTING ===
            
            {self.village}
            
            === CRIME TYPE ===
            
            {self.random_crime()}
            
            === CRIME MOTIVE ===
            
            {self.random_motive()}
            
            """
            llm_messages = llm_messages.build(prompt, llm_messages.USER)
            response: str = llm.do_string_completion(
                messages=llm_messages.messages, mode=AdaptiveRequestMode.controlled_creative_mode()
            )
            return response
        except Exception as error:
            self.LOGGER.error(str(error))
            raise AppException(str(error))

    def generate_puzzle_scenario(self, crime_seed: str) -> CosyCrimePuzzleScenario:
        """Creates a crime puzzle scenario with participants."""

        self.LOGGER.info("Generating a CrimePuzzleScenario...")
        try:
            llm: LLM = LLM()
            llm_messages = LLMMessages()

            prompt: str = f"""
            === INSTRUCTIONS ===

            - Write a cosy short crime puzzle scenario using the newspaper article below as a seed.
            
            
            === STEPS ===

            1. Generate a structured crime puzzle scenario. Do not write a narrative. 
            2. You do not need to include the detective or police in the output. These will be added later.
            3. Review the background article and create the crime scenario.
            3. Review your work and make sure it is coherent and consistent with the time period and setting.
            4. Update and correct any inconsistencies if needed.
            
            === COMPONENTS ===
            
            Provide the following components:
            
                Location: A brief description of where the crime took place.
            
                Crime: The nature of the crime (e.g., murder, theft, sabotage).
            
                Participants: A list of 3 to 6 named individuals involved in the scenario. Each entry should include:
            
                    Name
            
                    Role or relation to the others (e.g., gardener, business partner, sibling)
            
                    Any relevant background detail or motive
            
                Additional Notes (optional): Any unusual conditions, items found at the scene, alibis, or known facts 
                that might be relevant to solving the case.
            
            Constraints:
            
                At least one participant must be a suspect.
            
                One participant may be the victim.
            
                Optionally, the guilty party and the victim can be the same person (e.g., a staged accident or suicide).
            
                Do not include the solution or point out who is guilty.
            
                Avoid supernatural or implausible elements.
                
                
            === CRIME NEWSPAPER ARTICLE ===
            {crime_seed}
            """
            llm_messages = llm_messages.build(prompt, llm_messages.USER)
            response: CosyCrimePuzzleScenario = llm.do_instructor(
                messages=llm_messages.messages,
                response_model=CosyCrimePuzzleScenario,
                mode=AdaptiveRequestMode.controlled_creative_mode(),
            )
            return response
        except Exception as error:
            self.LOGGER.error(str(error))
            raise AppException(str(error))

    def generate_puzzle(self, crime_puzzle_scenario: CosyCrimePuzzleScenario) -> CosyCrimePuzzle:
        """Creates a crime puzzle narrative with a solution."""

        self.LOGGER.info("Generating a CrimePuzzle...")
        try:
            llm: LLM = LLM()
            llm_messages = LLMMessages()

            prompt: str = f"""
            === INSTRUCTIONS ===

            Write a cosy crime puzzle, using the steps below and the scenario and background details provided.
            
            === STEPS ===
            
    `        ## STEP 1: Start with a Simple, Singular Crime
            
            - Choose a core mystery to anchor the story based on the newspaper article below.
            - Please note, your goal is a logical puzzle, not a dramatic thriller.
            - This puzzle should be difficult but not impossible to solve.
            
            ## STEP 2: Establish a Closed Setting
            
            - Create a closed-circle environment that helps contain suspects and clues.
            - The setting must be a logical extension of the background details provided.
            - Keep the world small enough for everyone to plausibly interact.
            
            ## STEP 3: Create a Cast of 4–6 Characters
            
            - Using the list of parcipants provided, create your characters.
            - Each should serve a role:
            
                - The detective
                - The victim 
                - 2–3 suspects, each with a possible motive
                - 1–2 bystanders, red herrings, or secret-holders
            
            - Give each character:
                - A motivation
                - A relationship to the others
                - A quirk or distinctive trait
            
            ## STEP 4: Build a Timeline and Alibis
            
            - Create a clear chain of events and where each character claims to be at critical moments.
            - Example:
            
                6:00 p.m. – Dinner begins
                6:45 p.m. – Power outage
                7:00 p.m. – Body discovered
            
            - Everyone must fit into that timeline—with room for contradiction.
            - Please note this timeline does not have to be made explicit in the narrative unless useful.
            - This timeline can serve as the framework you hang your story on.
            
            
            STEP 5: Plan Your Clues and Red Herrings
            
            - Now layer your narrative puzzle with:
                - 1–2 telling details (the real clues)
                - 2–3 red herrings (details that seem suspicious but aren’t)
            
            - Types of telling clues (choose one as appropriate or combine):
            
                1. Knowledge They Shouldn’t Have - These are clues where the suspect reveals something they couldn't possibly know unless they were involved.
                2. Time Inconsistencies - These involve contradictions or impossibilities related to time.
                3. Physical Impossibilities - The suspect’s story contradicts physical reality.
                4. Behavioral Slips - These are inconsistencies in how someone acts or reacts.
                5. Clothing and Appearance - These relate to what someone is wearing or how they’re presented.
                6. Environmental Mismatch - The setting doesn’t match the suspect’s story.
                7. Implausible Tools or Objects - The story requires something that doesn’t make sense.
                8. Reversed or Incorrect Assumptions - Sometimes the flaw is in logic or assumption.

            
                TIP: The best puzzles hide the telling detail in natural-sounding dialogue or setting. 
                The detective’s genius is not in noticing something dramatic—but in realizing something doesn’t quite fit.
            
            Your detective will eventually reason backward from one or more of these.
            
            ## STEP 6: Write the Narrative in Scenes
            
            - Structure the narrative similar to below but feel free to elaborate if it improve the narrative:
            
                - Introduce the setting, characters, and crime.
                - Let the detective begin investigating.
                - Show the detective speaking with each suspect.
                - Let inconsistencies emerge.
                - Include 1–2 clue moments and some red herrings.
            
            - The clues and red herrings should slot smoothly into the narrative with editorialising or narrative comment. 
            - Do not add anything to suggest something is a clue, a red herring or someone is a suspect. Then it is not a puzzle!
            
            - The solution is given separately from the narrative so the reader has a chance to complete the puzzle. 
            
            - End the puzzle narrative with a challenge to the reader, for example:
            
                Why does the detective suspect the neighbor?
                What doesn’t add up about her story?
                What has the detective realized?
            
            - DO NOT GIVE AWAY THE SOLUTION BY GIVING LEADING QUESTIONS.
            
            ## STEP 7: Make the Clue Solvable
            
            - This is crucial in a puzzle story:
            
                - Everything the detective uses should be visible to the reader.
                - Don’t spring surprise info at the end.
                - Make the “Aha!” moment satisfying.
                - The reader should slap their forehead, not throw the book.
            
            - The solution should be provided outside the main narrative so the reader has a chance to complete the puzzle.
            
            ## STEP 8: Write With Cosy Mystery Voice
            
                1. Measured and Observant
                
                Make sure your prose is clear, concise, and unadorned, with a calm, almost detached narration. 
                This tone allows readers to observe events and characters closely, picking up on subtle clues and 
                red herrings.
                
                2. Witty and Dryly Humorous
                
                There’s often a layer of understated British wit, especially in dialogue. 
                Characters deliver clever observations with dry, ironic humor.
                
                3. Atmospheric and Tense
                
                While never overtly grim or gory, you should builds a quiet, simmering tension.
                 Whether in a country house, train, or isolated island, there’s a growing sense that something 
                 is deeply wrong beneath the surface.
                 
                4. Polite but Deceptive
                
                HYour settings are sometimes genteel but the tone often contrasts civility with underlying deceit, 
                making murder all the more chilling when it intrudes.
                
                5. Analytical and Logical
                
                Your tone values order, rationality, and deduction. The storytelling mimics a puzzle, encouraging the 
                reader to solve the mystery alongside the characters.
                
                In short: restrained, clever, and quietly unsettling, with a sharp eye for human nature.
                            
            ## STEP 9 - Review your work
            
            - Go back through the puzzle and check for inconsistencies, mistakes and other errors.
            - Check that your solution has the detective use logic to eliminate the red herring and isolate the real clue.
            - In your solution, explain how the contradiction reveals the guilty party’s involvement.
            - The solution should be airtight but not obvious on first reading.
            
            General Output Constraints

            - Avoid direct confessions, obvious evidence, or technological solutions.
            - The crime puzzle should be consistent with the time period and setting. No iPhones in the 1950s!
            - Make sure all clues are presented in the narrative — no external knowledge should be required.
            - Ensure that the reader has enough information to solve it, but only if they catch the logical 
              inconsistency.
            - Do not use em-dashes.
                
            === CRIME PUZZLE SCENARIO ===
            
            {crime_puzzle_scenario}
            
            === CRIME YEAR ===
            
            {self.time_period}

            === CRIME SETTING ===
            
            {self.village}
            
            === CRIME DETECTIVE ===
            
            {self.detective}
            
            """
            llm_messages = llm_messages.build(prompt, llm_messages.USER)
            response: CosyCrimePuzzle = llm.do_instructor(
                messages=llm_messages.messages,
                response_model=CosyCrimePuzzle,
                mode=AdaptiveRequestMode.controlled_creative_mode(),
            )
            return response
        except Exception as error:
            self.LOGGER.error(str(error))
            raise AppException(str(error))

    def review_puzzle(self, crime_puzzle: CosyCrimePuzzle) -> ReviewedCosyCrimePuzzle:
        """Reviews a crime puzzle narrative with a solution."""

        self.LOGGER.info("Reviewing a CrimePuzzle...")
        try:
            llm: LLM = LLM()
            llm_messages = LLMMessages()

            prompt: str = f"""
            === INSTRUCTIONS ===

            You must review the cosy crime puzzle below and provide a review of the narrative and solution.

            === STEPS ===

            1. Read the crime puzzle narrative and solution and check all the following points below.
            2. Add the detective's notes to the narrative, summarising the key point using the example below.
            3. The detective's notes should:
               - Stay within the story world
               - Deliver structured information without breaking tone
               - Preserve the puzzle while deepening character immersion
               - Avoid "narrator voice" that could bias or spoil
               - Not give away the solution or lead the reader to it in the notes. 
               - Avoid tipping the reader off to physical clues or contradictions. 
                 Those should be unearthed naturally in the narrative.
               - Your goal is to preserve the puzzle element and give the reader a chance to solve it themselves, 
                 the suspect list should be clean and neutral, without including any embedded clues or editorial hints.
                 The suspect list should be personality traits or community roles. 
            2. Tighten the narrative, removing any unnecessary words or phrases.
            3. Remove the use of em-dashes.
            4. Ensure the narrative is coherent and consistent with the time period and setting.
            5. Ensure the solution is logical and can be deduced from the narrative. Also, ensure the solution is not
               silly, trivial or stupid. There is no point in writing a puzzle that is not solvable but also no 
               satisfaction in solving a puzzle that is too easy or trivial. This is very important.
            6. The questions at the end of the narrative should be open-ended and not lead the reader to the solution.
            7. Provide a review of the narrative and solution, including any inconsistencies or errors.
            8. Indicate the level of difficulty of the puzzle on a scale of 1 to 10, where 1 is very easy and 10 is 
               very difficult.
            9. Review your work again.
    `     
            === CRIME PUZZLE SCENARIO ===

            {crime_puzzle}

            === CRIME YEAR ===

            {self.time_period}

            === CRIME SETTING ===

            {self.village}

            === CRIME DETECTIVE ===

            {self.detective}
            
            === DETECTIVE NOTES EXAMPLE ===
            
            Case: <CASE_TITLE>
            Date: <DATE>
            Filed by: <DETECTIVE_NAME>
            Location: <LOCATION>
            
            Incident
            
                Parish records office found unlocked morning of July 17
            
                1935–36 correspondence file missing
            
                Known to contain letters detailing past financial irregularities and potential council misconduct
            
                Torn envelope discovered near disused marl pit
            
                Vehicle tracks and two sets of footprints at scene
            
            Suspects
            
                Mrs. Enid Whitelaw
                
                    Local resident. Drove past marl pit evening of the 16th.
                
                    Claims to have stopped to walk her dog.
                
                Mr. Lionel Frobisher
                
                    Parish treasurer and post office clerk.
                
                    States he was home with his sister that evening.
                
                Miss Agnes Frobisher
                
                    Resides with Lionel.
                
                    Confirms his alibi.
                
                Mr. Harold Pym
                
                    Village grocer and council member.
                
                    Claims to have remained at home, aside from a brief outing.
            
            Known Facts
            
              Weather dry since early morning July 16
            
              Muddy ground persists only at marl pit
            
              Witness reports of a figure near the post office that evening

            """
            llm_messages = llm_messages.build(prompt, llm_messages.USER)
            response: ReviewedCosyCrimePuzzle = llm.do_instructor(
                messages=llm_messages.messages,
                response_model=ReviewedCosyCrimePuzzle,
                mode=AdaptiveRequestMode.controlled_creative_mode(),
            )
            return response
        except Exception as error:
            self.LOGGER.error(str(error))
            raise AppException(str(error))
