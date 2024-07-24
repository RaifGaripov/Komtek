from django.db import models


class RefBook(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name="Код")
    name = models.CharField(max_length=300, verbose_name="Наименование")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def get_current_version(self):
        current_version = RefBookVersion.objects.filter(refbook=self).order_by('-start_date').first()
        return current_version.version if current_version else None

    def get_current_version_start_date(self):
        current_version = RefBookVersion.objects.filter(refbook=self).order_by('-start_date').first()
        return current_version.start_date if current_version else None

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"


class RefBookVersion(models.Model):
    refbook = models.ForeignKey(RefBook, on_delete=models.CASCADE, verbose_name="Наименование справочника")
    version = models.CharField(max_length=50, verbose_name="Версия")
    start_date = models.DateField(verbose_name="Дата начала версии")

    class Meta:
        unique_together = [('refbook', 'version'),
                           ('refbook', 'start_date')]
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочника'

    def __str__(self):
        return f"{self.refbook.name} - {self.version}"


class RefBookElement(models.Model):
    refbook_version = models.ForeignKey(RefBookVersion, on_delete=models.CASCADE, verbose_name="Версия")
    code = models.CharField(max_length=100, verbose_name="Код элемента")
    value = models.CharField(max_length=300, verbose_name="Значение элемента")

    class Meta:
        unique_together = ('refbook_version', 'code')
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочника'

    def __str__(self):
        return f"{self.code} - {self.value}"
