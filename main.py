from flask import Flask, render_template , request
import uuid
from werkzeug.utils import secure_filename
import os



ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'user_uploads'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create" , methods =["GET" , "POST"])
def create():
    myid = uuid.uuid1()
    if request.method == "POST":
        print(request.files.keys())
        rec_id = request.form.get("uuid")
        desc = request.form.get("text")
        input_files = []
        for key , item in request.files.items():
            print(key , item)
            # Upload The files
            file = request.files[key]
            if file:
                filename = secure_filename(file.filename)
                if(not (os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'] , str(rec_id))))):
                    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'] , str(rec_id)))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'] , str(rec_id) , filename))
                input_files.append(file.filename)
            #Capture a descripyion and save it to a file 
            with open(os.path.join(app.config['UPLOAD_FOLDER'] , str(rec_id) , "desc.txt") , "w") as f:
                f.write(desc)

        # Save input.txt in correct format for FFmpeg
        with open(os.path.join(app.config['UPLOAD_FOLDER'] , str(rec_id) , "input.txt"), "w") as f:
            for i, filename in enumerate(input_files):
                f.write(f"file '{filename}'\n")
                if i != len(input_files) - 1:
                    f.write("duration 1\n")

    return render_template("create.html" , myid = myid)

@app.route("/gallery")
def gallery():
    reels = os.listdir("static/reels")
    print(reels)

    return render_template("gallery.html" , reels = reels)

if __name__ == "__main__":
    app.run(host = "0.0.0.0" , debug=True)