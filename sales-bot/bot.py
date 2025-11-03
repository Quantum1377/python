import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN

# Função para mostrar produtos
async def vendas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("data/sales.json", "r") as f:
        data = json.load(f)
    
    mensagem = "🛒 *Produtos disponíveis:*\n\n"
    for produto in data["products"]:
        mensagem += f"{produto['name']} - Estoque: {produto['stock']} - R$ {produto['price']}\n"
    
    await update.message.reply_text(mensagem, parse_mode='Markdown')

# Função para checar estoque de um produto
async def estoque(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Digite o nome do produto. Ex: /estoque SD Card 64GB")
        return

    produto_nome = " ".join(args)
    with open("data/sales.json", "r") as f:
        data = json.load(f)
    
    for produto in data["products"]:
        if produto['name'].lower() == produto_nome.lower():
            await update.message.reply_text(f"Produto: {produto['name']}\nEstoque: {produto['stock']}")
            return

    await update.message.reply_text("Produto não encontrado.")

# Função start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Eu sou o Bot de Vendas.\nUse /vendas para ver produtos.")

# Configuração do bot
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("vendas", vendas))
app.add_handler(CommandHandler("estoque", estoque))

print("Bot iniciado...")
app.run_polling()
