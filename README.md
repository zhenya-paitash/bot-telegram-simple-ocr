
# Telegram OCR Bot

## What is OCR?

OCR stands for Optical Character Recognition. It's a technology that converts text from images into editable and searchable text. This allows you to extract text from photos, scanned documents, or any other image containing written content.

## Features

- OCR processing using Tesseract
- Docker support for containerization
- Environment configuration support

## Prerequisites

- Python 3.x
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/zhenya-paitash/bot-telegram-simple-ocr.git
cd bot-telegram-simple-ocr
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
- Copy `.env.example` to `.env`
- Edit `.env` with your configuration values

## Running the Bot

### Local Development
```bash
python bot.py
```

### Docker
```bash
docker build -t bot-telegram-simple-ocr .
docker run -d --env-file .env --name bot-telegram-simple-ocr bot-telegram-simple-ocr
```

## License

This project is licensed under the terms of the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
