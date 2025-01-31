## Setup for Deepseek Repo analyzer

To run this project, follow these steps:

```bash
# Clone the repository
git clone "[Repo Link]"
cd "[Repo Location]"

# Create and activate virtual environment
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate

# Add new requirements
pip freeze > requirements.txt

# Install dependencies
pip install -r requirements.txt

# Start the application
uvicorn app.main:app --reload --port 3001
```
