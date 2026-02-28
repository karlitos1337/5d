# In this file, you can set the configurations of the app.


# config related to logging must have prefix LOG_
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_FILE = "app.log"
LOG_CONSOLE = True
LOG_FILE_MAX_BYTES = 10485760
LOG_FILE_BACKUP_COUNT = 3

LLM_MODEL_TYPE = "openai"
LLM_MODEL = "gpt-4o-mini"
# Only required for OLLAMA models
LLM_API_URL = ""
