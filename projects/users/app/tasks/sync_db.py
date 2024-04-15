from app.config.settings import Config
from app.models.users import User
from app.services.users import UsersService
from app.utils.user_cache import UserCache


async def sync_users(db, sleep):
    while Config.SYNC_USERS:
        if UserCache.users:
            process_users = UserCache.users[: Config.TOTAL_USERS_BY_RUN]
            repeated_users = db.query(User).filter(User.email.in_([user.email for user in process_users])).all()
            for user in repeated_users:
                UserCache.users_with_errors_by_email_map[user.email] = user

            users_to_save = [user for user in process_users if user.email not in [repeated_user.email for repeated_user in repeated_users]]
            users_created = UsersService(db).create_users(users_to_save)
            UserCache.users = UserCache.users[Config.TOTAL_USERS_BY_RUN :]
            UserCache.users_success_by_email_map.update({user["email"]: user for user in users_created})
        await sleep(1)
