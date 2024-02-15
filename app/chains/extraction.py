from langchain.chains import create_extraction_chain

from ..dependencies.ollama_functions_model import ollama_functions_model

# demo from https://python.langchain.com/docs/integrations/chat/ollama_functions#using-for-extraction

# Schema
schema = {
    "properties": {
        "name": {"type": "string"},
        "height": {"type": "integer"},
        "hair_color": {"type": "string"},
    },
    "required": ["name", "height"],
}

extraction_chain = create_extraction_chain(
    schema,
    ollama_functions_model,
).with_types(input_type=str)
