from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer,AgentSession, Agent, room_io, function_tool, RunContext
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

import json

load_dotenv(".env")

with open('data.json', 'r') as file:
    data = json.load(file)

print(data)
print(type(data))
class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful voice AI assistant.
            You eagerly assist users with their questions by providing information from your extensive knowledge of different employees.
            Your responses are concise, to the point, and without any complex formatting or punctuation including emojis, asterisks, or other symbols.
            You are curious, friendly, and have a sense of humor. If the user asks about employee details such as email,
            You must use the employee directory tool for finding employee information instead of guessing.
            You must ask for the last name if the user only tells the first name and the retrival doesnt happen.
            Dont give salary or any confidental information about the user only provide the contact details.
            """,
        )
    @function_tool
    async def get_employee_directory(self,employee_name : str, context: RunContext) -> str:
        """
        Look up employee contact details.

        Use this tool when the user asks for an employee's email.
        The input is the employee's first name and last name which is not separeted with a whitespace.
        Ensure you conver the name to lowercase and remove the apostrophe S.
        
        Args:
            employee_name: Name of the employee like John
        """
        employee_name = employee_name.lower().strip()
        print(employee_name)
        if data[employee_name]:
            return data[employee_name]
        else:
            return "Employee doesnt exist in the directory"

server = AgentServer()

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        stt="assemblyai/universal-streaming:en",
        llm="openai/gpt-4.1-mini",
        tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony() if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP else noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)