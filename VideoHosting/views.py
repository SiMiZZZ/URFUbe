from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import boto3
import botocore
from .models import *
import hashlib
import os
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib import messages

session = boto3.session.Session()
s3_client = session.client(
        service_name='s3',
        endpoint_url='https://hb.bizmrg.com',
        aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY")
    )

bucket_name = os.getenv("BUCKET_NAME")


class IndexAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        print(request.user.is_authenticated)
        videos = Video.objects.all()
        context = {
            "videos": videos,
            "user": request.user
        }
        return render(request, "index.html", context=context)


class UploadAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return render(request, "upload.html")

    @csrf_exempt
    def post(self, request):
        video_name = request.POST["video_name"]
        video_file = request.FILES["video_file"]
        preview_url = None
        try:
            last_index = Video.objects.first().id + 1
        except:
            last_index = 1

        try:
            cloud_video_name = hashlib.md5(f"{last_index}_{video_name}".encode()).hexdigest()
            url = f"https://{bucket_name}.hb.bizmrg.com/{cloud_video_name}"

            if "preview" in request.FILES:
                preview = request.FILES["preview"]
                cloud_preview_name = hashlib.md5(f"{last_index}_{preview.name}".encode()).hexdigest()
                preview_url = f"https://{bucket_name}.hb.bizmrg.com/{cloud_preview_name}"
                s3_client.put_object(Bucket=bucket_name, Key=cloud_preview_name, Body=preview.read())

            s3_client.put_object(Bucket=bucket_name, Key=cloud_video_name, Body=video_file.read())

        except botocore.exceptions.ConnectionClosedError:
            print("Ошибка сети. Проверьте соединение")
            return render(request, "upload.html")
        except:
            messages.success(request, ("Что-то пошло не так. Попробуйте ввести данные заново",))
            return render(request, "upload.html")

        if preview_url:
            Video.objects.create(name=video_name, url=url, cloud_name=cloud_video_name,
                                 author=request.user, preview_url=preview_url)
        else:
            Video.objects.create(name=video_name, url=url, cloud_name=cloud_video_name, author=request.user)
        return render(request, "upload.html")


class VideoAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            video = Video.objects.get(id=pk)
        except:
            messages.success(request, ("Некоректная ссылка",))
            return redirect("/")
        video.views_count += 1
        video.save()
        like_count = Reaction.objects.filter(video_id=video.id, like=True).count()
        dislike_count = Reaction.objects.filter(video_id=video.id, dislike=True).count()
        context = {"video": video, "like_count": like_count,
                   "dislike_count": dislike_count}
        if request.user.is_authenticated:
            is_liked = Reaction.objects.filter(video_id=video.id, user=request.user, like=True).exists()
            is_disliked = Reaction.objects.filter(video_id=video.id, user=request.user, dislike=True).exists()
            context["is_liked"] = is_liked
            context["is_disliked"] = is_disliked



        if request.user.is_authenticated:
            query = History.objects.filter(video=video, user=request.user)
            if query.exists():
                query.first().delete()
            History.objects.create(video=video, user=request.user)

        videos = Video.objects.all().exclude(id=video.id)
        context["videos"] = videos
        comments = Comment.objects.filter(video=video)
        context["comments"] = comments


        url = s3_client.generate_presigned_url(ClientMethod='get_object',
                                               Params={
                                                   'Bucket': bucket_name,
                                                   'Key': video.cloud_name,
                                               })
        video.url = url

        return render(request, "video.html", context=context)


class HistoryAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        videos_dct = History.objects.filter(user=user).values("video")
        videos = list(map(lambda x: Video.objects.get(id=x["video"]), videos_dct))
        context = {"videos": videos}
        return render(request, "history.html", context=context)


class CommentAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        request_referer = request.META["HTTP_REFERER"]
        text = request.POST["label"]
        video_id = int(request_referer.split("/")[-1])
        Comment.objects.create(video_id=video_id, user=request.user, text=text)

        return redirect(request.META['HTTP_REFERER'])


class LikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        request_referer = request.META["HTTP_REFERER"]
        video_id = int(request_referer.split("/")[-1])
        reaction = Reaction.objects.filter(video_id=video_id, user=request.user)
        if reaction.exists():
            reaction = reaction.first()
            if reaction.like:
                reaction.like = False
            elif reaction.dislike:
                reaction.dislike = False
                reaction.like = True
            else:
                reaction.like = True
            reaction.save()
        else:
            Reaction.objects.create(video_id=video_id, user=request.user, like=True)
        return redirect(request.META["HTTP_REFERER"])


class DislikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        request_referer = request.META["HTTP_REFERER"]
        video_id = int(request_referer.split("/")[-1])
        reaction = Reaction.objects.filter(video_id=video_id, user=request.user)
        if reaction.exists():
            reaction = reaction.first()
            if reaction.dislike:
                reaction.dislike = False
            elif reaction.like:
                reaction.dislike = True
                reaction.like = False
            else:
                reaction.dislike = False
            reaction.save()
        else:
            Reaction.objects.create(video_id=video_id, user=request.user, dislike=True)
        return redirect(request.META["HTTP_REFERER"])
