import json
from typing import Any
from app.core import predict
from app.core.secret import OPENAI_API_KEY
from app.model.survivor import Survivor
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
from langchain_openai.chat_models import ChatOpenAI

memoria = ConversationBufferMemory()
llm_conversation = ChatOpenAI(model="gpt-4-turbo",
                              api_key=OPENAI_API_KEY,
                              temperature=0.3)

llm2_data_extractor = ChatOpenAI(model="gpt-4-turbo",
                                 api_key=OPENAI_API_KEY,
                                 temperature=0)

template_chat = """
Eres un chatbot encargado de recolectar las siguietes preguntas en el orden especificado.
Vas a iniciar saludando al usuario
Siempre vas a mantener al usuario dentro del contexto de la conversacion.
Cuando ya tengaas todos los datos le diras al usuario `gracias por participar` y terminaras la conversacion.

### Preguntas:
- Cual es tu edad?
- Cual es tu sexo (M/F)?
- Cual es tu clase de pasajero (1, 2, 3)?
- Cual es tu tarifa (0 a 100)?
- Cual es tu puerto de embarque (C, Q, S)?

### Historia:
{history}

### Ultimo mensaje del usuario:
{input}

"""

template_extractor = """
Eres el encargado de analizar la informacion recolectada y responder con el siguiente json:
- Debes response solo un texto en formato json
- Debes completar el json solo con los datos recolectados
- Debe cumplir con la siguiete estructura:

### Historia:
{history}

### Ultimo mensaje del usuario:
{input}

### JSON RESPONSE:

{{
    "pclass": int,
    "sex": int,
    "age": float,
    "fare": float,
    "port": str
}}


"""

prompt_chat = PromptTemplate(input_variables=[
    "history", "input"], template=template_chat)

prompt_extractor = PromptTemplate(input_variables=[
    "history", "input"], template=template_extractor)


async def chatting(message: str) -> str:
    conversation_chat = ConversationChain(
        llm=llm_conversation,
        prompt=prompt_chat,
        verbose=False,
        memory=memoria
    )
    response = conversation_chat.predict(input=message)
    chatEnded = True if "gracias por participar" in response.lower() else False

    if chatEnded:
        conversation_extractor = ConversationChain(
            llm=llm_conversation,
            prompt=prompt_extractor,
            verbose=False,
            memory=memoria
        )
        json_string = conversation_extractor.predict(
            input=message).replace("json", "").replace("```", "")
        json_object = json.loads(json_string)
        survivor = Survivor(**json_object)
        predition = await predict.predict(survivor)
        if predition:
            response = "Felicidades serias uno de los posibles sobrevivientes del Titanic"
        else:
            response = "Lo siento lo mas probable es que mueres en el Titanic"

    return response
