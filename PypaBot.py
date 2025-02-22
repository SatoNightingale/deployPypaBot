from telegram.ext import Application, ContextTypes, MessageHandler, CommandHandler, filters
from telegram import Update

cuento = "¿Quieres que te haga el cuento de la buena Pypa?"

def main():
    bot = Application.builder().token("7939769480:AAHpVCAVbDWmFjxCGwq8EhI0dVzxxmgMLm4").build()
    
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echoPypa))
    bot.add_handler(CommandHandler("start", inicioPypa))
    bot.add_handler(CommandHandler("stop", detenerPypa))
    bot.add_handler(CommandHandler("help", ayudaPypa))
    
    bot.run_polling(allowed_updates=Update.ALL_TYPES)

    print("Iniciado")

async def echoPypa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Yo no te he dicho que "' + update.message.text + '", yo te dije que si quieres que te haga el cuento de la buena Pypa')
    
    print("Usuario", update.effective_user.username, "dijo:", update.message.text)

async def inicioPypa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(cuento)

    chat_id = update.message.chat_id
    context.job_queue.run_repeating(preguntarPypa, 14400, chat_id=chat_id, name=str(chat_id))
    
    print("Usuario", update.effective_user.username, "ha caido en la trampa")

async def preguntarPypa(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text=cuento)

async def detenerPypa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=chat_id, text='Ok ya dejo de joderte')
    job = context.job_queue.get_jobs_by_name(str(chat_id))
    job[0].schedule_removal()

    print("Usuario", update.effective_user.username, "ha cancelado el juego")

async def ayudaPypa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=chat_id, text="No hay ayuda, " + cuento)

    print("Usuario", update.effective_user.username, "ha solicitado ayuda. Pobre de el...")

if __name__ == '__main__':
    main()