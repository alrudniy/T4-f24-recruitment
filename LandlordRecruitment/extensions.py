from LandlordRecruitment import loginManager
from LandlordRecruitment.models import User

@loginManager.user_loader
def loadUser(id):
    user = User.query.get(int(id))
    return user