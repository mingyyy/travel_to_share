import app_user.constants as cons
from app_user.models import Language, Topic

# lan_list=[]
# for x,y in enumerate(cons.LANGUAGE_LIST):
#     lan_list.append(Language(id=x, language=y))
#
# print(lan_list)


for y in cons.LANGUAGE_LIST:
    p = Language.objects.create(language=y)
    p.save()

for x in cons.SUBJECT_LIST:
    t = Topic.objects.create(topic=x)
    t.save()
