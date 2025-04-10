# Generated manually

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template',
            name='css_file',
        ),
        migrations.RemoveField(
            model_name='template',
            name='html_template',
        ),
        migrations.AddField(
            model_name='template',
            name='preview_url',
            field=models.URLField(blank=True),
        ),
        migrations.RenameField(
            model_name='portfolio',
            old_name='bio',
            new_name='about_me',
        ),
        migrations.RenameField(
            model_name='portfolio',
            old_name='email',
            new_name='contact_email',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='technologies_used',
            new_name='technologies',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='location',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='website_url',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='skills',
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolios', to='auth.user'),
        ),
        migrations.AlterField(
            model_name='project',
            name='completion_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='portfolios/project_images/'),
        ),
        migrations.AlterField(
            model_name='project',
            name='order',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='portfolios/resumes/'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ] 