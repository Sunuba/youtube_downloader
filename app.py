from flask import Flask, render_template, request
from pytube import YouTube

app = Flask(__name__)


class Video:
    def __init__(self, url = None):
        self.url = url

video = Video()

@app.route('/')
def index():
    return render_template('enter_url.html')


@app.route('/options', methods=['GET', 'POST'])
def show_options():
    if request.method == 'POST':
        try:
            url = request.form.get('url')
            video.url = url
            yt = YouTube(url)
            title = yt.title
            image = yt.thumbnail_url
            data = yt.streams.all()
        except:
            return render_template('error.html')

        return render_template('options.html', data=data, title=title, image=image)
    else:
        return 'Method not allowed!'


@app.route("/download/<int:itag>")
def download(itag):
    try:
        yt = YouTube(video.url)
        stream = yt.streams.get_by_itag(itag)
        stream.download()
    except:
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
