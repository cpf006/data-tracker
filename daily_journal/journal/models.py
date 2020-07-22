from django.db import models


class DataTracker(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class DataOption(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=30)
    data_tracker = models.ForeignKey(DataTracker, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'data_tracker')

    def __str__(self):
        return self.data_tracker.name + ": " + self.name


class Entry(models.Model):
    pub_date = models.DateField(unique="True")
    content = models.TextField()

    def __str__(self):
        return str(self.pub_date)


class DataResponse(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    data_tracker = models.ForeignKey(DataTracker, on_delete=models.CASCADE)
    data_option = models.ForeignKey(
        DataOption,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('entry', 'data_tracker')

    def __str__(self):
        return str(self.entry) + " - " + str(self.data_option)
