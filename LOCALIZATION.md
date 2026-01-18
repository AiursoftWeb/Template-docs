```bash
OLLAMA_API_KEY="CONFIDENTIAL"
dotlang folder-translate -s ./zh/ -d ./en/ -k -l en_US -e md -r  --model "qwen3:30b-a3b-instruct-2507-q8_0" --token $OLLAMA_API_KEY --instance "https://ollama.aiursoft.com/api/chat/completions"
```