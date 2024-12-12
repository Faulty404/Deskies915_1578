from aiohttp import web
import json
from aiortc import RTCPeerConnection, VideoStreamTrack
import asyncio
import logging

pcs = set()

async def offer(request):
    params = await request.json()
    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        if pc.iceConnectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    await pc.setRemoteDescription(params["sdp"])
    await pc.setLocalDescription(await pc.createAnswer())

    return web.Response(
        content_type="application/json",
        text=json.dumps({"sdp": pc.localDescription})
    )

async def cleanup():
    while True:
        await asyncio.sleep(10)
        for pc in list(pcs):
            if pc.iceConnectionState == "closed":
                pcs.discard(pc)

app = web.Application()
app.router.add_post("/offer", offer)
app.on_shutdown.append(cleanup)

web.run_app(app, port=8080)

logging.basicConfig(level=logging.DEBUG)

@app.post("/offer")
async def offer(request):
    try:
        data = await request.json()
        logging.debug(f"Received offer: {data}")
        # Server logic here
    except Exception as e:
        logging.error(f"Error processing offer: {e}")
        return web.Response(status=500, text="Internal Server Error")
