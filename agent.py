from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer,AgentSession, Agent, room_io, function_tool
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv(".env")

data = {
    "vishal" : {
        "email" : "vishalshetty@gmail.com",
        "salary" : 2000
    } ,
    "tom" : {
        "email" : "tom@gmail.com",
        "salary" : 20000
    } ,
}

@function_tool
async def get_employee_directory(employee_name : str) -> str:
    """
     Look up employee contact details.

    Use this tool when the user asks for an employee's email.
    The input is the employee's first name.
    Ensure you conver the name to lowercase and remove the apostrophe s
    
    Args:
        employee_name: Name of the employee like John
    """

    return data[employee_name] 



class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful voice AI assistant.
            You eagerly assist users with their questions by providing information from your extensive knowledge.
            Your responses are concise, to the point, and without any complex formatting or punctuation including emojis, asterisks, or other symbols.
            You are curious, friendly, and have a sense of humor. If the user asks about employee details such as email,
            you must use the employee directory tool instead of guessing.
            Dont give salary or any confidental information about the user only provide the contact details
            
            """,
            tools = [get_employee_directory]
        )

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