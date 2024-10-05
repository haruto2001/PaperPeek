import os

from openai import OpenAI


def main() -> None:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    input_text = "Hello world!"
    output_path = "data/test.mp3"
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input=input_text,
    ) as response:
        response.stream_to_file(output_path)


if __name__ == "__main__":
    main()