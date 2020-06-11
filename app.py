#!/usr/bin/env python3

from flask import Flask, render_template, url_for, request
import os
import requests
import youtube_dl
import json

app = Flask(__name__)


app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/download", methods=['POST'])
def download():
    video_link = request.form['video_link']
    video_format = request.form['video_format'] 
    if request.method == 'POST' and video_link[:8] == "https://":
        dowonload_video(video_link, video_format)
        video_title = None
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_link, download=False)
            video_title = info_dict.get('title', None)
        data = {
            'status': 'success',
            'filename': video_title
        }
    else:
        data = {'status': 'failed'}
    response = app.response_class(response=json.dumps(data),
                                  status=200,
                                  mimetype='application/json'
                                  )
    return response


def dowonload_video(video_link, video_format):
    if video_format == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': './static/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        ydl_opts = {
            'outtmpl': './static/%(title)s.%(ext)s',
            'format': 'mp4',
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_link])
    
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=80, debug=True)