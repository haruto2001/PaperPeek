from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory


class ChatSessionManager:
    """
    Manages chat message histories for different session IDs.

    Attributes:
        history (dict[str, BaseChatMessageHistory]): A dictionary to store chat message histories based on session IDs.
    """

    def __init__(self) -> None:
        """
        Initializes the ChatSessionManager with an empty history dictionary.
        """
        self.history: dict[str, BaseChatMessageHistory] = {}

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """
        Gets the chat message history for a given session ID.

        Args:
            session_id (str): The session ID to get the history for.

        Returns:
            BaseChatMessageHistory: The chat message history for the given session ID.
        """
        if session_id not in self.history:
            self.history[session_id] = ChatMessageHistory()
        return self.history[session_id]
