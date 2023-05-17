# video-subtitle-process

A website on which video(s) can be uploaded, processed in some manner (in the background) and then searched using the subtitles in that video as keywords.

For instance, if a 2 minute clip of a music video was uploaded, the application will parse it, apply subtitles to it and ensure that searching for a particular word or phrase returns the time segment within which the video has those phrases being mentioned.

1)Used the ccextractor binary for extracting subtitles from video. Note that using any API, etc for subtitle extraction is not allowed.

2. Further, after processing, the videos will be stored in S3 and the search keywords (subtitles) in DynamoDB.

3. HTTP requests should has a maximum latency of approx 1 second.

4. The backend is written in **Django**. **Celery** for background tasks.

"Use this sample video file for running ccextractor”: https://drive.google.com/file/d/1gLi5ho33TIRNVZkSE-gD4S24zs6Xy1ci/view?usp=sharing
