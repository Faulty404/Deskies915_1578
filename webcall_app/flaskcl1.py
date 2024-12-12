import asyncio
import aiohttp
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer

def create_local_media():
    return MediaPlayer("/dev/video0")  # Adjust for your OS if needed

async def run_client(server_url):
    pc = RTCPeerConnection()
    player = None

    @pc.on("track")
    async def on_track(track):
        print(f"Track {track.kind} received")

    try:
        # Create media player
        player = create_local_media()
        if player.video:
            pc.addTrack(player.video)

        # Create offer and set local description
        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)

        # Send offer to server
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{server_url}/offer",
                json={"sdp": pc.localDescription.sdp, "type": "offer"},
            ) as resp:
                if resp.status == 200:
                    answer = await resp.json()
                    await pc.setRemoteDescription(
                        RTCSessionDescription(sdp=answer["sdp"], type=answer["type"])
                    )
                    print("SDP answer received and set.")
                else:
                    print(f"Error: {resp.status}, {await resp.text()}")
                    return

        # Keep the connection alive for 60 seconds
        print("Connection established. Streaming for 60 seconds...")
        await asyncio.sleep(60)

    except asyncio.CancelledError:
        print("Task was cancelled.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Proper cleanup
        if player:
            player.video.stop()
        await pc.close()
        print("Resources released and connection closed.")

if __name__ == "__main__":
    server_url = "http://172.20.10.8:5000"  # Replace with your server's IP and port
    try:
        asyncio.run(run_client(server_url))
    except KeyboardInterrupt:
        print("Client interrupted. Exiting.")
