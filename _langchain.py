from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

from audioGen import audioGen
import os

# Your PAT (Personal Access Token) can be found in the portal under Authentification in clarifai
os.environ['PAT'] = 'aca3bbf0c7c446f99d7e30fc894bd61b'

# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = 'meta'
APP_ID = 'Llama-2'
# Change these to whatever model and text URL you want to use
MODEL_ID = 'llama2-13b-chat'
MODEL_VERSION_ID = '79a1af31aa8249a99602fc05687e8f40'
# Here we are creating a prompt template for the Llama2. 
# STORY_LINES = "There's a llama in my garden. It's eating all my flowers. I'm going to call the police."
# RAW_TEXT = f"<s>[INST] <<SYS>>You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.<</SYS>>Given this Story:'{STORY_LINES}' write a very short prompt describing a melody that would fit the story. Here's a template for a prompt: 110bpm 64kbps 16khz lofi hiphop summer smooth [/INST]"

# Here we are creating a function to generate a prompt for the AudioGen model.
# The function takes three parameters: `MODEL_ID`, `MODEL_VERSION_ID` and `RAW_TEXT`.
# The `MODEL_ID` parameter is the model you want to use.
# The `MODEL_VERSION_ID` parameter is the version of the model.
# The `RAW_TEXT` parameter is the instuction to make the prompt
def get_response(STORY_LINES):
    RAW_TEXT = f"<s>[INST] <<SYS>>You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.<</SYS>>Given this Story:'{STORY_LINES}' write a very short prompt of one sentence describing a melody that would fit the story. Here's an example for a prompt I expect you answer me with: 110bpm 64kbps 16khz lofi hiphop summer smooth [/INST]"
    # Here we are creating a LLM (Llama2 in our case).
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + os.environ.get("PAT")),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=RAW_TEXT
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")

    # Since we have one input, one output will exist here
    output = post_model_outputs_response.outputs[0]
    response = output.data.text.raw # This is the response from the LLM (Llama2 in our case).
    
    # audioGen(output.data.text.raw)  # This takes the response from the LLM and generates a background music for the storyline.

    print("Completion:\n")

    
    return response
