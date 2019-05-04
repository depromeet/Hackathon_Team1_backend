from django.db import models


class Family(models.Model):
    family_name= models.CharField(max_length=45,default="family")
    created_time = models.DateTimeField(auto_now_add=True) # 생성 시각

    class Meta:
        ordering=['created_time']

class User(models.Model):
    user_unique_id = models.IntegerField(unique=True) # 카카오톡 고유 id
    user_name  = models.CharField(max_length=45, null=False) # 카카오톡 프로필 이름
    user_profile_image = models.TextField(null=True) # 카카오톡 프로필 사진
    family_id = models.ForeignKey(
        Family,
        related_name='FamilyMember',
        on_delete=models.CASCADE,
        null=True
    ) # 가족 id


class Housework(models.Model):
    housework_name = models.CharField(max_length=100, null=False) # 할 일 이름
    assignee_id = models.ForeignKey(
        User,
        related_name='Assignee',
        on_delete=models.CASCADE,
        null=False
    ) # 할 일 담당자 id
    created_time = models.DateTimeField(auto_now_add=True) # 할 일 등록순

    ordering = ['created_time']

class HouseworkCheck(models.Model):
    housework_id = models.ForeignKey(
        Housework,
        related_name='Housework',
        on_delete=models.CASCADE
    ) # 할 일 id
    assignee_id = models.ForeignKey(
        User,
        related_name='CurrentAssignee',
        on_delete=models.CASCADE
    ) # 현재 담당자 id (완료 시)
    duedate = models.DateTimeField(auto_now_add=True) # 할 일 완료 날짜

    class Meta:
        ordering=['duedate']

