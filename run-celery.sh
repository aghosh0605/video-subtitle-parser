#!/bin/bash
source env/bin/activate && cd video_sub_parser && celery -A video_sub_parser worker --loglevel=debug --concurrency=4
