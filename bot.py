import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
from PIL import Image
import pytesseract
import os
from langdetect import detect, LangDetectException
import re
from typing import List, Dict

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class TextAnalyzer:
    @staticmethod
    def is_code(text: str) -> bool:
        code_keywords = ['def ', 'class ', 'import ', 'from ', 'return ', 'if ', 'else ', 'for ', 'while ']
        command_keywords = ['$ ', '# ', '> ', 'sudo ', 'git ', 'docker ', 'python ']
        
        if any(keyword in text for keyword in code_keywords + command_keywords):
            return True
            
        code_chars = r'[{}();=<>+\-*/%\[\]]'
        return len(re.findall(code_chars, text)) > 2

    @staticmethod
    def is_command(text: str) -> bool:
        return any(text.strip().startswith(cmd) for cmd in ['$', '#', '>', 'sudo ', 'git ', 'docker '])

    @staticmethod
    def detect_language(text: str) -> str:
        try:
            return detect(text)
        except LangDetectException:
            return 'en'

    @staticmethod
    def analyze_text(text: str) -> Dict:
        if not text.strip():
            return {'type': 'empty', 'content': text}
            
        if TextAnalyzer.is_command(text):
            return {'type': 'command', 'content': text}
            
        if TextAnalyzer.is_code(text):
            return {'type': 'code', 'content': text}
            
        return { 'type': 'text', 'language': TextAnalyzer.detect_language(text), 'content': text }

class ImageProcessor:
    @staticmethod
    def preprocess_image(image: Image.Image) -> Image.Image:
        image = image.convert('L') # up contrast & sharpness
        return image

    @staticmethod
    def extract_text(image: Image.Image) -> str:
        custom_config = r'--oem 3 --psm 6 -l rus+eng'
        return pytesseract.image_to_string(image, config=custom_config)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hi! Send me an image with text and I\'ll try to recognize it.')

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        photo_file = await update.message.photo[-1].get_file()
        image_path = 'temp_image.jpg'
        await photo_file.download_to_drive(image_path)
        
        # processing image
        image = Image.open(image_path)
        processor = ImageProcessor()
        processed_image = processor.preprocess_image(image)
        text = processor.extract_text(processed_image)
        
        if not text.strip():
            await update.message.reply_text("❌ Text could not be recognized.")
            return
        
        # analyze text
        analyzer = TextAnalyzer()
        analysis = analyzer.analyze_text(text)
        
        # Generate response
        response = "📄 Recognized text:\n\n"
        response += f"```\n{analysis['content']}\n```\n\n"
        
        if analysis['type'] == 'command':
            response += "🔧 Looks like a terminal command\n"
        elif analysis['type'] == 'code':
            response += "💻 Looks like code\n"

        # Hints
        suggestions = ["Check syntax",
                       "Try running command",
                       "Check logs",
                       "Update dependencies",
                       "Check permissions"]
        
        response += "\n💡 Possible actions:\n" + "\n".join(f"• {s}" for s in suggestions)
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        await update.message.reply_text("❌ An error occurred while processing the image.")

def main() -> None:
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image)) 
    application.run_polling()

if __name__ == '__main__':
    main()
