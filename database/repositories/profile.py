from django.db.models import Q

from database.models import Profile


class ProfileRepo:
    @staticmethod
    def get_profiles():
        return Profile.objects.all()

    @staticmethod
    def get_profile(id_or_oid: int | str) -> Profile | None:
        return Profile.objects.filter(Q(id=id_or_oid) | Q(oid=id_or_oid)).first()

    @staticmethod
    def get_profile_by_user_id(user_id: int) -> Profile | None:
        return Profile.objects.filter(user=user_id).first()

    @staticmethod
    def create_profile(name: str, email: str, user_id: int, phone: str | None = None) -> Profile:
        data = Profile.objects.create(
            name=name,
            email=email,
            phone=phone,
            user_id=user_id,
        )

        return data

    @staticmethod
    def manager():
        return Profile.objects
