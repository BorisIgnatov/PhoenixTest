import httpx
from ..models import CustomUser


async def call_api(user: CustomUser):
    async with httpx.AsyncClient() as client:
        body = {'request_id': 'e1477272-88d1-4acc-8e03-7008cdedc81e', 'ClubId': user.club_id, 'Method': 'GetSpecialList',
                'Parameters': {'ServiceId': ''}}
        r = await client.post("http://borisignatov1.pythonanywhere.com/users/integration", data=body,
                              auth=(user.username, user.password))
        #print(r.text)
    return r.text