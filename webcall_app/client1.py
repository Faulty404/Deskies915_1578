import cv2
import asyncio
import aiohttp
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer

# Create a local media source (e.g., webcam)
def create_local_media():
    return MediaPlayer("/dev/video0")  # For Linux

async def run():
    pc = RTCPeerConnection()
    player = None

    @pc.on("track")
    async def on_track(track):
        print(f"Track {track.kind} received")
        # Example: Handle the received track (e.g., save or display it)
        pass

    try:
        # Access webcam
        player = create_local_media()
        if player.video:
            pc.addTrack(player.video)

        # Create an SDP offer
        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)

        # Send the offer to the server and get the answer
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://172.20.10.8:8080/offer",
                json={"sdp": pc.localDescription.sdp, "type": "offer"}
            ) as resp:
                if resp.status == 200 and resp.headers.get("Content-Type") == "application/json":
                    answer = await resp.json()
                    await pc.setRemoteDescription(
                        RTCSessionDescription(sdp=answer["sdp"], type=answer["type"])
                    )
                    print("SDP answer received and set.")
                else:
                    print(f"Unexpected response: {resp.status}, {await resp.text()}")
                    return

        # Keep the connection alive for a while
        print("Connection established. Streaming for 60 seconds...")
        await asyncio.sleep(60)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Cleanup resources
        if player:
            player.__del__()  # Properly release the MediaPlayer
        await pc.close()
        print("Resources released and connection closed.")

if __name__ == "__main__":
    asyncio.run(run())
