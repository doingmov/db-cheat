from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation

def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for mark in bad_marks:
        mark.points = 5
        mark.save()

def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()

def create_commendation(schoolkid_name, subject_title):
    try:
        child = Schoolkid.objects.get(full_name__icontains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        print(f"Ученика с именем {schoolkid_name} не найдено")
        return
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников с именем {schoolkid_name}")
        return

    lesson = Lesson.objects.filter(
        year_of_study=child.year_of_study,
        group_letter=child.group_letter,
        subject__title=subject_title
    ).order_by('-date').first()
    
    if not lesson:
        print(f"Уроки по предмету {subject_title} для {child.full_name} не найдены")
        return

    Commendation.objects.create(
        text="Хвалю!",
        created=lesson.date,
        schoolkid=child,
        subject=lesson.subject,
        teacher=lesson.teacher
    )
