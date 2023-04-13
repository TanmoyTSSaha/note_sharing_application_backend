from django.contrib import admin
from .models import QnaModel, QnaCommentModel

# Register your models here.
admin.site.register(QnaModel)
admin.site.register(QnaCommentModel)