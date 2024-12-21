from huggingface_hub import InferenceClient

# Initialize the client with your API key
client = InferenceClient(api_key="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")

# Initialize chat history with a predefined context
chat_history = [
    {"role": "system", "content": "You are a therapy bot. Listen attentively to the user and reply in a comforting and professional tone."}
]
model_name = "mistralai/Mistral-Nemo-Instruct-2407"


def chat_with_model(user_input):
    global chat_history

    # Add user input to chat history
    chat_history.append({"role": "user", "content": user_input})

    # Make the API call
    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=chat_history,
            max_tokens=500
        )
        model_response = completion.choices[0].message["content"]

        # Add model's response to chat history
        chat_history.append({"role": "assistant", "content": model_response})

        return model_response, len(chat_history)
    except Exception as e:
        return f"Error: {e}", len(chat_history)


def give_analysis(chat_history, emotion_list):
    try:
        # Use placeholder content if chat history or emotion list is empty
        if not chat_history:
            chat_history = [
                {"role": "system", "content": "You are a helpful therapy bot."},
                {"role": "assistant", "content": "Hello, I'm here to help you. How are you feeling today?"}
            ]

        if not emotion_list:
            emotion_list = ["neutral"]  # Placeholder emotion

        # Prepare the input prompt for the model
        input_prompt = (
            "The following is the user's chat history with the therapy bot:\n\n"
            + " ".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat_history]) + "\n\n"
            + "The following is a list of detected facial emotions throughout the session, in order from start to end:\n\n"
            + ", ".join(emotion_list) + "\n\n"
            + "Based on the chat history and the detected emotions, generate an insightful analysis about how the user is likely feeling "
              "by the end of the chat. Keep the response concise and around 100 words. Your response should be addressing the user directly."
        )

        completion = client.text_generation(
            model=model_name, prompt=input_prompt, max_new_tokens=500
        )

        return completion
    except Exception as e:
        return f"Error in analysis: {e}"
