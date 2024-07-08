from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from werkzeug.utils import secure_filename
import video_maker  # Assuming you have a video_maker.py with a video_maker() function
import threading
import queue
import logging

# Create a queue to store progress messages
progress_queue = queue.Queue()

# Configure logging for app.py
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = 'video_creator_key' 
app.config['UPLOAD_FOLDER'] = r'02. Scripts\static\uploads'
app.config['FINAL_VIDEO_FOLDER'] = r'02. Scripts\static\uploads\final_video'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'descriptions'), exist_ok=True)
os.makedirs(app.config['FINAL_VIDEO_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        return redirect(url_for('upload', title=title))
    return render_template('index.html')

@app.route('/upload/<title>', methods=['GET', 'POST'])
def upload(title):
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        for i, file in enumerate(files):
            if file and allowed_file(file.filename):
                extension = file.filename.rsplit('.', 1)[1].lower()
                filename = f'media_{i+1}.{extension}'
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'images', filename)
                file.save(save_path)
        return redirect(url_for('reorder', title=title))
    return render_template('upload.html', title=title)

@app.route('/reorder/<title>', methods=['GET', 'POST'])
def reorder(title):
    image_files = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'images'))
    if request.method == 'POST':
        ordered_files = []
        for file in image_files:
            order = int(request.form[f'order_{file}'])
            ordered_files.append((order, file))
        ordered_files.sort()  # Sort based on the order numbers
        ordered_files = [file for _, file in ordered_files]  # Extract sorted file names
        # Save the ordered file list to pass to the next step
        session['ordered_files'] = ordered_files
        return redirect(url_for('record', title=title))
    return render_template('reorder.html', title=title, image_files=image_files)

@app.route('/record/<title>', methods=['GET', 'POST'])
def record(title):
    image_files = session.get('ordered_files', [])
    if request.method == 'POST':
        return redirect(url_for('generate', title=title))
    return render_template('record.html', title=title, image_files=image_files)

"""
@app.route('/save_audio/<int:index>', methods=['POST'])
def save_audio(index):
    audio_data = request.files['audio_data']
    filename = f'Descr_{index}.wav'
    audio_data.save(os.path.join(app.config['UPLOAD_FOLDER'], 'descriptions', filename))
    return '', 204
"""

@app.route('/save_audio/<int:index>', methods=['POST'])
def save_audio(index):
    audio_data = request.files['audio_data']
    original_filename = secure_filename(audio_data.filename)  # Secure filename for safety
    print("original_filename:", original_filename)
    extension = original_filename.rsplit('.', 1)[1].lower()  # Extract original extension
    filename = f'Descr_{index}.{extension}'
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'descriptions', filename)
    audio_data.save(save_path)
    print("save_path:", save_path)
    return '', 204

@app.route('/progress', methods=['GET'])
def progress():
    try:
        message = progress_queue.get_nowait()
        if message == "Video generation completed.":
            completed = True
        else:
            completed = False
        return jsonify({'message': message, 'completed': completed})
    except queue.Empty:
        if progress_queue.empty():
            return jsonify({'message': '', 'completed': False})
        else:
            message = progress_queue.get()
            return jsonify({'message': message, 'completed': False})

@app.route('/generate/<title>', methods=['GET'])
def generate(title):
    image_files = sorted(os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'images')))
    description_files = sorted(os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'descriptions')))
    number_of_segments = len(image_files)
    #print("number_of_segments:", number_of_segments)
    #print("description_files:", description_files)
    media_info_list = []
    for i in range(number_of_segments):
        #print("I:", i)
        #print("media_info_list:", media_info_list)
        image_file = image_files[i]
        description_file = description_files[i]
        media_format = 'IMAGE' if image_file.lower().endswith(('png', 'jpg', 'jpeg', 'gif')) else 'VIDEO'
        description_format = description_file.rsplit('.', 1)[1].lower()

        media_info = {
            "media_loc": os.path.join(app.config['UPLOAD_FOLDER'], 'images', image_file),
            "media_format": media_format,
            "description_audio_loc": os.path.join(app.config['UPLOAD_FOLDER'], 'descriptions', description_file),
            "description_audio_format": description_format,
            "description_text": None,
            "transcript_text": None,
            "transcript_start_sec": None,
            "transcript_end_sec": None
        }
        media_info_list.append(media_info)
    
    media_information = {
        "STARTER": {
            "title": title,
            "combined_description_audio_loc": None,
            "final_voiceover_loc": None,
            "bg_music_loc": r'02. Scripts\static\uploads\bg_music\Standard BG Music.mp3',
            "transcript_text": None,
            "transcript_start_sec": None,
            "transcript_end_sec": None,
            "number_of_segments": number_of_segments
        },
        "MEDIA_INFO": media_info_list
    }

    print(media_information)

    # Function to run video_maker function in a separate thread
    def run_video_maker(media_information):
        try:
            video_maker.video_maker(media_information, progress_queue)
            progress_queue.put("Video generation completed.")
        except Exception as e:
            progress_queue.put(f"Error during video generation: {str(e)}")
    # Start a new thread to run video_maker
    thread = threading.Thread(target=run_video_maker, args=(media_information,))
    thread.start()
    return render_template('generate.html', title=title)


@app.route('/result/<title>', methods=['GET'])
def result(title):
    video_path = os.path.join(app.config['FINAL_VIDEO_FOLDER'], 'final_video.m4a')
    return render_template('result.html', title=title, video_path=video_path)

if __name__ == '__main__':
    app.run(debug=True)