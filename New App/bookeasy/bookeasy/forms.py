from django import forms
from .models import Book, Movie, Authors
from .models import userProfile


class BookForm(forms.ModelForm):
    
    author_uuid = forms.ModelChoiceField(
        queryset=Authors.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Author",  
        required=False  
    )

    class Meta:
        model = Book
        fields = [
            'book_name', 
            'category', 
            'language', 
            'publish_date', 
            'publisher_name', 
            'total_pages', 
            'books_available', 
            'price', 
            'isbn', 
            'book_image', 
            'author_uuid'  
        ]
        widgets = {
            'book_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'publish_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'publisher_name': forms.TextInput(attrs={'class': 'form-control'}),
            'total_pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'books_available': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'book_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'author_uuid': forms.Select(attrs={'class': 'form-control'})
        }


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'name', 'language', 'duration', 'director', 
            'maleactor', 'femaleactor', 'music', 'category', 'movieimage'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),  
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'maleactor': forms.TextInput(attrs={'class': 'form-control'}),  
            'femaleactor': forms.TextInput(attrs={'class': 'form-control'}),  
            'music': forms.TextInput(attrs={'class': 'form-control'}), 
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'movieimage': forms.ClearableFileInput(attrs={'class': 'form-control'}),  
        }


class AuthorsForm(forms.ModelForm):
    class Meta:
        model = Authors
        fields = [
            'author_name', 'bio', 'authorimage', 'date_of_birth', 
            'nationality', 'website', 'email'
        ]
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author Name'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Short Biography'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nationality'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website URL'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

class userProfileForm(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = [
            'user_image',
            'hobbie',
            'phone_number',
            'country',
            'states',
            'city',
            'address',
            'landmark',
            'house_no',
            'pincode',
        ]
        widgets = {
            'user_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'hobbie': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your hobbies'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country'
            }),
            'states': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Your Address'
            }),
            'landmark': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Landmark'
            }),
            'house_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'House Number'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pincode'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add 'form-control' to all fields without overwriting widget-specific attributes
        for field_name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'