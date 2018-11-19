from django.db import models


ROBOT_TYPE_LIST = (
    ROBOT_TYPE_INGOING,
    ROBOT_TYPE_OUTGOING,
) = (
    1000,
    2000,
)


# Create your models here.
class RobotPi(models.Model):
    uuid = models.CharField(max_length=256)
    type_id = models.IntegerField()
    user_id = models.IntegerField()
    app_id = models.IntegerField()
