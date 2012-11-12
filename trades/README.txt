python manage.py runserver
Ajax, JQuery, and GET
http://127.0.0.1:8000/trades/search_game/
POST and JSON
http://127.0.0.1:8000/trades/search_form/

python manage.py shell
from trades.models import Users, Userratings
u1=Users(name="AAA")
u2=Users(name="BBB")
u1.save()
u2.save()
u1.id
u1.name
u2.id
u2.name
r=Userratings(rating=5,senderID=u1,receiverID=u2)
r.save()
r.id
r.rating
r.senderID.id
r.senderID.name
r. receiverID.id
r. receiverID.name