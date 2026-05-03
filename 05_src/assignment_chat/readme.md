# Initial Set Up
___________________________________________________
Getting Environment Variables and setting up chat
The app loads the .secrets file to access the OPENAI_API_KEY.
If the key is missing, the program stops immediately.

The script initializes a chat model using OpenAi and gpt-4o-mini
__________________________________________________
Service #1 Bored API
__________________________________________________
This simple chat app, establishes a connection with OpenAI's chat API, but using a local Gradio interface. The intent is to build a chatbot that can give ideas to bored users about what random activities to try.
Steps inside get_activity():
- Send a GET request to
https://www.boredapi.com/api/activity
- Parse the JSON response into a Python dictionary
- Extract fields such as "activity" and "type"
- Transform the raw API data into a natural‑language sentence
- Return the rewritten text to the user
- Inside the chat function, the system checks the user’s message:If the message contains keywords like “bored” or “activity”, the chatbot bypasses the LLM and directly returns the Service 1 result.
Gradio stores messages as dictionaries.
LangChain expects HumanMessage and AIMessage objects.
The script loops through the history and converts each message into the correct format.
The final step launches a browser‑based chat UI using:
gr.ChatInterface(fn=simple_chat, type="messages").launch()
__________________________________________________
Service #2
__________________________________________________

Service 2 provides the user to 'find' or 'search' anything in the chesterton.txt file
using semantic search.
The user query must contain the words 'search' or find'
How the semantic_search function works 

The chesterton text is read through a .txt file, chunked and embedded using vector embeddings found in embed.py
The embeddings and generated and stored in the same folder (vector store) so that they dont need to be generated each time.

The responsed generated from the user query is presented in natural language. 

How the chat function works for service 2:
When a user enters a query that contains the words 'find' or 'search' in the chatbox,
then the query will be sent to def semantic_search 
The embeddings will also be applied to the user query to convert the query into vector, and then the similarity search method will be used to find nearest 3 matches between embedded query and embedded database. 
The responses generated will be displayed to user in natural language.
__________________________________________________
Service #3
__________________________________________________
1. Service 3 provides weather information using a real public weather API.  
2. The service uses OpenAI function calling to allow the model to request structured weather data.  
3. The service defines a function schema named get_weather that includes one required parameter called city.  
4. When the user asks about weather, the model is allowed to call the get_weather function automatically.  
5. The get_weather function first sends a request to the Open Meteo geocoding API to convert the city name into latitude and longitude coordinates.  
6. After obtaining the coordinates, the function sends a second request to the Open Meteo weather API to retrieve the current weather conditions.  
7. The function returns the current temperature, wind speed, and other available weather fields from the API response.  
8. The chatbot receives the function result and formats it into a natural language response for the user.  
9. This service demonstrates the use of OpenAI function calling by allowing the model to decide when to call the function and by passing structured arguments to the function.  
10. This service satisfies the assignment requirement for a tool based on function calling and shows how external data can be integrated into the chatbot workflow.

__________________________________________________
How simple_chat works in assignment_chat
__________________________________________________

1. The simple chat function acts as the central routing system for all user messages and determines which service should respond.  
2. The function begins by applying guardrails that block attempts to access or reveal the system prompt.  
3. The guardrails check for phrases such as “system prompt,” “your instructions,” “your rules,” “your configuration,” and similar attempts to modify or expose internal instructions.  
4. If any of these phrases appear in the user message, the function immediately returns a refusal message and does not process the request further.  
5. The function also includes guardrails that block restricted topics required by the assignment.  
6. These restricted topics include cats, dogs, horoscopes, zodiac signs, and Taylor Swift.  
7. If the user message contains any restricted topic, the function returns a refusal message and does not continue to other services.  
8. After guardrails are applied, the function checks for keywords that trigger Service 1, which provides an activity suggestion using a public API.  
9. If the message contains keywords related to boredom or activities, the function calls Service 1 and returns its output.  
10. If the message does not match Service 1, the function checks for keywords that trigger Service 2, which performs semantic search using the Chroma vector store.  
11. If the message contains 'search' or 'find'keywords, the function calls Service 2 and returns the retrieved information.  
12. If the message does not match Service 1 or Service 2, the function checks for weather related keywords that trigger Service 3.  
13. When Service 3 is triggered, the function allows the model to use OpenAI function calling to request structured weather data.  
14. If the model returns a function call, the function extracts the arguments, calls the weather API helper function, and returns the formatted weather result.  
15. If none of the service triggers match, the function defaults to normal chat mode using the language model.  
16. In normal chat mode, the function reconstructs the conversation history, appends the new user message, sends it to the model, and returns the model’s response.
