import vk_api
import time
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем токен доступа из переменной окружения
access_token = os.getenv("VK_ACCESS_TOKEN")

if not access_token:
    print("🔑 Токен доступа не найден. Убедитесь, что он указан в .env файле.")
    exit(1)

# Инициализируем сессию VK API с токеном доступа
vk_session = vk_api.VkApi(token=access_token)
vk = vk_session.get_api()

def print_banner():
    print("\n" + "="*50)
    print("         🎉 VK Cleaner by Alex2289 🎉        ".center(50))
    print("="*50)
    print("\n" + "              Добро пожаловать!              ".center(50))
    print("   Этот инструмент поможет вам удалить      ".center(50))
    print("  непрочитанные сообщения, заявки в друзья,  ".center(50))
    print("  приглашения в группы и все диалоги.       ".center(50))
    print("="*50 + "\n")

def delete_unread_conversations():
    while True:
        response = vk.messages.getConversations(filter='unread')

        if not response.get('items'):
            print("\n📭 Непрочитанных сообщений нет.\n")
            break
        
        dialogs = response['items']
        for dialog in dialogs:
            peer_id = dialog['conversation']['peer']['id']
            try:
                vk.messages.deleteConversation(peer_id=peer_id)
                print(f"✅ Удален диалог с peer_id: {peer_id}")
                time.sleep(2)
            except vk_api.exceptions.ApiError as e:
                if e.code == 9:  # Flood control error
                    print("⏳ Flood control активирован. Ожидание 30 секунд.")
                    time.sleep(30)
                else:
                    print(f"❌ Произошла ошибка: {e}")
                    return

def delete_friend_requests():
    while True:
        response = vk.friends.getRequests(filter='incoming')
        if not response['items']:
            print("\n🚫 Входящих заявок в друзья нет.\n")
            break
        
        for user_id in response['items']:
            try:
                vk.friends.delete(user_id=user_id)
                print(f"🚷 Заявка в друзья от пользователя {user_id} отклонена.")
                time.sleep(2)
            except vk_api.exceptions.ApiError as e:
                if e.code == 9:
                    print("⏳ Flood control активирован. Ожидание 30 секунд.")
                    time.sleep(30)
                else:
                    print(f"❌ Произошла ошибка: {e}")
                    return

def delete_group_invites():
    while True:
        response = vk.groups.getInvites()
        
        if not response.get('items'):
            print("\n🚫 Входящих приглашений в группы нет.\n")
            break
        
        for invite in response['items']:
            if 'id' in invite:
                group_id = invite['id']
                try:
                    vk.groups.leave(group_id=group_id)
                    print(f"🚪 Приглашение в группу {group_id} отклонено.")
                    time.sleep(2)
                except vk_api.exceptions.ApiError as e:
                    if e.code == 9:
                        print("⏳ Flood control активирован. Ожидание 30 секунд.")
                        time.sleep(30)
                    else:
                        print(f"❌ Произошла ошибка: {e}")
                        return
            else:
                print("⚠️ Нет доступного group_id в приглашении.")

def delete_all_dialogs():
    while True:
        response = vk.messages.getConversations()

        if not response.get('items'):
            print("\n🚫 Нет доступных диалогов для удаления.\n")
            break
        
        dialogs = response['items']
        for dialog in dialogs:
            peer_id = dialog['conversation']['peer']['id']
            try:
                vk.messages.deleteConversation(peer_id=peer_id)
                print(f"🗑️ Удален диалог с peer_id: {peer_id}")
                time.sleep(2)
            except vk_api.exceptions.ApiError as e:
                if e.code == 9:
                    print("⏳ Flood control активирован. Ожидание 30 секунд.")
                    time.sleep(30)
                else:
                    print(f"❌ Произошла ошибка: {e}")
                    return

def main_menu():
    print_banner()  # Выводим баннер в начале меню
    while True:
        print("\n🛠️ Меню:")
        print("📬 1. Удалить все непрочитанные сообщения")
        print("🤝 2. Удалить входящие заявки в друзья")
        print("📢 3. Удалить входящие приглашения в группы")
        print("🗨️  4. Удалить все диалоги")
        print("❌ 5. Выход")

        choice = input("Выберите действие (1, 2, 3, 4 или 5): ")
        
        if choice == '1':
            delete_unread_conversations()
        elif choice == '2':
            delete_friend_requests()
        elif choice == '3':
            delete_group_invites()
        elif choice == '4':
            delete_all_dialogs()
        elif choice == '5':
            print("👋 Выход из программы.")
            break
        else:
            print("❗ Неверный ввод, попробуйте снова.")

# Запускаем главное меню
main_menu()
