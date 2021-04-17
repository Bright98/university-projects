from django.db import models


class Stop(models.Model):
    STATUS_CHOISE = [("wait", "wait"), ("done", "done")]
    status = models.CharField(max_length=9, choices=STATUS_CHOISE, default="wait")

    def __str__(self):
        return "status: {}".format(self.status)


class TrafficLight(models.Model):
    COMMAND_CHOISE = [("go", "go"), ("stop", "stop")]
    command = models.CharField(max_length=9, choices=COMMAND_CHOISE, default="go")
    STATUS_CHOISE = [("wait", "wait"), ("done", "done")]
    status = models.CharField(max_length=9, choices=STATUS_CHOISE, default="wait")

    def __str__(self):
        return "command: {} - status: {}".format(self.command, self.status)

