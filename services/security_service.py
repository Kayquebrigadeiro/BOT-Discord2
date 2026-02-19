class SecurityService:
    @staticmethod
    def is_user_blacklisted(user_id):
        # Placeholder: check blacklist
        return False

    @staticmethod
    def log_action(user_id, action):
        # Placeholder: log to file
        print(f"Log: {user_id} - {action}")