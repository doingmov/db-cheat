from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation

def fix_marks(schoolkid):
    if not schoolkid:
        return
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)
    

def remove_chastisements(schoolkid):
    if not schoolkid:
        return
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def get_schoolkid_by_name(schoolkid_name):
    try:
        return Schoolkid.objects.get(full_name__icontains=schoolkid_name)
    except (Schoolkid.DoesNotExist, Schoolkid.MultipleObjectsReturned):
        return


def create_commendation(schoolkid_name, subject_title):
    child = get_schoolkid_by_name(schoolkid_name)
    if child is None:
        return

    lesson = Lesson.objects.filter(
        year_of_study=child.year_of_study,
        group_letter=child.group_letter,
        subject__title=subject_title
    ).order_by('-date').first()

    if not lesson:
        return

    Commendation.objects.create(
        text="Хвалю!",
        created=lesson.date,
        schoolkid=child,
        subject=lesson.subject,
        teacher=lesson.teacher
    )

