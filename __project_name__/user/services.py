from __project_name__.user.models import User
from __project_name__.user.schemas import UserInputSchema, UserUpdateSchema
from __project_name__.base.services import BaseCRUDServices
from __project_name__.utils import mail


class UserServices(BaseCRUDServices[User, UserInputSchema, UserUpdateSchema]):

    def reset_password_email(self, email: str) -> None:

        user = self.model.query.filter_by(email=email).first()

        if user is not None:

            mail.send_mail(sender='sender',
                           to=user.email,
                           subject='Subject',
                           template='template',
                           name=user.name,
                           link='link',
                           token=user.token(60))

    def reset_password(self, id: int, password: str) -> None:

        user = self.model.query.get_or_404(id)

        user.password = password
        user.update()

        mail.send_mail(sender='sender',
                       to=user.email,
                       subject='Subject',
                       template='template')

    def change_password(self, id: int, password: str, new_password: str) -> bool:

        user = self.model.query.get_or_404(id)

        if user.verify_password(password):
            user.password = new_password
            user.update()
            return True

        return False


user_services = UserServices(User)
