import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='description',
            new_name='memo',
        ),
        migrations.RenameField(
            model_name='todo',
            old_name='created',
            new_name='created_at',
        ),
        migrations.AlterField(
            model_name='todo',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='todo',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
