from django.db import models
from django.contrib.auth.models import User
from .validator import *
from picklefield.fields import PickledObjectField

class Version(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="default") 
    number = models.IntegerField(default=1)
    archive = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'name']
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

class CurrentVersion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    version = models.ForeignKey(Version, on_delete=models.CASCADE, null=True, blank=True)
    state = models.CharField(max_length=50, default="/versions/")
    history = PickledObjectField(null=True, blank=True)
    gantt_buffer = PickledObjectField(null=True, blank=True)

class Category(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE, default="1")
    category_code = models.CharField(max_length=1)
    category_text = models.CharField(max_length=50)
    enabled = models.BooleanField(default=True)
    notes = models.CharField(max_length=400, null=True, blank=True)
    copied_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    selected_from = models.BooleanField(default=False, null=True, blank=True)
    selected_to = models.BooleanField(default=False, null=True, blank=True)
    
    class Meta:
        unique_together = ['category_code', 'version']
        ordering = ["category_code"]

    def __str__(self):
        return f"{self.category_code}: {self.category_text}"

class NodeStandard(models.Model):
        
    code = models.CharField(max_length=1, default="B")
    name = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.code}: {self.name}"

    class Meta:
        ordering = ["code", "name"]

class Node(models.Model):

    def get_default_node_standard():
        return NodeStandard.objects.get(name="Not defined").id

    version = models.ForeignKey(Version, on_delete=models.CASCADE, default="1")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    node_code = models.CharField(max_length=2, default="")
    node_text = models.CharField(max_length=200)
    weight = models.FloatField(blank=False, default=1, validators=[val_weight])
    duration = models.FloatField(blank=False, default=1, validators=[val_duration])
    enabled = models.BooleanField(blank=False, default=True)
    notes = models.CharField(max_length=400, null=True, blank=True)
    xpos = models.FloatField(null=True, blank=True, default=0)
    ypos = models.FloatField(null=True, blank=True, default=0)
    placed = models.BooleanField(default=False)
    selected = models.BooleanField(default=False)
    connected_to_goal = models.BooleanField(default=True)
    connected_to_goal_enabled = models.BooleanField(default=True)
    # node_standard = models.ForeignKey(NodeStandard, null=True, blank=True, default=get_default_node_standard, on_delete=models.SET_DEFAULT)
    node_standard = models.ForeignKey(NodeStandard, null=True, blank=True, on_delete=models.SET_NULL)
    copied_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ['node_code', 'category', 'version']
        ordering = ["category", "node_code"]

    def __str__(self):
        return f"{self.category.category_code}{self.node_code}: {self.node_text}"

class Link(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE, default="1")
    from_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='from_node', default=None)
    to_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='to_node', default=None)
    weight = models.FloatField(blank=False, default=1, validators=[val_weight])
    enabled = models.BooleanField(blank=False, default=True)
    notes = models.CharField(max_length=400, null=True, blank=True)
    xmid = models.FloatField(null=True, blank=True, default=None)
    ymid = models.FloatField(null=True, blank=True, default=None)
    in_loop = models.BooleanField(default=False)
    in_group = models.BooleanField(default=False)
    in_enabled_loop = models.BooleanField(default=False)
    in_enabled_group = models.BooleanField(default=False)
    copied_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def clean(self):
            if self.from_node == self.to_node:
                raise ValidationError('From and to nodes must be different.')

    class Meta:
        unique_together = ['from_node', 'to_node', 'version']
        ordering = ["from_node", "to_node"]

    def __str__(self):
        return f"{self.version}: {self.from_node.category.category_code}{self.from_node.node_code} to {self.to_node.category.category_code}{self.to_node.node_code}"

class Loop(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE, default="1")
    links = models.ManyToManyField(Link)
    enabled = models.BooleanField(default=True)
    # duration = models.FloatField(null=True, blank=True, default=1, validators=[val_duration])
    # weight = models.FloatField(null=True, blank=True, default=1, validators=[val_weight])
    notes = models.CharField(max_length=400, null=True, blank=True)
    group = models.BooleanField(default=False)
    copied_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        # return f"{self.version}: {self.id}"
        # return f"{self.version}: {self.links}"
        loop_string = ""
        loop_list = [link.from_node.category.category_code + link.from_node.node_code + ": " + link.from_node.node_text for link in self.links.all()]
        for i in loop_list:
            loop_string = loop_string + " / " + i
        loop_string = loop_string[3:]

        return loop_string

class Grouped(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE, default="1")
    loops = models.ManyToManyField(Loop)
    duration = models.FloatField(null=True, blank=True, default=1, validators=[val_duration])
    # weight = models.FloatField(null=True, blank=True, default=1, validators=[val_weight])
    copied_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.version}: {self.id}"

class Enabled_select_option(models.Model):
    option = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.option}"  

class Label_option(models.Model):
    option = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.option}"     

class Auto_layout_option(models.Model):
    option = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.option}"      

class NetworkParam(models.Model):

    MODEL_CHOICES = [
    ("EF", "Efficient"),
    ("AC", "Accurate"),
    ]
    def get_default_enabled_select():
        return Enabled_select_option.objects.get(option="All")
    
    def get_default_labels():
        return Label_option.objects.get(option="Full labels")
    
    def get_default_auto_layout():
        return Auto_layout_option.objects.get(option="Columns")   

    version = models.OneToOneField(Version, on_delete=models.CASCADE, default="1")
    Model_choice = models.CharField(max_length=50, null=False, blank=False, default="AC", choices=MODEL_CHOICES)
    Plot_width = models.IntegerField(null=True, blank=True, default=1000)
    Plot_height = models.IntegerField(null=True, blank=True, default=1000)
    Move_rate = models.FloatField(null=True, blank=True, default=0.1)
    Force_threshold = models.FloatField(null=True, blank=True, default=2)
    Target_node_distance = models.IntegerField(null=True, blank=True, default=200)
    Link_attraction = models.FloatField(null=True, blank=True, default=0.5)
    Repulsion = models.FloatField(null=True, blank=True, default=3)
    Boundry_repulsion = models.FloatField(null=True, blank=True, default=4)
    Target_boundary_distance = models.IntegerField(null=True, blank=True, default=100)
    Max_interations = models.IntegerField(null=True, blank=True, default=100)
    Link_clearance = models.IntegerField(null=True, blank=True, default=50)
    Pair_separation = models.IntegerField(null=True, blank=True, default=10)
    Legend_x_spacing = models.IntegerField(null=True, blank=True, default=140)
    Legend_y_spacing = models.IntegerField(null=True, blank=True, default=30)
    Legend_box_pad = models.IntegerField(null=True, blank=True, default=10)
    Slow_motion = models.BooleanField(default=False)
    Hide_links = models.BooleanField(default=False)
    Enabled_select = models.ForeignKey(Enabled_select_option, on_delete=models.CASCADE, default=get_default_enabled_select)
    Link_midpoints = models.BooleanField(default=True)
    Labels = models.ForeignKey(Label_option, on_delete=models.CASCADE, default=get_default_labels)
    JPG_output_resolution = models.IntegerField(null=True, blank=True, default=4)
    Show_arrows = models.BooleanField(default=True)
    Include_Goals_in_key = models.BooleanField(default=True)
    Auto_layout = models.ForeignKey(Auto_layout_option, on_delete=models.CASCADE, default=get_default_auto_layout)
    Show_unconnected = models.BooleanField(default=True)
    Enabled_loops_only = models.BooleanField(default=False)
    copied_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.version}"  

class Start_month_option(models.Model):
    option = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.option}"  

class Start_year_option(models.Model):
    option = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.option}"   

class Order_by_option(models.Model):
    option = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.option}"   

class X_axis_option(models.Model):
    option = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.option}"  

class Timing_option(models.Model):
    option = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.option}"  

class Duration_option(models.Model):
    option = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.option}"  

class GanttParam(models.Model):

    def get_default_x_axis():
        return X_axis_option.objects.get(option="Number")
    
    def get_default_start_month():
        return Start_month_option.objects.get(option="Jan")

    def get_default_start_year():
        return Start_year_option.objects.get(option="2023")

    def get_default_timing():
        return Timing_option.objects.get(option="Earliest")

    def get_default_duration():
        return Duration_option.objects.get(option="Without durations")
    
    def get_default_order_by():
        return Order_by_option.objects.get(option="Time")

    version = models.OneToOneField(Version, on_delete=models.CASCADE, default="1")
    X_axis = models.ForeignKey(X_axis_option, on_delete=models.CASCADE, default=get_default_x_axis)
    Time_unit_if_Number = models.CharField(max_length=50, null=True, blank=True, default="Year")
    Start_month_if_Month = models.ForeignKey(Start_month_option, on_delete=models.CASCADE, default=get_default_start_month)
    Start_year = models.ForeignKey(Start_year_option, on_delete=models.CASCADE, default=get_default_start_year)
    Max_X_ticks = models.IntegerField(null=True, blank=True, default=15)
    Order_by = models.ForeignKey(Order_by_option, on_delete=models.CASCADE, default=get_default_order_by)
    Plot_width = models.IntegerField(null=True, blank=True, default=1000)
    Plot_height = models.IntegerField(null=True, blank=True, default=1000)
    Plot_padding = models.IntegerField(null=True, blank=True, default=10)
    Internal_padding = models.IntegerField(null=True, blank=True, default=10)
    Legend_limit = models.IntegerField(null=True, blank=True, default=0)
    Legend_x_spacing = models.IntegerField(null=True, blank=True, default=140)
    Legend_y_spacing = models.IntegerField(null=True, blank=True, default=30)
    Legend_box_pad = models.IntegerField(null=True, blank=True, default=10)
    Top_margin = models.IntegerField(null=True, blank=True, default=50)
    Right_margin = models.IntegerField(null=True, blank=True, default=50)
    Y_axis_space = models.IntegerField(null=True, blank=True, default=250)
    X_axis_space = models.IntegerField(null=True, blank=True, default=50)
    Pixels_per_row = models.IntegerField(null=True, blank=True, default=16)
    Bar_padding = models.IntegerField(null=True, blank=True, default=3)
    Tick_length = models.IntegerField(null=True, blank=True, default=5)
    Path_optimisation_max_steps = models.IntegerField(null=True, blank=True, default=1)
    JPG_output_resolution = models.IntegerField(null=True, blank=True, default=4)
    Timing = models.ForeignKey(Timing_option, on_delete=models.CASCADE, default=get_default_timing)
    Durations = models.ForeignKey(Duration_option, on_delete=models.CASCADE, default=get_default_duration)
    Show_out_seq = models.BooleanField(default=True)
    Enabled_only = models.BooleanField(default=True)
    Apply_groups = models.BooleanField(default=True)
    copied_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.version}" 