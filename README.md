# video-subtitle-process

A website on which video(s) can be uploaded, processed in some manner (in the background) and then searched using the subtitles in that video as keywords.

For instance, if a 2 minute clip of a music video was uploaded, the application will parse it, apply subtitles to it and ensure that searching for a particular word or phrase returns the time segment within which the video has those phrases being mentioned.

1. Used the **ccextractor** binary for extracting subtitles from video. Note that using any API, etc for subtitle extraction is not allowed.

2. Further, after processing, the videos will be stored in **S3** and the search keywords (subtitles) in **DynamoDB**.

3. HTTP requests should has a maximum latency of approx 1 second.

4. The backend is written in **Django**. **Celery** for background tasks.

"Use this sample video file for running ccextractor”: https://drive.google.com/file/d/1gLi5ho33TIRNVZkSE-gD4S24zs6Xy1ci/view?usp=sharing

## How to start

### Demo video [![Watch the video](https://ecowiser-internship.s3.ap-south-1.amazonaws.com/vector-video-player-941434_1920.png)](https://ecowiser-internship.s3.ap-south-1.amazonaws.com/ecowiser_task.mp4)

- Clone the repo with `git clone https://github.com/aghosh0605/video-subtitle-process.git`
- cd into the folder `cd video-subtitle-process`
- Install the python dependencies `pip install -r requirements.txt` or `python3 -m pip install -r requirements.txt`
- cd into the Django project root directory `cd video_sub_parser`
- Run the below commands

`sudo apt-get install ccextractor` - Tested on ubuntu 20.04 LTS

```python
python3 manage.py makemigrations #Need if you use SQL DB
python3 manage.py migrate  #Need if you use SQL DB
python3 manage.py runserver #TO start the server
```

**For Nginx Reverse Proxy increase the upload file size and get rid of CORS errors, follow the below method**

1. Open `/etc/nginx/nginx.conf` and modify the below parameter within **http**
2. `client_max_body_size SIZE;` **SIZE** Refers to max body size
3. `sudo systemctl restart nginx` To restart nginx server

## Useful command snippet for Developers

```bash
source env/bin/activate #Enable python virtual environment
sudo apt install ccextractor #To install ccextractor binaries
pip install -r /path/to/requirements.txt #Install python requirements packages
pip3 freeze > requirements.txt #To install the python3 packages
ccextractor video_test.mp4 -out=ttxt #To extract subtitles from the video
sudo systemctl start redis-server.service # To start the redis service
celery -A video_sub_parser worker --loglevel=debug --concurrency=4  #To start celery instance
```

## Important Links

- How to setup the Django Project in python virtual environment https://realpython.com/django-setup/
- Install Redis Server on Ubuntu https://redis.io/docs/getting-started/installation/install-redis-on-linux/

## API Endpoints

### Request

`POST /api/v1/upload/file`

| Body     | Type          | Description                   |
| :------- | :------------ | :---------------------------- |
| `file`   | `File Object` | **Required**. File to Upload  |
| `remark` | `string`      | **Required**. Remark for File |

### Response

```JSON
{
    "message":string,
    "filename":string,
    "task_id":string
}
```

### Request

`GET /api/v1/parse?file=filename`

| Body       | Type     | Description                         |
| :--------- | :------- | :---------------------------------- |
| `filename` | `string` | **Required**. Name of Uploaded File |

### Response

```JSON
{
    "message":string
}
```

### Request

`GET /api/v1/subtitle/find?query=TO SUCCESS`

| Body    | Type     | Description                   |
| :------ | :------- | :---------------------------- |
| `query` | `string` | **Required**. Query to search |

### Response

```JSON
{
    {
    "Items": [
        {
            "subtitle_url": string,
            "media_path": string,
            "SubtitleID": string,
            "subtitle": string,
            "start_time": string,
            "end_time": string
        }
    ],
    "Count": number,
    "ScannedCount": number,
    "ResponseMetadata": {
        "RequestId": string,
        "HTTPStatusCode": number,
        "HTTPHeaders": {
            "server": string,
            "date": string,
            "content-type": string,
            "content-length": string,
            "connection": string,
            "x-amzn-requestid": string,
            "x-amz-crc32": string
        },
        "RetryAttempts": number
    }
}
}
```

### Request

`PATCH /api/v1/status/file/task_id`

| Body      | Type     | Description                                  |
| :-------- | :------- | :------------------------------------------- |
| `task_id` | `string` | **Required**. Background Task ID from Celery |

### Response

```
boolean
```

### Request

`GET /progress-track/task_id`

| Body      | Type     | Description                                  |
| :-------- | :------- | :------------------------------------------- |
| `task_id` | `string` | **Required**. Background Task ID from Celery |

### Response

```JSON
   {
    "state": string,
    "complete": boolean,
    "success": boolean,
    "progress": {
        "pending": boolean,
        "current": number,
        "total": number,
        "percent": number
    },
    "result": string | null
}
```
