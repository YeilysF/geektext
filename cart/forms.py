from django import forms

class CouponApplyForm(forms.Form):
    code = forms.CharField(max_length=10, label='Coupon')