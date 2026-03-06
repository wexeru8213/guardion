import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from fastapi import FastAPI, Request
import uvicorn

logging.basicConfig(level=logging.INFO)

TOKEN = "8714788178:AAESpaVMRWQcJJFIjIDcA4PylTAlnYHIg4I"
ADMIN_ID = 8215840669
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")
PORT = int(os.getenv("PORT", 8000))

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("✅ Бот запущен и работает!")

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Эхо: {message.text}")

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    update = types.Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.on_event("startup")
async def on_startup():
    if RENDER_URL:
        webhook_url = f"{RENDER_URL}/webhook"
        await bot.set_webhook(webhook_url)
        logging.info(f"✅ Веб-хук установлен на {webhook_url}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
