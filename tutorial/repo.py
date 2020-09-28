from .models import Lesson

class LessonRepo:
    def __init__(self,user):
        self.objects=Lesson.objects

    def lesson(self,lesson_id):
        try:
            return self.objects.get(pk=lesson_id)
        except expression as identifier:
            return None
    
    def list(self):
        return self.objects.all()
        