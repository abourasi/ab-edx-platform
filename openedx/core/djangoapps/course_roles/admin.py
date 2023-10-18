from django.contrib import admin
from openedx.core.djangoapps.course_roles.models import CourseRolesUserRole


@admin.register(CourseRolesUserRole)
class CourseRolesUserRoleAdmin(admin.ModelAdmin):
    pass
