import logging
from typing import List, Dict, Any, Mapping
from abc import ABC, abstractmethod
logger = logging.getLogger("agent_frame")


class LMAgent:
    """Base class for an agent."""

    def __init__(self, config: Mapping[str, Any]):
        self.config = config
        logger.debug(f"Initialized {self.__class__.__name__} with config: {config}")
        # The agent should not generate observations or expert feedback
        self.stop_words = ["\nObservation:", "\nTask:", "\n---"]

    def __call__(self) -> str:
        pass
    
    @abstractmethod
    def probs_gen(self, messages: List[dict],get_probs=False):
        pass
    
    def add_system_message(
        self, messages: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        # Prepend the prompt with the system message
        first_msg = messages[0]
        assert first_msg["role"] == "user"
        system, examples, task = first_msg["content"].split("\n---\n")
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": examples + "\n---\n" + task},
        ] + messages[1:]
        return messages
