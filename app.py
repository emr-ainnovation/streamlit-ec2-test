import streamlit as st # type: ignore
import boto3 # type: ignore
import json

# Nombre del perfil de AWS al que quieres conectarte
aws_profile = 'ainnovation'

# Crear una sesión en AWS utilizando el perfil especificado
session = boto3.Session(profile_name=aws_profile, region_name="us-east-1")

# Crear el cliente para interactuar con AWS Bedrock
bedrock_client = session.client('bedrock-agent-runtime')

# ID de tu agente de AWS Bedrock
agent_id = "Q1QRNJHTYS"
agent_alias_id = "OXOJLMFYSB"
session_id = "test-001"

# Función para obtener respuesta del agente de AWS Bedrock
def invokeAgent(agent_id,agent_alias_id,prompt,session_id):
    response = bedrock_client.invoke_agent(
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        inputText=prompt,
        sessionId=session_id
    )
    return response

st.title("💬 Asistente de biblias para series de animación")
   
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "¿Cómo puedo ayudarte?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Escribe tu mensaje..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)    
    response = invokeAgent(agent_id, agent_alias_id, prompt, session_id)
    completion = ""
    if(response.get("completion")):
       for event in response.get("completion"):
            chunk = event["chunk"]
            completion = completion + chunk["bytes"].decode('utf-8')
    if(completion):
        st.session_state.messages.append({"role": "assistant", "content": completion})
        st.chat_message("assistant").write(completion)