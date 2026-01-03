# Nightscout MCP Server

An [MCP](https://modelcontextprotocol.io/) server that connects to your [Nightscout](http://www.nightscout.info/) instance. It exposes your diabetes data (glucose, treatments, profile, device status) to LLMs and provides tools for analyzing therapy settings using DIY Loop data.

## Features

### Resources
Access raw Nightscout data via standard MCP resources:
- `nightscout://entries`: Latest glucose entries (default: last 10).
- `nightscout://treatments`: Latest treatments (bolus, carbs, temp basals).
- `nightscout://profile`: Active insulin profile (Basal rates, ISF, CR).
- `nightscout://device_status`: Device status information (Pump battery, Loop status, IOB, COB).

### Tools
- `suggest_settings(hours=24)`: 
  - Analyzes data from a specified lookback period (default 24h).
  - Calculates statistics: Average Glucose, Time in Range (TIR).
  - integrates **Loop Data**: Analyzes average IOB (Insulin on Board) and COB (Carbs on Board) from `device_status`.
  - Provides basic heuristic suggestions (e.g., checking for resistance if high active insulin coincides with high glucose).

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/rustytek/nightscoutMCP.git
    cd nightscoutMCP
    ```

2.  **Create a Virtual Environment** (Recommended):
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Copy `.env.example` to `.env`:
    ```bash
    cp .env.example .env
    # or on Windows
    copy .env.example .env
    ```

2.  Edit `.env` and add your Nightscout credentials:
    ```ini
    NIGHTSCOUT_URL=https://your-nightscout-site.herokuapp.com
    API_SECRET=your_api_secret
    ```

## Usage

Run the server using Python:

```bash
python server.py
```

### Using with an MCP Client
Configure your AI assistant / MCP client to use this server.

**Command**: `python`
**Arguments**: `['/path/to/nightscoutMCP/server.py']`
(Ensure the environment variables or `.env` file are accessible to the client).

## Project Structure

- `server.py`: Main entry point. Defines MCP resources and tools.
- `nightscout.py`: HTTP Client for interacting with the Nightscout API V1.
- `analysis.py`: Logic for statistical analysis and therapy suggestions.
