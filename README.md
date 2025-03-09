---
title: USA Travel Guide AI Assistant
emoji: 🧳
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "5.20.0"
app_file: app.py
pinned: false
license: mit
---

# USA Travel Guide AI Assistant

An intelligent AI travel assistant that helps tourists plan trips and navigate destinations within the United States.

## Try It Out!

You can interact with this assistant directly in this Hugging Face Space. Just type your travel-related question in the chat box below.

## Features

- 🕒 Real-time timezone information
- 🌤️ Weather forecasts for US destinations
- 💰 Travel budget estimation
- 🏨 Hotel recommendations
- 🍽️ Restaurant suggestions
- 🎭 Local attractions based on traveler profiles
- 🚗 Transportation planning between cities
- 🚌 Local transportation options
- 🔒 Safety information for destinations
- 🔍 Web search capabilities for up-to-date information
- 🖼️ Image generation for attractions

## Sample Queries

- "What's the weather like in Miami?"
- "I need to travel from New York to Chicago. What are my options?"
- "Find me family-friendly attractions in Orlando."
- "What's the estimated budget for 3 people visiting San Francisco for 5 days?"
- "Are there any safety concerns in Las Vegas?"
- "Can you recommend restaurants in Austin?"
- "What's the current time in Los Angeles?"

## How It Works

This assistant uses the Qwen language model with specialized tools to answer travel-related questions. It prioritizes using domain-specific tools for different query types before falling back to web search.

## Tools and Technologies

- **smolagents**: Framework for building AI agents
- **Hugging Face**: Provides the language model (Qwen/Qwen2.5-Coder-32B-Instruct)
- **Gradio**: Creates the user interface
- **DuckDuckGo Search**: Enables web search capabilities

## Source Code

The source code for this project is available on [GitHub](https://github.com/YOUR_USERNAME/usa-travel-guide).

## License

MIT

## 🌟 Features

This AI assistant can help with various aspects of travel planning in the USA:

- **🌤️ Weather Information**: Get current weather forecasts for any US city
- **🏨 Hotel Recommendations**: Find accommodations that match your budget and preferences
- **🗽 Attractions Discovery**: Explore popular attractions based on your interests
- **🚗 Transportation Planning**: Get advice on how to travel between cities
- **🚌 Local Transportation**: Learn about public transit, ride-sharing, and other options
- **💰 Budget Estimation**: Calculate estimated costs for your trip
- **🕒 Time Zone Information**: Get current time across US time zones
- **🔒 Safety Information**: Learn about safety considerations for different cities

## 📋 Requirements

- Python 3.8+
- Required packages listed in `requirements.txt`
- Hugging Face API token for model access

## 🚀 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/usa-tour-guide.git
   cd usa-tour-guide
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up your Hugging Face API token:
   - Create a `.env` file in the project root based on `.env.example`
   - Add your token: `HUGGING_FACE_TOKEN=your_token_here`
   - Get your token from: https://huggingface.co/settings/tokens

## ⚠️ Model and API Considerations

This project uses the Qwen/Qwen2.5-Coder-32B-Instruct model from Hugging Face, which requires:
- A valid Hugging Face API token with READ access or higher
- Sufficient API credits for inference

The application includes a fallback mechanism that uses a `MockModel` when:
- API credits are exhausted
- The API is temporarily unavailable
- Network issues prevent API access

This ensures the application remains functional for demonstration purposes even when the primary model is unavailable.

## 🔄 Alternative Models

If you encounter limitations with the Qwen 32B model, you can modify `app.py` to use alternative models:

1. Smaller Qwen variants:
   - Qwen/Qwen2.5-7B-Instruct
   - Qwen/Qwen2-7B-Instruct

2. Other open source models:
   - mistralai/Mistral-7B-Instruct-v0.2
   - mistralai/Mixtral-8x7B-Instruct-v0.1
   - meta-llama/Llama-3-8B-Instruct

Edit the model initialization in `app.py` to change the model.

## 🎮 Usage

### Starting the application

Windows:
```bash
start.bat
```

Linux/macOS:
```bash
./start.sh
```

Or run directly with Python:
```bash
python app.py
```

### Sample Questions

Here are some examples of questions you can ask the assistant:

- "What's the weather like in Miami this week?"
- "Can you help me find hotels in Chicago for a family of 4?"
- "What are some historical attractions in Boston?"
- "How can I get from San Francisco to Los Angeles?"
- "I'm traveling to New York with my partner for 5 days. What's our estimated budget?"
- "What's the local transportation like in Washington DC?"
- "Is Seattle safe for solo travelers?"

## ⚙️ Configuration

You can customize the assistant's behavior by modifying the `config.yaml` file:

```yaml
model:
  id: "Qwen/Qwen2.5-Coder-32B-Instruct"  # The model to use
  max_tokens: 2096                      # Maximum tokens per response
  temperature: 0.7                      # Creativity level (0.0-1.0)

app:
  title: "USA Tour Guide AI Assistant"   # Application title
  description: "An AI travel assistant"  # Application description

features:
  weather: true       # Enable weather information
  hotels: true        # Enable hotel recommendations
  attractions: true   # Enable attractions discovery
  transportation: true # Enable transportation planning
  budget: true        # Enable budget estimation

search:
  enabled: true       # Enable web search capability
  max_results: 5      # Maximum search results to return
```

## 📦 Project Structure

- `app.py`: Main application file with agent and tools setup
- `Gradio_UI.py`: User interface implementation using Gradio
- `config.yaml`: Configuration settings
- `requirements.txt`: Package dependencies
- `start.bat`/`start.sh`: Startup scripts

## 🔧 Customization

### Adding Custom Tools

You can add more tools by:

1. Creating a new function with the `@tool` decorator in `app.py`
2. Adding it to the `init_tools()` function
3. Updating the `config.yaml` file to enable/disable the tool

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💬 Acknowledgements

This project uses the `smolagents` framework for agent functionality, Hugging Face models for AI capabilities, and Gradio for the user interface. 