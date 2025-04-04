# WhatsApp Chat Analyzer

## Overview
WhatsApp Chat Analyzer is a Streamlit-based web application that allows users to upload their WhatsApp chat files and gain insights into their messaging behavior. It provides statistics such as message count, word usage, media sharing, and activity timelines.

## Features
- **Upload and Analyze WhatsApp Chats**: Supports .txt file uploads of chat history.
- **User-wise Analysis**: View statistics for individual users or overall group conversations.
- **Message Statistics**: Get details on total messages, words, media, and links shared.
- **Time-based Trends**: Analyze messaging trends over months, weeks, and days.
- **Most Common Words**: Generate word clouds and frequency charts.
- **Emoji Analysis**: Identify the most frequently used emojis.
- **Active User Analysis**: Find the most active participants in a group chat.
- **Heatmaps**: Visualize chat activity using heatmaps.

## Installation
To run this project locally, follow these steps:

### Prerequisites
Ensure you have Python installed on your system.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/whatsapp-chat-analyzer.git
   cd whatsapp-chat-analyzer
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage
1. Open the Streamlit web interface.
2. Upload your WhatsApp chat file (.txt format).
3. Select a user or view overall chat statistics.
4. Click "Show Analysis" to generate insights.

## Project Structure
```
whatsapp-chat-analyzer/
│-- app.py               # Main Streamlit app
│-- helper.py            # Helper functions for data processing
│-- preprocessor.py      # Preprocessing functions (not provided in the snippet)
│-- stop_hinglish.txt    # Stopwords for filtering common words
│-- requirements.txt     # Dependencies
```

## Dependencies
- `streamlit`
- `matplotlib`
- `seaborn`
- `pandas`
- `wordcloud`
- `collections`
- `emoji`
- `urlextract`

## License
This project is licensed under the MIT License.

## Acknowledgments
Inspired by data visualization techniques and chat analytics.

## Author
Developed by Renuja.

---


