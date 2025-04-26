import asyncio
import websockets
import subprocess
import os
import pty

async def terminal_handler(websocket):
    # Lance un shell bash avec venv activé
    master_fd, slave_fd = pty.openpty()
    env = os.environ.copy()
    env['PS1'] = ''  # Prompt vide

    process = subprocess.Popen(
        ['bash'],
        preexec_fn=os.setsid,
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        env=env,
        cwd='/chemin/vers/ton/projet'  # Change ici !
    )

    # Active venv automatiquement
    os.write(master_fd, b"source venv/bin/activate\n")

    async def read_terminal():
        while True:
            await asyncio.sleep(0.1)
            try:
                output = os.read(master_fd, 1024).decode()
                await websocket.send(output)
            except OSError:
                break

    reader_task = asyncio.create_task(read_terminal())

    try:
        async for message in websocket:
            os.write(master_fd, message.encode())
    finally:
        process.terminate()
        reader_task.cancel()

async def main():
    async with websockets.serve(terminal_handler, "0.0.0.0", 8000, path="/ws/terminal/"):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
