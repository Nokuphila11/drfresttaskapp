from django import forms
from .models import Task
from datetime import date

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status', 'completed_at']

    # Ensure the due date is in the future
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date <= date.today():
            raise forms.ValidationError("The due date must be in the future.")
        return due_date

    # Ensure completion date is valid
    def clean_completed_at(self):
        completed_at = self.cleaned_data.get('completed_at')
        status = self.cleaned_data.get('status')
        
        if completed_at and completed_at < date.today():
            raise forms.ValidationError("Completion date cannot be in the past.")
        
        # If task is not completed, completion date should not be set
        if status != Task.STATUS_COMPLETED and completed_at:
            raise forms.ValidationError("Completion date can only be set if the task is marked as completed.")
        
        return completed_at

    # Ensure that completed_at is set only when the task is marked as Completed
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        completed_at = cleaned_data.get('completed_at')

        if status == Task.STATUS_COMPLETED and not completed_at:
            self.add_error('completed_at', "Please provide a completion date when marking the task as completed.")

        return cleaned_data
