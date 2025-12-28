import { useState, useEffect } from 'react';
import {
  LiveKitRoom,
  RoomAudioRenderer,
  AudioConference,
  useVoiceAssistant,
  BarVisualizer,
  FocusLayout,
} from "@livekit/components-react";
import "@livekit/components-styles"; 

function SimpleVoiceAssistant() {
  // Get the agent's audio track and current state
  const { state, audioTrack } = useVoiceAssistant();
  return (
    <div className="h-80">
      <BarVisualizer state={state} barCount={5} trackRef={audioTrack} style={{}} />
      <p className="text-center">{state}</p>
    </div>
  );
}

const MyLiveKitApp = () => {
  const [token, setToken] = useState("");
  
  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/token")
    .then((res) => res.json())
    .then((data) => {
      setToken(data.token);
    });
  }, []);


  console.log("Token state:", token);
  return (

    <LiveKitRoom
      serverUrl={import.meta.env.VITE_LIVEKIT_URL}
      token={token}
      connect={true}
      audio={true}
      video={false}
    >
      <div style={{textAlign:'center'}}>
        <h3>LiveKit Basic UI</h3>
        {/* required to hear audio */}
        <RoomAudioRenderer />
   
        <SimpleVoiceAssistant />
        
        <AudioConference />
     
      </div>
    </LiveKitRoom>
  );
}

export default MyLiveKitApp;