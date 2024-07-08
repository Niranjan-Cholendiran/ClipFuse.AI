# ClipFuse.AI

In today's digital age, sharing experiences through video content on social media has become the primary mode of expression. However, **barriers such as the need for video editing skills, software knowledge, and the time required to create videos often limit many individuals from sharing their stories.**

Isn't this disparity unfair? Not anymore. **ClipFuse.AI** addresses these challenges by **empowering users without any editing background to effortlessly create vlog-style videos in just 5 minutes with a few simple clicks.** The tool includes animations and the user's own voice voiceover, generated without the need for them to record it manually.

This innovation aims to democratize video creation, enabling everyone to share their beautiful moments seamlessly, thereby breaking down traditional barriers to digital storytelling.

Find out more:
* [YouTube Introduction](https://youtu.be/vMr8ML_7gsw?si=pQf2pmzZx2Y0g_1q)

  ![Architecture](https://github.com/Niranjan-Cholendiran/ClipFuse.AI/assets/78549555/2e2776b8-6d4a-4a76-b6d6-ca3c3b039ed9)


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

### Step 4: Download ImageMagick

Download ImageMagick from the official website: [ImageMagick Download Page](https://imagemagick.org/script/download.php)

### Step 5: Setup Environment Variables:

Create a `.env` file in the root directory and add the following keys:

```plaintext
PLAYHT_USER_ID= <your_playht_userid>
PLAYHT_SECRET_KEY= <your_playht_secretkey>
OPENAI_API_KEY= <your_openapi_key>
IMAGEMAGICK_PATH= <your_imagemagic_path>
```
Generate your free PlayHT keys [here](https://play.ht/studio/api-access) and OpenAI API key [here](https://openai.com/index/openai-api/). You can use a paid version of the APIs for faster processing, but the free versions work reasonably well.

Find the ImageMagick's executable location using the following terminal command. In most cases, it will be `C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe` for Windows OS.
```bash
which magick
```

## Running the project

Once you have completed the steps above, you can run the project using:
```bash
python '\02. Scripts\app.py'
```
Replace `app.py` with the entry point of your project.

-----

Happy coding! If you encounter any issues, please open an issue in this repository or message me on [LinkedIn](https://www.linkedin.com/in/niranjan-cholendiran/).

