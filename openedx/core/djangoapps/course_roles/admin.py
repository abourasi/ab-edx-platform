""" Django admin page for course_roles djangoapp """


from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model

# from openedx.core.lib.courses import clean_course_id
from openedx.core.djangoapps.course_roles.models import CourseRolesUserRole

User = get_user_model()  # pylint:disable=invalid-name


class CourseRolesUserRoleForm(forms.ModelForm):
    """Form for assigning users new roles in the Django Admin Panel"""
    email = forms.EmailField(required=True)
    # course = forms.CharField(required=False)
    # org = forms.CharField(required=False)

    def clean_org(self):
        """If org and course-id exists then Check organization name
        against the given course.
        """
        if self.cleaned_data.get('course') and self.cleaned_data['org']:
            org = self.cleaned_data['org']
            org_name = self.cleaned_data.get('course').org
            if org.name.lower() != org_name.lower():
                raise forms.ValidationError(
                    "Org name {} is not valid. Valid name is {}.".format(
                        org, org_name
                    )
                )
        # if self.cleaned_data.get('course') and self.cleaned_data['org'] is None:
        #     raise forms.ValidationError(
        #         "Org cannot be blank if the role is being assigned for a course."
        #     )
        return self.cleaned_data['org']

    def clean_email(self):
        """
        Checking user object against given email id.
        """
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except Exception:
            raise forms.ValidationError(  # lint-amnesty, pylint: disable=raise-missing-from
                "Email does not exist. Could not find {email}. Please re-enter email address".format(
                    email=email
                )
            )

        return user

    def clean(self):
        """
        Check if the user is already assigned this role in the DB for the context.
        Context can be course, org, or instance.
        """
        cleaned_data = super().clean()
        if not self.errors:
            if CourseRolesUserRole.objects.filter(
                    user=cleaned_data.get("email"),
                    org=cleaned_data.get("org"),
                    course=cleaned_data.get("course"),
                    role=cleaned_data.get("role")
            ).exists():
                raise forms.ValidationError("Duplicate Record.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user_id:
            self.fields['email'].initial = self.instance.user.email
        self.fields["course"].widget.attrs.update(style="width: 25%")
        self.fields["org"].widget.attrs.update(style="width: 25%")
        self.fields["email"].widget.attrs.update(style="width: 25%")

@admin.register(CourseRolesUserRole)
class CourseRolesUserRoleAdmin(admin.ModelAdmin):
    """Admin panel for course_roles role assignment"""
    form = CourseRolesUserRoleForm
    raw_id_fields = ("user", "org", "course")

    fieldsets = (
        ('Assign Course Role to User', {
            'fields': ('email', 'course', 'org', 'role',),
            'description': '<br/>A role assigned to a course will only be valid for that course.<br/>'+
            'A role assigned to an org, without a course, will apply to all courses that are assigned to that org.'+
            '<br/>A role assigned to neither a course nor an org will apply to all courses for the instance.<br/><br/>'
        }),
    )

    list_display = (
        'id', 'user', 'course', 'org', 'role',
    )

    search_fields = (
        'id', 'user__username', 'user__email', 'course', 'org', 'role',
    )

    def save_model(self, request, obj, form, change):
        obj.user = form.cleaned_data['email']
        super().save_model(request, obj, form, change)
