# ClipFuse.AI


## Prerequisites

- Python 3.7 or higher
- `pip` (Python package installer)

## Installation

### Step 1: Clone the Repository

First, clone the repository to your local machine using git:

```bash
git clone https://github.com/your-username/your-repo-name.git https://github.com/Niranjan-Cholendiran/ClipFuse.AI.git
cd your-repo-name
```

### Step 2: Install Required Packages

Install the necessary Python packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 3: Install FFMPEG

FFMPEG is a multimedia framework needed for processing audio and video files. Follow the instructions below to install it on your operating system.

**Windows:**

Follow this [video](https://youtu.be/JR36oH35Fgg?si=32yKMXuZKsAckeqX) for reference.
1. Download the latest FFMPEG release from.
2. Extract the downloaded zip file.
3. Add the `bin` folder to your system's PATH environment variable.

**macOS:**

Use Homebrew to install FFMPEG:
```bash
brew install ffmpeg
```
**Linux:**

Use the package manager for your distribution. For example, on Ubuntu:
```bash
sudo apt update
sudo apt install ffmpeg
```

### Step 4: Setup Environment Variables:

Create a `.env` file in the root directory and add the following secret codes:

```plaintext
PLAYHT_USER_ID= <your_playht_userid>
PLAYHT_SECRET_KEY= <your_playht_secretkey>
OPENAI_API_KEY= <your_openapi_key>
```
You can generate your PlayHT key [here](https://play.ht/studio/api-access).

## Running the project

Once you have completed the steps above, you can run the project using:
```bash
python '\02. Scripts\app.py'
```
Replace `app.py` with the entry point of your project.

-----

Happy coding! If you encounter any issues, please open an issue in this repository or message me on [LinkedIn](https://www.linkedin.com/in/niranjan-cholendiran/).

