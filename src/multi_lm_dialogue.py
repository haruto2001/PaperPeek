import os

from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables import Runnable
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from modules import ChatSessionManager
from utils import get_logger

logger = get_logger(__name__)


def create_chat_prompt_template(system_prompt_template: str) -> ChatPromptTemplate:
    """
    Creates a chat prompt template with a given system prompt template.

    Args:
        system_prompt_template (str): The system prompt template to use.

    Returns:
        ChatPromptTemplate: The chat prompt template with the given system prompt template.
    """
    chat_prompt_template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_prompt_template),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )
    return chat_prompt_template


def create_runnable_with_history(
    chat_prompt_template: ChatPromptTemplate,
    chat_model: ChatOpenAI,
    session_manager: ChatSessionManager,
) -> RunnableWithMessageHistory:
    """
    Creates a runnable with message history using a chat prompt template and chat model.

    Args:
        chat_prompt_template (ChatPromptTemplate): The chat prompt template to use.
        chat_model (ChatOpenAI): The chat model to use.

    Returns:
        RunnableWithMessageHistory: The runnable with message history using the given chat prompt template and chat model.
    """
    runnable = chat_prompt_template | chat_model
    runnable_with_history = RunnableWithMessageHistory(
        runnable,
        session_manager.get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )
    return runnable_with_history


def simulate_conversation(
    runnable_a: Runnable,
    runnable_b: Runnable,
    name_a: str = "太郎",
    name_b: str = "花子",
    session_id: str = "123",
    initial_input: str = "日本の良いところについて話しましょう！",
    turns: int = 2,
) -> None:
    """
    Simulates a conversation between two models.

    Args:
        runnable_a (Runnable): The first runnable to simulate the conversation with.
        runnable_b (Runnable): The second runnable to simulate the conversation with.
        name_a (str): The name of the first runnable (default: "太郎").
        name_b (str): The name of the second runnable (default: "花子").
        session_id (str): The session ID to use for the conversation (default: "123").
        initial_input (str): The initial input to start the conversation with (default: "日本の良いところについて話しましょう．").
        turns (int): The number of turns to simulate in the conversation (default: 2).
    """
    conversation_turn = initial_input
    logger.info(f"{name_b} (ターン: 0): {conversation_turn}")
    for turn in range(turns):
        try:
            output_a = runnable_a.invoke(
                {"input": conversation_turn},
                config={"configurable": {"session_id": session_id}},
            )
            logger.info(f"{name_a} (ターン: {turn+1}): {output_a.content}")

            output_b = runnable_b.invoke(
                {"input": output_a.content},
                config={"configurable": {"session_id": session_id}},
            )
            logger.info(f"{name_b} (ターン: {turn+1}): {output_b.content}")

            conversation_turn = output_b.content
        except Exception as e:
            logger.error(
                f"Error during conversation simulation at turn {turn+1}: {str(e)}"
            )
            break


def main() -> None:
    """
    Main function to simulate a conversation between two models.
    """
    chat_model = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], model="gpt-4o")

    name_a = "太郎"
    name_b = "花子"

    session_manager = ChatSessionManager()

    system_prompt_template_a = f"あなたは{name_a}です．{name_b}と会話をしてください．"
    system_prompt_template_b = f"あなたは{name_b}です．{name_a}と会話をしてください．"

    chat_prompt_template_a = create_chat_prompt_template(system_prompt_template_a)
    chat_prompt_template_b = create_chat_prompt_template(system_prompt_template_b)

    runnable_with_history_a = create_runnable_with_history(
        chat_prompt_template_a, chat_model, session_manager
    )
    runnable_with_history_b = create_runnable_with_history(
        chat_prompt_template_b, chat_model, session_manager
    )

    simulate_conversation(runnable_with_history_a, runnable_with_history_b)


if __name__ == "__main__":
    main()
