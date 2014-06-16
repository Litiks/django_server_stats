from django import forms
from server_stats.models import BenchmarkMilestone

class BenchmarkMilestoneForm(forms.ModelForm):
    class Meta:
        model=BenchmarkMilestone
        
#eof
