"""
Permissions for the instructor dashboard and associated actions
"""

from bridgekeeper import perms
from bridgekeeper.rules import is_staff

from openedx.core.djangoapps.course_roles.permissions import CourseRolesPermission
from lms.djangoapps.courseware.rules import HasAccessRule, HasRolesRule, HasPermissionRule

ALLOW_STUDENT_TO_BYPASS_ENTRANCE_EXAM = 'instructor.allow_student_to_bypass_entrance_exam'
ASSIGN_TO_COHORTS = 'instructor.assign_to_cohorts'
EDIT_COURSE_ACCESS = 'instructor.edit_course_access'
EDIT_FORUM_ROLES = 'instructor.edit_forum_roles'
EDIT_INVOICE_VALIDATION = 'instructor.edit_invoice_validation'
ENABLE_CERTIFICATE_GENERATION = 'instructor.enable_certificate_generation'
GENERATE_CERTIFICATE_EXCEPTIONS = 'instructor.generate_certificate_exceptions'
GENERATE_BULK_CERTIFICATE_EXCEPTIONS = 'instructor.generate_bulk_certificate_exceptions'
GIVE_STUDENT_EXTENSION = 'instructor.give_student_extension'
VIEW_ISSUED_CERTIFICATES = 'instructor.view_issued_certificates'
CAN_RESEARCH = 'instructor.research'
CAN_ENROLL = 'instructor.enroll'
CAN_BETATEST = 'instructor.enroll_beta'
ENROLLMENT_REPORT = 'instructor.enrollment_report'
EXAM_RESULTS = 'instructor.view_exam_results'
OVERRIDE_GRADES = 'instructor.override_grades'
SHOW_TASKS = 'instructor.show_tasks'
VIEW_COUPONS = 'instructor.view_coupons'
EMAIL = 'instructor.email'
RESCORE_EXAMS = 'instructor.rescore_exams'
VIEW_REGISTRATION = 'instructor.view_registration'
VIEW_DASHBOARD = 'instructor.dashboard'


perms[ALLOW_STUDENT_TO_BYPASS_ENTRANCE_EXAM] = HasAccessRule('staff')
perms[ASSIGN_TO_COHORTS] = HasAccessRule('staff')
perms[EDIT_COURSE_ACCESS] = HasAccessRule('instructor')
perms[EDIT_FORUM_ROLES] = HasAccessRule('staff')
perms[EDIT_INVOICE_VALIDATION] = HasAccessRule('staff')
perms[ENABLE_CERTIFICATE_GENERATION] = is_staff
perms[GENERATE_CERTIFICATE_EXCEPTIONS] = is_staff
perms[GENERATE_BULK_CERTIFICATE_EXCEPTIONS] = is_staff
perms[GIVE_STUDENT_EXTENSION] = HasAccessRule('staff')
# TODO: course roles: If the course roles feature flag is disabled the HasPermissionRule
#       below will never return true.
#       Remove the HasRolesRule('data_researcher') call when course_roles Django app are implemented.
perms[VIEW_ISSUED_CERTIFICATES] = (
    HasAccessRule('staff')
    | HasRolesRule('data_researcher')
    | HasPermissionRule(CourseRolesPermission.ACCESS_DATA_DOWNLOADS.value)
)
# only global staff or those with the data_researcher role can access the data download tab
# HasAccessRule('staff') also includes course staff
# TODO: course roles: If the course roles feature flag is disabled the HasPermissionRule
#       below will never return true.
#       Remove the HasRolesRule('data_researcher') call when course_roles Django app are implemented.
perms[CAN_RESEARCH] = (
    is_staff | HasRolesRule('data_researcher') | HasPermissionRule(CourseRolesPermission.ACCESS_DATA_DOWNLOADS.value)
)
perms[CAN_ENROLL] = HasAccessRule('staff')
perms[CAN_BETATEST] = HasAccessRule('instructor')
# TODO: course roles: If the course roles feature flag is disabled the HasPermissionRule
#       below will never return true.
#       Remove the HasRolesRule('data_researcher') call when course_roles Django app are implemented.
perms[ENROLLMENT_REPORT] = (
    HasAccessRule('staff')
    | HasRolesRule('data_researcher')
    | HasPermissionRule(CourseRolesPermission.ACCESS_DATA_DOWNLOADS.value)
)
# TODO: course roles: If the course roles feature flag is disabled the HasPermissionRule
#       below will never return true.
#       Remove the HasRolesRule('data_researcher') call when course_roles Django app are implemented.
perms[VIEW_COUPONS] = (
    HasAccessRule('staff')
    | HasRolesRule('data_researcher')
    | HasPermissionRule(CourseRolesPermission.ACCESS_DATA_DOWNLOADS.value)
)
perms[EXAM_RESULTS] = HasAccessRule('staff')
perms[OVERRIDE_GRADES] = HasAccessRule('staff')
# TODO: course roles: If the course roles feature flag is disabled the HasPermissionRule
#       below will never return true.
#       Remove the HasRolesRule('data_researcher') call when course_roles Django app are implemented.
perms[SHOW_TASKS] = (
    HasAccessRule('staff')
    | HasRolesRule('data_researcher')
    | (
        HasPermissionRule(CourseRolesPermission.MANAGE_STUDENTS.value)
        | HasPermissionRule(CourseRolesPermission.ACCESS_DATA_DOWNLOADS.value)
        | HasPermissionRule(CourseRolesPermission.ACCESS_INSTRUCTOR_DASHBOARD.value)
    )
)
perms[EMAIL] = HasAccessRule('staff')
perms[RESCORE_EXAMS] = HasAccessRule('instructor')
perms[VIEW_REGISTRATION] = HasAccessRule('staff')
# TODO: course roles: If the course roles feature flag is disabled the HasPermissionRule
#       below will never return true.
#       Remove the HasRolesRule('staff', 'instructor', 'data_researcher')
#       call when course_roles Django app are implemented.
perms[VIEW_DASHBOARD] = (
    HasRolesRule('staff', 'instructor', 'data_researcher')
    | HasAccessRule('staff')
    | HasAccessRule('instructor')
    | HasPermissionRule(CourseRolesPermission.ACCESS_DATA_DOWNLOADS.value)
)
