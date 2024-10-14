from django import forms
from .models import Auction, Bid, WatchList, Comment

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['name', 'category', 'description', 'url_image', 'min_price']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',        # Add Bootstrap class
                'placeholder': 'Auction Name',  # Add placeholder
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',  # Bootstrap class for dropdown
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Auction Description',
                'rows': 5,                      # Set number of rows for textarea
            }),
            'min_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minimum Price'
            }),
            'creator': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Creator Name'
            }),
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price', 'auction']
        widgets = {
            'auction': forms.HiddenInput(),  # Render auction as a hidden input
        }

    def __init__(self, *args, **kwargs):
        auction = kwargs.pop('auction', None)  # Extract auction from kwargs
        super().__init__(*args, **kwargs)  # Call the parent constructor
        if auction is not None:
            self.fields['auction'].initial = auction  # Set the initial value

    def clean_price(self):
        price = self.cleaned_data.get('price')
        auction = self.fields['auction'].initial
        current_price = auction.current_price()

        if current_price != None and price <= current_price:
            raise forms.ValidationError(f"The bid must be greater than the actual price of ${current_price}.")
        if price < auction.min_price:
            raise forms.ValidationError(f"The minimum allowed bid is ${auction.min_price}.")

        return price

    def clean_auction(self):
        auction = self.fields['auction'].initial

        if not auction.is_active:
            raise forms.ValidationError(f"The auction is closed")
        return auction

class WatchListForm(forms.ModelForm):
    class Meta:
        model = WatchList
        fields = ['auction', 'user']
        widgets = {
            'auction': forms.HiddenInput(),
            'user': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        auction = kwargs.pop('auction', None)  # Extract auction from kwargs
        user = kwargs.pop('user', None)        # Extract user from kwargs
        super().__init__(*args, **kwargs)  # Call the parent constructor
        if auction is not None:
            self.fields['auction'].initial = auction  # Set the initial value
        if user is not None:
            self.fields['user'].initial = user  # Set the initial value

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'user', 'auction']
        widgets = {
            'auction': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',  # Add Bootstrap form-control class
                'rows': 3,               # Set a default number of rows
                'placeholder': 'Add your comment here...',  # Placeholder text
                'required': 'required',   # Make this field required
            }),
        }

    def __init__(self, *args, **kwargs):
        auction = kwargs.pop('auction', None)  # Extract auction from kwargs
        user = kwargs.pop('user', None)        # Extract user from kwargs
        super().__init__(*args, **kwargs)  # Call the parent constructor
        if auction is not None:
            self.fields['auction'].initial = auction  # Set the initial value
        if user is not None:
            self.fields['user'].initial = user  # Set the initial value




