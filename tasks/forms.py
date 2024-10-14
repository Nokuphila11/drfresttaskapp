from django import forms
from .models import Task
from datetime import date

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status', 'completed_at']

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date <= date.today():
            raise forms.ValidationError("The due date must be in the future.")
        return due_date

    def clean_completed_at(self):
        completed_at = self.cleaned_data.get('completed_at')
        if completed_at and completed_at < date.today():
            raise forms.ValidationError("Completion date cannot be in the past.")
        return completed_at
