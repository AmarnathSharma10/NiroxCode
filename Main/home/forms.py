from django import forms
from home.models import CodeRunner
LANG_CHOICES={
    ("py","Python"),
    ("java","Java"),
    ("cpp","C++"),
    ("c","C")
}
class  CodeRunnerForm(forms.ModelForm):
    # lang=forms.ChoiceField(choices=LANG_CHOICES)
    class Meta:
        model=CodeRunner
        fields=["language","input_data","code","output_data","verdict"]
        widgets = {
            'language': forms.Select(attrs={'class': 'border py-2 px-3 text-grey-darkest'}),
            'input_data': forms.Textarea(attrs={'class': 'border py-2 px-3 text-grey-darkest small-input',
                                                 'style': 'width: 400px; height:80px;  background-color: black; color: white;'}),
            'code': forms.Textarea(attrs={'class': 'border py-2 px-3 text-grey-darkest w-full h-40',
                                          'style':'width: 800px; height:200px;background-color: #add8e6;color:black;font-family: Consolas, "Courier New", monospace;'}),
            'output_data': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'border py-2 px-3 text-grey-darkest w-full h-40',
                                                 'style': 'width: 500px; height:80px;  background-color: black; color: white;',
                                                     'id' : 'code-textarea;'
                                                 }),
            'verdict': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'border py-2 px-3 text-grey-darkest w-full h-40',
                                                 'style': 'width: 400px; height:80px;  background-color: grey; color: white;'
                                                 }),
        }


