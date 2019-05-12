from django.db import models
import json


class Works(models.Model):
    works = models.CharField(max_length=10000, default=json.dumps({}))
    max_votes = models.IntegerField(default=1)


class UserVoteLog(models.Model):
    wechat_openid = models.CharField(max_length=64)
    work_tag = models.CharField(max_length=64)


class UploadStatus(models.Model):
    # free/loading
    status = models.CharField(max_length=64, default='free')
