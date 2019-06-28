from config import settings


settings.change_url("test")
print(settings.BASE_URL)