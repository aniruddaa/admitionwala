from django.contrib import admin  # type: ignore
from .models import College, Course, Review, CounselingRequest, News, UserProfile, CertifiedCourse, JobInCareer  # type: ignore
from .models import JobApplication  # type: ignore


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
	list_display = ('name', 'location', 'featured')
	readonly_fields = ('preview_background',)
	fields = ('name', 'location', 'description', 'website', 'logo', 'background_image', 'preview_background', 'phone', 'featured')

	def preview_background(self, obj):
		if obj and obj.background_image:
			return f"<img src='{obj.background_image.url}' style='max-width:300px; height:auto;'/>"
		return '(no background)'
	preview_background.allow_tags = True
	preview_background.short_description = 'Background Preview'


admin.site.register(Course)
admin.site.register(Review)
admin.site.register(CounselingRequest)
admin.site.register(News)
admin.site.register(UserProfile)
admin.site.register(CertifiedCourse)
admin.site.register(JobInCareer)
from .models import Job  # type: ignore
admin.site.register(Job)
admin.site.register(JobApplication)
from .models import Bookmark  # type: ignore
admin.site.register(Bookmark)
from .models import AboutPage, Director, StaffMember


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
	list_display = ('title', 'updated_at')


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
	list_display = ('name', 'title')
	readonly_fields = ('preview_photo',)
	def preview_photo(self, obj):
		if obj and obj.photo:
			return f"<img src='{obj.photo.url}' style='max-width:200px; height:auto;'/>"
		return '(no photo)'
	preview_photo.allow_tags = True


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
	list_display = ('name', 'role')
	readonly_fields = ('preview_photo',)
	def preview_photo(self, obj):
		if obj and obj.photo:
			return f"<img src='{obj.photo.url}' style='max-width:200px; height:auto;'/>"
		return '(no photo)'
	preview_photo.allow_tags = True
