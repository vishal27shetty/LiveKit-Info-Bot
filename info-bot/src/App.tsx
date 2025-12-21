import { useState, useEffect } from 'react';
import {
  LiveKitRoom,
  RoomAudioRenderer,
  ConnectionState,
} from "@livekit/components-react";
import "@livekit/components-styles"; 

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
      <div style={{ padding: 20 }}>
        <h3>LiveKit Basic UI</h3>

        {/* shows Connecting / Connected / Disconnected */}
        <ConnectionState />

        {/* required to hear audio */}
        <RoomAudioRenderer />
      </div>
    </LiveKitRoom>
  );
}

export default MyLiveKitApp;