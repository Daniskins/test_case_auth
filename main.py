"""Небольшая демонстрация возможностей модуля core.operations."""

from core.operations import (
    register_user,
    login_user,
    auth_session,
    logout_user,
)


def demo_register_users() -> None:
    print("\n=== Регистрация пользователей ===")
    users = [
        {
            'email': 'danis_90@mail.ru',
            'password': '24031990',
            'first_name': 'Danis',
            'last_name': 'Khisamutdinov',
            'middle_name': 'Khanifovich',
        },
        {
            'email': 'test@gmail.ru',
            'password': 'test111',
            'first_name': 'Tester',
            'last_name': 'Testerov',
            'middle_name': '',
        },
    ]

    for user in users:
        try:
            register_user(
                user['email'],
                user['password'],
                user['first_name'],
                user['last_name'],
                user['middle_name'],
            )
        except ValueError as err:
            print(f"- {user['email']}: {err}")
        else:
            print(f"- {user['email']}: успешно зарегистрирован")


def demo_login_and_session() -> None:
    print("\n=== Вход пользователей ===")
    credentials = [
        ('danis_90@mail.ru', '24031990'),
        ('test@gmail.ru', 'test111'),
    ]
    tokens: dict[str, str] = {}

    for email, password in credentials:
        try:
            result = login_user(email, password)
        except ValueError as err:
            print(f"- {email}: {err}")
        else:
            token = result['session_token']
            tokens[email] = token
            print(f"- {email}: вошёл. Токен {token[:12]}...")

    print("\n=== Проверка активных сессий ===")
    for email, token in tokens.items():
        try:
            session_info = auth_session(token)
        except ValueError as err:
            print(f"- {email}: {err}")
        else:
            print(f"- {email}: сессия активна -> {session_info}")

    if tokens:
        email, token = next(iter(tokens.items()))
        print(f"\n=== Выход пользователя {email} ===")
        try:
            logout_user(token)
        except ValueError as err:
            print(f"- {email}: {err}")
        else:
            print(f"- {email}: сессия завершена")

        print("\n=== Повторная проверка сессии ===")
        try:
            auth_session(token)
        except ValueError as err:
            print(f"- {email}: ожидаемая ошибка -> {err}")


def main() -> None:
    demo_register_users()
    demo_login_and_session()


if __name__ == "__main__":
    main()

