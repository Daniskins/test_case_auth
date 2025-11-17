from datetime import datetime, timezone, timedelta
from crud.users import read_json, write_json
from crud.sessions import read_json as read_sessions, write_json as write_sessions
from core.security import hash_password_or_token, generate_id, verify_password, make_token

def register_user(email: str,
                  password: str,
                  first_name: str,
                  last_name: str,
                  middle_name: str='',
                  ) -> None:
    if any(el['email'] == email for el in read_json()['users']):
       raise ValueError('Данный адрес электронной почты уже существует')
    password_hash = hash_password_or_token(password) #Хэшируем пароль пользователя
    new_user = {
        'id' : generate_id(),
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'middle_name': middle_name,
        'pwd_hash': password_hash,
        'is_active': True,
        'created_at': datetime.now(timezone.utc).isoformat()
    }
    data = read_json()
    data['users'].append(new_user)
    write_json(data)

def login_user(email: str, password: str) -> dict:
    users = read_json()
    sessions = read_sessions()
    for user in users['users']:
        if (user['email'] == email
        and verify_password(hash_password_or_token(password), user['pwd_hash'])
        and user['is_active']):
            #Создаем сессию со сроком действия 31 день
            token = make_token()
            current_user = {
                'session_hash': hash_password_or_token(token),
                'user_id': user['id'],
                'is_active': True,
                'created_at': datetime.now(timezone.utc).isoformat(),
                'expired_at': (datetime.now(timezone.utc) + timedelta(days=31)).isoformat()
            }
            sessions['sessions'].append(current_user)
            write_sessions(sessions)
            #Возвращаем токен и id пользователя
            return {'user_id': user['id'], 'session_token': token}
    else:
        raise ValueError('Неверный адрес электронной почты или пароль')

def logout_user(token: str) -> None:
    #Выключаем сессию при совпадении токена
    sessions = read_sessions()
    hashed_token = hash_password_or_token(token)
    for session in sessions['sessions']:
        if verify_password(hashed_token, session['session_hash']):
            session['is_active'] = False
            write_sessions(sessions)
            return
    raise ValueError('Сессия не найдена или уже завершена')

def delete_user(user_id: str) -> None:
    #Мягкое удаление пользователя сделав ее неактивной
    for user in read_json()['users']:
        if user['id'] == user_id:
            user['is_active'] = False
            break

def auth_session(token: str) -> dict:
    hashed_token = hash_password_or_token(token)
    now = datetime.now(timezone.utc)
    for session in read_sessions()['sessions']:
        session_hash = session.get('session_hash')
        expired_at = session.get('expired_at')
        if not (session_hash and expired_at):
            continue
        try:
            expires_at = datetime.fromisoformat(expired_at)
        except ValueError:
            continue
        if (verify_password(hashed_token, session_hash)
            and session.get('is_active', True)
            and now < expires_at):
            # При успешной авторизации возвращаем токен и id пользователя
            return {'user_id': session['user_id'], 'session_token': token}
    raise ValueError('Пользователь не авторизован')
