# video-subtitle-process

A website on which video(s) can be uploaded, processed in some manner (in the background) and then searched using the subtitles in that video as keywords.

For instance, if a 2 minute clip of a music video was uploaded, the application will parse it, apply subtitles to it and ensure that searching for a particular word or phrase returns the time segment within which the video has those phrases being mentioned.

1)Used the ccextractor binary for extracting subtitles from video. Note that using any API, etc for subtitle extraction is not allowed.

2. Further, after processing, the videos will be stored in **S3** and the search keywords (subtitles) in **DynamoDB**.

3. HTTP requests should has a maximum latency of approx 1 second.

4. The backend is written in **Django**. **Celery** for background tasks.

"Use this sample video file for running ccextractor”: https://drive.google.com/file/d/1gLi5ho33TIRNVZkSE-gD4S24zs6Xy1ci/view?usp=sharing

## How to start

- Clone the repo with `git clone https://github.com/aghosh0605/video-subtitle-process.git`
- cd into the folder `cd video-subtitle-process`
- Install the python dependencies `pip install -r requirements.txt` or `python3 -m pip install -r requirements.txt`
- cd into the Django project root directory `cd video_sub_parser`
- Run the below commands

`sudo apt-get install ccextractor` - Tested on ubuntu 20.04 LTS

```python
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

## Endpoints

### REST API Endpoints

```
POST /api/v1/subtitle               Add a subtitle
GET /api/v1/subtitle                Shows all subtitle details
GET /api/v1/subtitle/item_id        Shows subtitle details with ID
```

## Useful command snippet for Developers

```bash
ccextractor video_test.mp4 -out=ttxt
pip3 freeze > requirements.txt
```
