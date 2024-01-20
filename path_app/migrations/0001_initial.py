# Generated by Django 4.2.7 on 2024-01-08 19:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import path_app.models
import path_app.validator
import picklefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Auto_layout_option",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("option", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category_code", models.CharField(max_length=1)),
                ("category_text", models.CharField(max_length=50)),
                ("enabled", models.BooleanField(default=True)),
                ("notes", models.CharField(blank=True, max_length=400, null=True)),
                (
                    "selected_from",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                (
                    "selected_to",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                (
                    "copied_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="path_app.category",
                    ),
                ),
            ],
            options={
                "ordering": ["category_code"],
            },
        ),
        migrations.CreateModel(
            name="Duration_option",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("option", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Enabled_select_option",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("option", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Label_option",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("option", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Link",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "weight",
                    models.FloatField(
                        default=1, validators=[path_app.validator.val_weight]
                    ),
                ),
                ("enabled", models.BooleanField(default=True)),
                ("notes", models.CharField(blank=True, max_length=400, null=True)),
                ("xmid", models.FloatField(blank=True, default=None, null=True)),
                ("ymid", models.FloatField(blank=True, default=None, null=True)),
                ("in_loop", models.BooleanField(default=False)),
                ("in_group", models.BooleanField(default=False)),
                ("in_enabled_loop", models.BooleanField(default=False)),
                ("in_enabled_group", models.BooleanField(default=False)),
                (
                    "copied_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="path_app.link",
                    ),
                ),
            ],
            options={
                "ordering": ["from_node", "to_node"],
            },
        ),
        migrations.CreateModel(
            name="Order_by_option",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("option", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Start_month_option",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("option", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Start_year_option",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("option", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Timing_option",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("option", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="X_axis_option",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("option", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Version",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="default", max_length=50)),
                ("number", models.IntegerField(default=1)),
                ("archive", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "unique_together": {("user", "name")},
            },
        ),
        migrations.CreateModel(
            name="Node",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("node_code", models.CharField(default="", max_length=2)),
                ("node_text", models.CharField(max_length=200)),
                (
                    "weight",
                    models.FloatField(
                        default=1, validators=[path_app.validator.val_weight]
                    ),
                ),
                (
                    "duration",
                    models.FloatField(
                        default=1, validators=[path_app.validator.val_duration]
                    ),
                ),
                ("enabled", models.BooleanField(default=True)),
                ("notes", models.CharField(blank=True, max_length=400, null=True)),
                ("xpos", models.FloatField(blank=True, default=0, null=True)),
                ("ypos", models.FloatField(blank=True, default=0, null=True)),
                ("placed", models.BooleanField(default=False)),
                ("selected", models.BooleanField(default=False)),
                ("connected_to_goal", models.BooleanField(default=True)),
                ("connected_to_goal_enabled", models.BooleanField(default=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="path_app.category",
                    ),
                ),
                (
                    "copied_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="path_app.node",
                    ),
                ),
                (
                    "version",
                    models.ForeignKey(
                        default="1",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="path_app.version",
                    ),
                ),
            ],
            options={
                "ordering": ["category", "node_code"],
                "unique_together": {("node_code", "category", "version")},
            },
        ),
        migrations.CreateModel(
            name="NetworkParam",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "Model_choice",
                    models.CharField(
                        choices=[("EF", "Efficient"), ("AC", "Accurate")],
                        default="AC",
                        max_length=50,
                    ),
                ),
                (
                    "Plot_width",
                    models.IntegerField(blank=True, default=1000, null=True),
                ),
                (
                    "Plot_height",
                    models.IntegerField(blank=True, default=1000, null=True),
                ),
                ("Move_rate", models.FloatField(blank=True, default=0.1, null=True)),
                (
                    "Force_threshold",
                    models.FloatField(blank=True, default=2, null=True),
                ),
                (
                    "Target_node_distance",
                    models.IntegerField(blank=True, default=200, null=True),
                ),
                (
                    "Link_attraction",
                    models.FloatField(blank=True, default=0.5, null=True),
                ),
                ("Repulsion", models.FloatField(blank=True, default=3, null=True)),
                (
                    "Boundry_repulsion",
                    models.FloatField(blank=True, default=4, null=True),
                ),
                (
                    "Target_boundary_distance",
                    models.IntegerField(blank=True, default=100, null=True),
                ),
                (
                    "Max_interations",
                    models.IntegerField(blank=True, default=100, null=True),
                ),
                (
                    "Link_clearance",
                    models.IntegerField(blank=True, default=50, null=True),
                ),
                (
                    "Pair_separation",
                    models.IntegerField(blank=True, default=10, null=True),
                ),
                (
                    "Legend_x_spacing",
                    models.IntegerField(blank=True, default=140, null=True),
                ),
                (
                    "Legend_y_spacing",
                    models.IntegerField(blank=True, default=30, null=True),
                ),
                (
                    "Legend_box_pad",
                    models.IntegerField(blank=True, default=10, null=True),
                ),
                ("Slow_motion", models.BooleanField(default=False)),
                ("Hide_links", models.BooleanField(default=False)),
                ("Link_midpoints", models.BooleanField(default=True)),
                (
                    "JPG_output_resolution",
                    models.IntegerField(blank=True, default=4, null=True),
                ),
                ("Show_arrows", models.BooleanField(default=True)),
                ("Include_Goals_in_key", models.BooleanField(default=True)),
                ("Show_unconnected", models.BooleanField(default=True)),
                ("Enabled_loops_only", models.BooleanField(default=False)),
                (
                    "Auto_layout",
                    models.ForeignKey(
                        default=path_app.models.NetworkParam.get_default_auto_layout,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="path_app.auto_layout_option",
                    ),
                ),
                (
                    "Enabled_select",
                    models.ForeignKey(
                        default=path_app.models.NetworkParam.get_default_enabled_select,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="path_app.enabled_select_option",
                    ),
                ),
                (
                    "Labels",
                    models.ForeignKey(
                        default=path_app.models.NetworkParam.get_default_labels,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="path_app.label_option",
                    ),
                ),
                (
                    "copied_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="path_app.networkparam",
                    ),
                ),
                (
                    "version",
                    models.OneToOneField(
                        default="1",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="path_app.version",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Loop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("enabled", models.BooleanField(default=True)),
                ("notes", models.CharField(blank=True, max_length=400, null=True)),
                ("group", models.BooleanField(default=False)),
                (
                    "copied_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="path_app.loop",
                    ),
                ),
                ("links", models.ManyToManyField(to="path_app.link")),
                (
                    "version",
                    models.ForeignKey(
                        default="1",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="path_app.version",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="link",
            name="from_node",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="from_node",
                to="path_app.node",
            ),
        ),
        migrations.AddField(
            model_name="link",
            name="to_node",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="to_node",
                to="path_app.node",
            ),
        ),
        migrations.AddField(
            model_name="link",
            name="version",
            field=models.ForeignKey(
                default="1",
                on_delete=django.db.models.deletion.CASCADE,
                to="path_app.version",
            ),
        ),
        migrations.CreateModel(
            name="Grouped",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "duration",
                    models.FloatField(
                        blank=True,
                        default=1,
                        null=True,
                        validators=[path_app.validator.val_duration],
                    ),
                ),
                (
                    "copied_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="path_app.grouped",
                    ),
                ),
                ("loops", models.ManyToManyField(to="path_app.loop")),
                (
                    "version",
                    models.ForeignKey(
                        default="1",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="path_app.version",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GanttParam",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "Time_unit_if_Number",
                    models.CharField(
                        blank=True, default="Year", max_length=50, null=True
                    ),
                ),
                ("Max_X_ticks", models.IntegerField(blank=True, default=15, null=True)),
                (
                    "Plot_width",
                    models.IntegerField(blank=True, default=1000, null=True),
                ),
                (
                    "Plot_height",
                    models.IntegerField(blank=True, default=1000, null=True),
                ),
                (
                    "Plot_padding",
                    models.IntegerField(blank=True, default=10, null=True),
                ),
                (
                    "Internal_padding",
                    models.IntegerField(blank=True, default=10, null=True),
                ),
                ("Legend_limit", models.IntegerField(blank=True, default=0, null=True)),
                (
                    "Legend_x_spacing",
                    models.IntegerField(blank=True, default=140, null=True),
                ),
                (
                    "Legend_y_spacing",
                    models.IntegerField(blank=True, default=30, null=True),
                ),
                (
                    "Legend_box_pad",
                    models.IntegerField(blank=True, default=10, null=True),
                ),
                ("Top_margin", models.IntegerField(blank=True, default=50, null=True)),
                (
                    "Right_margin",
                    models.IntegerField(blank=True, default=50, null=True),
                ),
                (
                    "Y_axis_space",
                    models.IntegerField(blank=True, default=250, null=True),
                ),
                (
                    "X_axis_space",
                    models.IntegerField(blank=True, default=50, null=True),
                ),
                (
                    "Pixels_per_row",
                    models.IntegerField(blank=True, default=16, null=True),
                ),
                ("Bar_padding", models.IntegerField(blank=True, default=3, null=True)),
                ("Tick_length", models.IntegerField(blank=True, default=5, null=True)),
                (
                    "Path_optimisation_max_steps",
                    models.IntegerField(blank=True, default=1, null=True),
                ),
                (
                    "JPG_output_resolution",
                    models.IntegerField(blank=True, default=4, null=True),
                ),
                ("Show_out_seq", models.BooleanField(default=True)),
                ("Enabled_only", models.BooleanField(default=True)),
                ("Apply_groups", models.BooleanField(default=True)),
                (
                    "Durations",
                    models.ForeignKey(
                        default=path_app.models.GanttParam.get_default_duration,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="path_app.duration_option",
                    ),
                ),
                (
                    "Order_by",
                    models.ForeignKey(
                        default=path_app.models.GanttParam.get_default_order_by,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="path_app.order_by_option",
                    ),
                ),
                (
                    "Start_month_if_Month",
                    models.ForeignKey(
                        default=path_app.models.GanttParam.get_default_start_month,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="path_app.start_month_option",
                    ),
                ),
                (
                    "Start_year",
                    models.ForeignKey(
                        default=path_app.models.GanttParam.get_default_start_year,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="path_app.start_year_option",
                    ),
                ),
                (
                    "Timing",
                    models.ForeignKey(
                        default=path_app.models.GanttParam.get_default_timing,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="path_app.timing_option",
                    ),
                ),
                (
                    "X_axis",
                    models.ForeignKey(
                        default=path_app.models.GanttParam.get_default_x_axis,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="path_app.x_axis_option",
                    ),
                ),
                (
                    "copied_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="path_app.ganttparam",
                    ),
                ),
                (
                    "version",
                    models.OneToOneField(
                        default="1",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="path_app.version",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CurrentVersion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state", models.CharField(default="/versions/", max_length=50)),
                (
                    "history",
                    picklefield.fields.PickledObjectField(
                        blank=True, editable=False, null=True
                    ),
                ),
                (
                    "gantt_buffer",
                    picklefield.fields.PickledObjectField(
                        blank=True, editable=False, null=True
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        unique=True,
                    ),
                ),
                (
                    "version",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="path_app.version",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="category",
            name="version",
            field=models.ForeignKey(
                default="1",
                on_delete=django.db.models.deletion.CASCADE,
                to="path_app.version",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="link",
            unique_together={("from_node", "to_node", "version")},
        ),
        migrations.AlterUniqueTogether(
            name="category",
            unique_together={("category_code", "version")},
        ),
    ]