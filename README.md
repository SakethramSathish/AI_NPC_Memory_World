# AI NPC Memory World

A sophisticated AI-powered simulation where NPCs (Non-Player Characters) have persistent memory, dynamic relationships, and the ability to gossip with each other about the player.

Built with **Streamlit**, **LangGraph**, **ChromaDB**, and **Google Gemini**.

## 🌟 Features

-   **🧠 Persistent Memory**: NPCs remember your past interactions using vector storage (ChromaDB).
-   **❤️ Dynamic Relationships**:
    -   Relationships evolve based on your interactions.
    -   AI analyzes the **impact** of your words (compliments vs. insults) and context (insulting a third party vs. the listener).
    -   Status ranges from **Hostile** to **Loyal**.
-   **🗣️ Gossip System**: NPCs talk to each other! If you do something noteworthy, one NPC might tell another, spreading your reputation.
-   **🎭 Distinct Personalities**: Each NPC has a unique personality and mood that affects their dialogue.
-   **📊 Real-time Dashboard**: View relationship scores, current moods, and a live gossip log.

## 🛠️ Technologies

-   **Frontend**: [Streamlit](https://streamlit.io/)
-   **LLM**: [Google Gemini Pro](https://ai.google.dev/)
-   **Orchestration**: [LangGraph](https://langchain-ai.github.io/langgraph/)
-   **Vector Database**: [ChromaDB](https://www.trychroma.com/)
-   **Embeddings**: Sentence Transformers (`all-MiniLM-L6-v2`)

## 🚀 Getting Started

### Prerequisites

-   Python 3.10+
-   A Google Cloud Project with the **Gemini API** enabled.

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/ai-npc-memory-world.git
    cd ai-npc-memory-world
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up configuration**:
    -   Create a `.env` file in the root directory.
    -   Add your Gemini API key:
        ```env
        GEMINI_API_KEY=your_api_key_here
        ```

### Running the App

Start the Streamlit server:

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`.

## 📂 Project Structure

-   `agents/`: Logic for NPC and Gossip agents.
-   `data/`: Stores `npc_profiles.json` and ChromaDB data.
-   `frontend/`: UI components for Streamlit.
-   `graphs/`: LangGraph state definitions and workflows.
-   `memory/`: ChromaDB interaction and memory retrieval logic.
-   `models/`: LLM wrapper configuration.
-   `utils/`: Helper functions for text analysis, scoring, and world state.

## 🎮 How to Play

1.  **Select an NPC** from the sidebar (e.g., Eldon or Mira).
2.  **Chat** with them! Ask questions, share stories, or be rude.
3.  **Watch the Status Panel**: See how their mood and your relationship score change in real-time.
4.  **Switch NPCs**: Talk to another character and check the **Gossip Log** to see if they've heard about your previous interactions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the GNU General Public License v3.0.
