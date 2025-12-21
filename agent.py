import logging

from dotenv import load_dotenv

logger = logging.getLogger("infobot-agent")
logger.setLevel(logging.INFO)

from livekit import agents, rtc
from livekit.agents import AgentServer,AgentSession, Agent, room_io, function_tool, RunContext
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from livekit.agents.metrics import LLMMetrics, STTMetrics, TTSMetrics, EOUMetrics
import asyncio

from google import genai
import numpy as np

from livekit.plugins import groq



def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


import json

load_dotenv(".env")

# Loading the dummy dataset
with open('data.json', 'r') as file:
    data = json.load(file)

client = genai.Client()

employee_index = np.load(
    "employee_embeddings.npy",
    allow_pickle=True
).tolist()


class Assistant(Agent):
    def __init__(self) -> None:

        super().__init__(
            instructions="""You are a helpful voice AI assistant.
            You eagerly assist users with their questions by providing information from your extensive knowledge of different employees.
            Your responses are concise, to the point, and without any complex formatting or punctuation including emojis, asterisks, or other symbols.
            You are curious, friendly, and have a sense of humor. If the user asks about employee details such as email,
            You must use the employee directory tool for finding employee information instead of guessing.
            Dont give salary or any confidental information about the user only provide the contact details.
            """,
        )

    async def on_enter(self):
        def llm_metrics_wrapper(metrics: LLMMetrics):
            asyncio.create_task(self.on_llm_metrics_collected(metrics))
        def stt_metrics_wrapper(metrics: LLMMetrics):
            asyncio.create_task(self.on_stt_metrics_collected(metrics))
        def eou_metrics_wrapper(metrics: LLMMetrics):
            asyncio.create_task(self.on_eou_metrics_collected(metrics))
        def tts_metrics_wrapper(metrics: LLMMetrics):    
            asyncio.create_task(self.on_tts_metrics_collected(metrics))
    
        
        self.session.llm.on("metrics_collected", llm_metrics_wrapper)
        self.session.stt.on("metrics_collected", stt_metrics_wrapper)
        self.session.stt.on("eou_metrics_collected", eou_metrics_wrapper)
        self.session.tts.on("metrics_collected", tts_metrics_wrapper)
        self.session.generate_reply()

    async def on_llm_metrics_collected(self, metrics: LLMMetrics) -> None:
        print("\n--- LLM Metrics ---")
        print(f"Prompt Tokens: {metrics.prompt_tokens}")
        print(f"Completion Tokens: {metrics.completion_tokens}")
        print(f"Tokens per second: {metrics.tokens_per_second:.4f}")
        print(f"TTFT: {metrics.ttft:.4f}s")
        print("------------------\n")

    async def on_stt_metrics_collected(self, metrics: STTMetrics) -> None:
        print("\n--- STT Metrics ---")
        print(f"Duration: {metrics.duration:.4f}s")
        print(f"Audio Duration: {metrics.audio_duration:.4f}s")
        print(f"Streamed: {'Yes' if metrics.streamed else 'No'}")
        print("------------------\n")

    async def on_eou_metrics_collected(self, metrics: EOUMetrics) -> None:
        print("\n--- End of Utterance Metrics ---")
        print(f"End of Utterance Delay: {metrics.end_of_utterance_delay:.4f}s")
        print(f"Transcription Delay: {metrics.transcription_delay:.4f}s")
        print("--------------------------------\n")

    async def on_tts_metrics_collected(self, metrics: TTSMetrics) -> None:
        print("\n--- TTS Metrics ---")
        print(f"TTFB: {metrics.ttfb:.4f}s")
        print(f"Duration: {metrics.duration:.4f}s")
        print(f"Audio Duration: {metrics.audio_duration:.4f}s")
        print(f"Streamed: {'Yes' if metrics.streamed else 'No'}")
        print("------------------\n")

    @function_tool
    async def get_employee_directory(self,employee_name : str, context: RunContext) -> str:
        """
        Look up employee contact details.

        Use this tool when the user asks for an employee's email.
        The input is the employee's first name and last name which is not separated with a whitespace.
        Ensure you conver the name to lowercase and remove the apostrophe S.
        
        Args:
            employee_name: Name of the employee like John
        """
        employee_name = employee_name.lower().strip()

        query_result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=employee_name
        )

        query_embedding = np.array(
        query_result.embeddings[0].values,
        dtype=np.float32
        )

        top = []
        
        for item in employee_index:
            score = cosine_sim(query_embedding, item["embedding"])
            top.append((score, item["key"]))
 

        top3 = sorted(top, reverse=True)[:3]

        results = []
        
        for score, key in top3:
            emp = data[key]
            results.append({
                "name": emp["name"],
                "email": emp["email"],
                "role": emp["role"],
                "department": emp["department"],
            })

        return json.dumps(results)

        # print(employee_name)
        # if data[employee_name]:
        #     return data[employee_name]
        # else:
        #     return "Employee doesnt exist in the directory"

server = AgentServer()

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        stt="assemblyai/universal-streaming:en",
        llm=groq.LLM(model="llama-3.3-70b-versatile"),
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