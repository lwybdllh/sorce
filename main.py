#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot with SQLite Database
Enhanced version with improved text formatting and additional commands
"""

import requests
import json
import time
import datetime
import os
from database import BotDatabase

# Bot Configuration
API_TOKEN = '8365541805:AAGA-vNLqUedfYZrw_55B6ddji3oyf0yJiY'
SUDO_ID = 8033941376
BOT_ID = 8365541805
ANTI_SAFE_BOT_USERNAME = "@source_protect_bot"

# Initialize Database
db = BotDatabase('bot_data.db')

# Bot Buttons
DEV_BUTTONS = {
    'inline_keyboard': [
        [{'text': '𓄼𝗗𝗲𝘃𓄹', 'url': 'https://t.me/boststot'}],
        [{'text': '𓄼𝗦𝗼𝘂𝗿𝗰𝗲𓄹', 'url': 'https://t.me/Luai_shamer'}]
    ]
}

def bot_request(method, params=None, timeout=60):
    """Make request to Telegram Bot API"""
    url = f"https://api.telegram.org/bot{API_TOKEN}/{method}"
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            if params:
                response = requests.post(url, json=params, timeout=timeout)
            else:
                response = requests.get(url, timeout=timeout)
            return response.json()
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                print(f"Timeout on attempt {attempt + 1}, retrying...")
                time.sleep(2)
                continue
            else:
                print(f"Error in bot_request: Timeout after {max_retries} attempts")
                return None
        except Exception as e:
            print(f"Error in bot_request: {e}")
            return None
    
    return None

def get_chat_member_status(chat_id, user_id):
    """Get user status in chat"""
    result = bot_request('getChatMember', {'chat_id': chat_id, 'user_id': user_id})
    if result and result.get('ok'):
        return result['result']['status']
    return 'member'

def handle_message(update):
    """Handle incoming messages"""
    message = update.get('message')
    if not message:
        return

    # Extract message info
    chat_id = message.get('chat', {}).get('id')
    chat_type = message.get('chat', {}).get('type')
    from_id = message.get('from', {}).get('id')
    message_id = message.get('message_id')
    text = message.get('text', '').strip()
    
    user_name = message.get('from', {}).get('first_name', 'User')
    user_username = message.get('from', {}).get('username', 'no_username')
    
    reply_to_message = message.get('reply_to_message')
    new_chat_member = message.get('new_chat_member')
    left_chat_member = message.get('left_chat_member')
    
    # Reply info
    re_id = reply_to_message.get('from', {}).get('id') if reply_to_message else None
    re_user = reply_to_message.get('from', {}).get('username', 'no_username') if reply_to_message else None
    re_msgid = reply_to_message.get('message_id') if reply_to_message else None
    
    # Get user and bot status
    group_status = get_chat_member_status(chat_id, from_id) if chat_type in ['group', 'supergroup'] else 'member'
    bot_group_status = get_chat_member_status(chat_id, BOT_ID) if chat_type in ['group', 'supergroup'] else 'member'
    
    # Check if bot is enabled in this group
    groups = db.get_all_groups()
    is_enabled = chat_id in groups
    
    # Get group settings
    settings = db.get_group_settings(chat_id)
    
    # Message count
    if chat_type in ['group', 'supergroup'] and is_enabled:
        db.increment_message_count(chat_id, from_id)
        user_message_count = db.get_message_count(chat_id, from_id)
    else:
        user_message_count = 0
    
    # Check permissions
    is_admin_or_creator = (group_status in ['creator', 'administrator'] or from_id == SUDO_ID)
    can_manage_roles = (from_id == SUDO_ID or 
                       db.has_role(0, from_id, 'developer') or 
                       db.has_role(chat_id, from_id, 'manager') or 
                       db.has_role(chat_id, from_id, 'creator'))
    
    # /start command in private
    if text == "/start" and chat_type == "private":
        db.add_private_member(from_id)
        
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "💯¦ مـرحبآ آنآ بوت آسـمـي العملاق 🎖\n"
                "💰¦ آختصـآصـي حمـآيهہ‌‏ آلمـجمـوعآت\n"
                "📛¦ مـن آلسـبآم وآلتوجيهہ‌‏ وآلتگرآر وآلخ...\n"
                "🚸¦ البوت خدمي ومتاح للكل \n"
                "👷🏽¦ فقط اضف البوت لمجموعتك وارفعه مشرف  \n"
                "  ثم ارسل تفعيل\n\n"
                "⚖️¦ مـعرف آلمـطـور  : @Luai_shamer 👨🏽‍🔧"
            ),
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
        
        # Log to sudo
        current_time = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=3)))
        time_str = current_time.strftime("%H:%M")
        date_str = current_time.strftime("%Y/%m/%d")
        
        bot_request('sendMessage', {
            'chat_id': SUDO_ID,
            'text': (
                "شخص قام بالدخول إلى البوت\n"
                "ــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n"
                "ℓ☯️- المعرف الخاص بالعضو\n"
                f"ℓ🅿️- @{user_username}\n"
                "➖➖\n"
                "ℓ✳️- الاسم الخاص بالعضو\n"
                f"ℓ📳- {user_name}\n"
                "➖➖\n"
                "ℓ🚹- الايدي الخاص بالعضو\n"
                f"ℓ🆔- {from_id}\n"
                "➖➖\n"
                "ـ➖➖➖➖\n"
                f"⏰┇الساعة :: {time_str}\n"
                f"📆┇التاريخ :: {date_str}\n"
                "ـ➖➖➖➖\n"
                "📮"
            ),
            'parse_mode': "Markdown",
            'disable_web_page_preview': True
        })

    # Bot added to group
    if new_chat_member and new_chat_member.get('id') == BOT_ID:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "💯 مـرحبآ آنآ بوت حمايه\n"
                "¦ آختصـآصـي حمـآيهہ‏‏ آلمـجمـوعآت\n"
                "¦ مـن آلسـبآم وآلتوجيهہ‏‏ وآلتگرآر وآلخ...\n"
                "¦ مـعرف آلمـطـور  : @Luai_shamer"
            ),
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Enable/Disable bot
    if text == "تفعيل" and is_admin_or_creator:
        db.add_group(chat_id, message.get('chat', {}).get('title', 'Unknown'))
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "🎖¦ آهہ‏‏لآ عزيزي\n🔅¦ تم تفعيل البوت \n✓",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    if text == "تعطيل" and is_admin_or_creator:
        db.remove_group(chat_id)
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "🎖¦ آهہ‏‏لآ عزيزي\n🔅¦ تم تعطيل البوت \n✓",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # ====== ID COMMAND ======
    if text in ["ايدي", "أيدي", "ايديي", "إيدي", "id", "ID", "ٱيدي"]:
        try:
            response_text = (
                "━━━━━━━━━━━━━━━━━━\n"
                f"👤¦ Name : {user_name}\n"
                f"🆔¦ ID : `{from_id}`\n"
                f"📮¦ Username : @{user_username}\n"
                "━━━━━━━━━━━━━━━━━━"
            )
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': response_text,
                'parse_mode': 'MarkDown',
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        except Exception as e:
            print(f"Error in ID command: {e}")
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': f"🆔¦ Your ID: {from_id}",
                'reply_to_message_id': message_id
            })

    # Protection system
    if chat_type == "supergroup" and is_enabled:
        if group_status not in ["creator", "administrator"] and from_id != SUDO_ID:
            # Photo lock
            if message.get('photo') and settings.get('photo_lock') == 'l':
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
                return
            
            # Video lock
            if message.get('video') and settings.get('video_lock') == 'l':
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
                return
            
            # Audio lock
            if message.get('audio') and settings.get('audio_lock') == 'l':
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
                return
            
            # Voice lock
            if message.get('voice') and settings.get('voice_lock') == 'l':
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
                return
            
            # Sticker lock
            if message.get('sticker') and settings.get('sticker_lock') == 'l':
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
                return
            
            # Document lock
            if message.get('document') and settings.get('doc_lock') == 'l':
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
                return
            
            # Contact lock
            if message.get('contact') and settings.get('contact_lock') == 'l':
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
                return
            
            # Forward lock
            if message.get('forward_from') and settings.get('fwd_lock') == 'l':
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
                return
            
            # Link lock
            if text and settings.get('link_lock') == 'l':
                if any(x in text.lower() for x in ['http://', 'https://', 't.me/', 'telegram.me/']):
                    bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
                    return
            
            # Tag lock (@username or #hashtag)
            if text and settings.get('tag_lock') == 'l':
                if '@' in text or '#' in text:
                    bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
                    return
            
            # Markdown lock
            if message.get('entities') and settings.get('markdown_lock') == 'l':
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
                return
            
            # Bots lock
            if new_chat_member and new_chat_member.get('is_bot') and settings.get('bots_lock') == 'l':
                if new_chat_member.get('id') != BOT_ID:
                    bot_request('kickChatMember', {'chat_id': chat_id, 'user_id': new_chat_member.get('id')})
                    bot_request('sendMessage', {
                        'chat_id': chat_id,
                        'text': (
                            f"👤¦ آلعضـو : @{new_chat_member.get('username')}\n"
                            f"👤¦ الايدي : {new_chat_member.get('id')} \n"
                            "🚫¦ مـمـنوع آضـآفهہ آلبوتآت \n"
                            "📛¦ تم طـرد آلبوت \n✘"
                        ),
                        'reply_markup': json.dumps(DEV_BUTTONS)
                    })
                    return

    # Lock/Unlock commands
    if bot_group_status == "administrator" and is_admin_or_creator:
        lock_commands = {
            "قفل الصور": {'photo_lock': 'l'},
            "فتح الصور": {'photo_lock': 'o'},
            "قفل الفيديو": {'video_lock': 'l'},
            "فتح الفيديو": {'video_lock': 'o'},
            "قفل الصوت": {'audio_lock': 'l'},
            "فتح الصوت": {'audio_lock': 'o'},
            "قفل البصمات": {'voice_lock': 'l'},
            "فتح البصمات": {'voice_lock': 'o'},
            "قفل الملصقات": {'sticker_lock': 'l'},
            "فتح الملصقات": {'sticker_lock': 'o'},
            "قفل الملفات": {'doc_lock': 'l'},
            "فتح الملفات": {'doc_lock': 'o'},
            "قفل الجهات": {'contact_lock': 'l'},
            "فتح الجهات": {'contact_lock': 'o'},
            "قفل التوجيه": {'fwd_lock': 'l'},
            "فتح التوجيه": {'fwd_lock': 'o'},
            "قفل الروابط": {'link_lock': 'l'},
            "فتح الروابط": {'link_lock': 'o'},
            "قفل التاك": {'tag_lock': 'l'},
            "فتح التاك": {'tag_lock': 'o'},
            "قفل المعرفات": {'tag_lock': 'l'},
            "فتح المعرفات": {'tag_lock': 'o'},
            "قفل الماركدون": {'markdown_lock': 'l'},
            "فتح الماركدون": {'markdown_lock': 'o'},
            "قفل البوتات": {'bots_lock': 'l'},
            "فتح البوتات": {'bots_lock': 'o'},
            "قفل الايدي": {'id_lock': 'l'},
            "فتح الايدي": {'id_lock': 'o'},
        }
        
        if text in lock_commands:
            db.update_group_settings(chat_id, lock_commands[text])
            action = "قفل" if list(lock_commands[text].values())[0] == 'l' else "فتح"
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': f"🎖¦ آهہ‏‏لآ عزيزي\n🔅¦ تم {action} الخاصية \n✓",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
    else:
        # Check if member tried to use lock commands
        all_lock_commands = [
            "قفل الصور", "فتح الصور", "قفل الفيديو", "فتح الفيديو",
            "قفل الصوت", "فتح الصوت", "قفل البصمات", "فتح البصمات",
            "قفل الملصقات", "فتح الملصقات", "قفل الملفات", "فتح الملفات",
            "قفل الجهات", "فتح الجهات", "قفل التوجيه", "فتح التوجيه",
            "قفل الروابط", "فتح الروابط", "قفل التاك", "فتح التاك",
            "قفل المعرفات", "فتح المعرفات", "قفل الماركدون", "فتح الماركدون",
            "قفل البوتات", "فتح البوتات", "قفل الايدي", "فتح الايدي"
        ]
        if text in all_lock_commands:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "⚠️¦ عذراً، هذا الأمر للأدمنية فقط\n👮‍♂️¦ يجب أن تكون أدمن لاستخدام أوامر القفل والفتح",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # Admin commands
    if bot_group_status == "administrator" and is_admin_or_creator:
        # Delete message
        if reply_to_message and text == "حذف":
            bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': re_msgid})
        
        # Ban/Kick
        if reply_to_message and re_id != BOT_ID and re_id != SUDO_ID and text in ["حظر", "طرد", "/ban", "/kick"]:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    f"¦ العضو » @{re_user}\n"
                    f"¦ الايدي » ( {re_id} )\n"
                    "¦ تم الحظر \n✓️"
                ),
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
            bot_request('kickChatMember', {'chat_id': chat_id, 'user_id': re_id})
        
        # Unban
        if reply_to_message and re_id != BOT_ID and re_id != SUDO_ID and text in ["الغاء الحظر", "/unban"]:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    f"¦ العضو » @{re_user}\n"
                    f"¦ الايدي » ( {re_id} )\n"
                    "¦ تم الغاء الحظر \n✓️"
                ),
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
            bot_request('unbanChatMember', {'chat_id': chat_id, 'user_id': re_id})
        
        # Mute
        if reply_to_message and re_id != BOT_ID and re_id != SUDO_ID and text == "كتم":
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    f"👤¦ العضو » @{re_user}\n"
                    f"🎫¦ الايدي » ( {re_id} )\n"
                    "🛠¦ تم كتمه\n✓️"
                ),
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
            bot_request('restrictChatMember', {
                'chat_id': chat_id,
                'user_id': re_id,
                'permissions': {'can_send_messages': False}
            })
        
        # Unmute
        if reply_to_message and re_id != BOT_ID and re_id != SUDO_ID and text == "الغاء الكتم":
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    f"👤¦ العضو » @{re_user}\n"
                    f"🎫¦ الايدي » ( {re_id} )\n"
                    "🛠¦ تم الغاء كتمه\n✓"
                ),
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
            bot_request('restrictChatMember', {
                'chat_id': chat_id,
                'user_id': re_id,
                'permissions': {
                    'can_send_messages': True,
                    'can_send_media_messages': True,
                    'can_send_polls': True,
                    'can_send_other_messages': True
                }
            })
        
        # Restrict
        if reply_to_message and re_id != BOT_ID and re_id != SUDO_ID and text == "تقييد":
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    f"👤¦ العضو » @{re_user}\n"
                    f"🎫¦ الايدي » ( {re_id} )\n"
                    "🛠¦ تم تقييده \n✓️"
                ),
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
            bot_request('restrictChatMember', {
                'chat_id': chat_id,
                'user_id': re_id,
                'permissions': {'can_send_messages': False}
            })
        
        # Unrestrict
        if reply_to_message and re_id != BOT_ID and re_id != SUDO_ID and text == "الغاء التقييد":
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    f"👤¦ العضو » @{re_user} \n"
                    f"🎫¦ الايدي » ( {re_id} )\n"
                    "🛠¦ تم الغاء تقييده \n✓️"
                ),
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
            bot_request('restrictChatMember', {
                'chat_id': chat_id,
                'user_id': re_id,
                'permissions': {
                    'can_send_messages': True,
                    'can_send_audios': True,
                    'can_send_documents': True,
                    'can_send_photos': True,
                    'can_send_videos': True,
                    'can_send_video_notes': True,
                    'can_send_voice_notes': True,
                    'can_send_other_messages': True
                }
            })
        
        # Promote to admin
        if reply_to_message and text in ["رفع ادمن", "/promote"]:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    f"¦ العضو » @{re_user}\n"
                    f"¦ الايدي » ( {re_id} )\n"
                    "¦ تمت ترقيته ليصبح ادمن \n✓️"
                ),
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
            bot_request('promoteChatMember', {
                'chat_id': chat_id,
                'user_id': re_id,
                'can_manage_chat': True,
                'can_delete_messages': True,
                'can_invite_users': True,
                'can_restrict_members': True,
                'can_pin_messages': True,
                'can_promote_members': False
            })
        
        # Demote admin
        if reply_to_message and re_id != BOT_ID and re_id != SUDO_ID and text in ["تنزيل ادمن", "/kool"]:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    f"👤¦ العضو » @{re_user} \n"
                    f"🎫¦ الايدي » ( {re_id} )\n"
                    "🛠¦ تمت تنزيل الادمن \n✓️"
                ),
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
            bot_request('promoteChatMember', {
                'chat_id': chat_id,
                'user_id': re_id,
                'can_manage_chat': False,
                'can_delete_messages': False,
                'can_invite_users': False,
                'can_restrict_members': False,
                'can_pin_messages': False,
                'can_promote_members': False
            })
        
        # Set group name
        if text and (text.startswith("ضع اسم ") or text.startswith("/setname ")):
            new_title = text.replace("ضع اسم ", "").replace("/setname ", "").strip()
            bot_request('setChatTitle', {'chat_id': chat_id, 'title': new_title})
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': f"تم تغيير اسم المجموعة إلى: {new_title}",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        
        # Pin message
        if reply_to_message and text in ["تثبيت", "pin"]:
            bot_request('pinChatMessage', {
                'chat_id': chat_id,
                'message_id': re_msgid
            })
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "¦ أهلا  \n¦ تم تثبيت الرساله \n✓",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        
        # Set/Delete chat photo
        if text == 'ضع صورة' and reply_to_message and reply_to_message.get('photo'):
            photo_file_id = reply_to_message['photo'][-1]['file_id']
            bot_request('setChatPhoto', {'chat_id': chat_id, 'photo': photo_file_id})
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "✅┇ تم وضع صورة للمجموعة بنجاح\n✔️ ",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        
        if text == 'حذف الصورة':
            bot_request('deleteChatPhoto', {'chat_id': chat_id})
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "❌┇ تم حذف صورة المجموعة بنجاح\n❌ ",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # Custom filters (Replies)
    if is_admin_or_creator:
        # Add filter
        if text and text.startswith("اضف رد "):
            parts = text.split('\n', 1)
            if len(parts) == 2:
                trigger = parts[0].replace("اضف رد ", "").strip()
                response = parts[1].strip()
                db.add_filter(chat_id, trigger, response)
                bot_request('sendMessage', {
                    'chat_id': chat_id,
                    'text': f"تم اضافة الرد:\n{trigger}",
                    'reply_to_message_id': message_id,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
        
        # Delete filter
        if text and text.startswith("حذف رد "):
            trigger = text.replace("حذف رد ", "").strip()
            db.delete_filter(chat_id, trigger)
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': f"تم حذف الرد:\n{trigger}",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        
        # List filters
        if text == "الردود":
            filters = db.get_all_filters(chat_id)
            if filters:
                filter_list = "\n".join([f"- {f}" for f in filters])
                bot_request('sendMessage', {
                    'chat_id': chat_id,
                    'text': f"قائمة الردود:\n{filter_list}",
                    'reply_to_message_id': message_id,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
            else:
                bot_request('sendMessage', {
                    'chat_id': chat_id,
                    'text': "لا توجد ردود مخصصة",
                    'reply_to_message_id': message_id,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
        
        # Clear all filters
        if text == "مسح الردود":
            db.delete_all_filters(chat_id)
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "تم مسح جميع الردود",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # Check for filter match
    if text and is_enabled:
        filter_response = db.get_filter(chat_id, text)
        if filter_response:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': filter_response,
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # Custom roles management
    # Developer role (SUDO only)
    if from_id == SUDO_ID and reply_to_message:
        if text == "رفع مطور":
            db.add_role(0, re_id, 'developer')
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': f"تم رفع المطور: {re_id}",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        elif text == "تنزيل مطور":
            db.remove_role(0, re_id, 'developer')
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': f"تم تنزيل المطور: {re_id}",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
    
    # Manager role
    if can_manage_roles and reply_to_message:
        if text == "رفع مدير":
            db.add_role(chat_id, re_id, 'manager')
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': f"تم رفع المدير: {re_id}",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        elif text == "تنزيل مدير":
            db.remove_role(chat_id, re_id, 'manager')
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': f"تم تنزيل المدير: {re_id}",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
    
    # Creator role
    if (from_id == SUDO_ID or db.has_role(0, from_id, 'developer')) and reply_to_message:
        if text == "رفع منشى":
            db.add_role(chat_id, re_id, 'creator')
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': f"تم رفع المنشىء: {re_id}",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        elif text == "تنزيل منشى":
            db.remove_role(chat_id, re_id, 'creator')
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': f"تم تنزيل المنشىء: {re_id}",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
    
    # Distinguished member role
    if can_manage_roles and reply_to_message:
        if text == "رفع عضو مميز":
            db.add_role(chat_id, re_id, 'distinguished')
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': f"تم رفع العضو المميز: {re_id}",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        elif text == "تنزيل عضو مميز":
            db.remove_role(chat_id, re_id, 'distinguished')
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': f"تم تنزيل العضو المميز: {re_id}",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # List roles
    if from_id == SUDO_ID and text == "المطورين":
        devs = db.get_users_by_role(0, 'developer')
        devs_str = "\n".join([str(d) for d in devs]) if devs else "لا يوجد مطورين"
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"قائمة المطورين:\n{devs_str}",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    if can_manage_roles and text == "المدراء":
        managers = db.get_users_by_role(chat_id, 'manager')
        managers_str = "\n".join([str(m) for m in managers]) if managers else "لا يوجد مدراء"
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"قائمة المدراء:\n{managers_str}",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    if can_manage_roles and text == "المنشئين":
        creators = db.get_users_by_role(chat_id, 'creator')
        creators_str = "\n".join([str(c) for c in creators]) if creators else "لا يوجد منشئين"
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"قائمة المنشئين:\n{creators_str}",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    if can_manage_roles and text in ["المميزون", "المميزين"]:
        distinguished = db.get_users_by_role(chat_id, 'distinguished')
        distinguished_str = "\n".join([str(d) for d in distinguished]) if distinguished else "لا يوجد أعضاء مميزين"
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"قائمة الأعضاء المميزين:\n{distinguished_str}",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Clear roles
    if from_id == SUDO_ID and text == "مسح المطورين":
        db.delete_all_roles(0, 'developer')
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "تم مسح جميع المطورين",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    if can_manage_roles and text == "مسح المدراء":
        db.delete_all_roles(chat_id, 'manager')
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "تم مسح جميع المدراء",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    if can_manage_roles and text == "مسح المنشئين":
        db.delete_all_roles(chat_id, 'creator')
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "تم مسح جميع المنشئين",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    if can_manage_roles and text in ["حذف المميزين", "مسح المميزين"]:
        db.delete_all_roles(chat_id, 'distinguished')
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "تم مسح جميع الأعضاء المميزين",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # User points/games
    if text in ["نقاطي", "نقاطى", "نقاط", "points"]:
        points = db.get_points(chat_id, from_id)
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"📬¦ عدد نقاطك من اللعبه هي {{ {points} }}",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    if is_admin_or_creator and reply_to_message and text == "مسح النقاط":
        db.reset_points(chat_id, re_id)
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"تم مسح نقاط المستخدم: {re_id}",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Word scramble game
    word_scramble_phrases = [
        ('اســرع واحد يرتب » { ل ، س ، ا ، ق ، ت ،ب ، ا } «', 'استقبال'),
        ('اســرع واحد يرتب » { ه ، ا ، ر ، س ، ي } «', 'سياره'),
        ('اســرع واحد يرتب » { ر ، و ، ح ، س } «', 'سحور'),
        ('اســرع واحد يرتب » { و ، ن ، ي ، ا ، ف } «', 'ايفون'),
        ('اســرع واحد يرتب » { ا ، ش ، ن ، ح } «', 'شاحن'),
        ('اســرع واحد يرتب » { ب ، و ، ر ، و ، ت } «', 'روبوت'),
        ('اســرع واحد يرتب » { ب ، م ، ل ، ا ، س } «', 'ملابس'),
        ('اســرع واحد يرتب » { ض ، ح ، ر ، م ، و ، ت } «', 'حضرموت'),
        ('اســرع واحد يرتب » { ط ، ب ، ي ، ر ، ق } «', 'بطريق'),
        ('اســرع واحد يرتب » { ف ، ي ، س ، ه ، ن } «', 'سفينه'),
        ('اســرع واحد يرتب » { ج ، ا ، ج ، د ، ه } «', 'دجاجه'),
        ('اســرع واحد يرتب » { س ، م ، ر ، د ، ه } «', 'مدرسه'),
        ('اســرع واحد يرتب » { ا ، ا ، ل ، ن ، و } «', 'الوان'),
        ('اســرع واحد يرتب » { ر ، ه ، غ ، ف } «', 'غرفه'),
        ('اســرع واحد يرتب » { ج ، ه ، ل ، ا ، ث } «', 'ثلاجه'),
        ('اســرع واحد يرتب » { خ ، م ، ب ، ط } «', 'مطبخ'),
    ]
    
    if text in ["ترتيب", "الترتيب", "ترتيب الكلمات", "رتب"]:
        import random
        selected = random.choice(word_scramble_phrases)
        db.set_config(f"game_{chat_id}", selected[1])
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': selected[0],
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # Check game answer
    game_answer = db.get_config(f"game_{chat_id}")
    if text and game_answer and text == game_answer:
        db.add_points(chat_id, from_id, 1)
        points = db.get_points(chat_id, from_id)
        db.delete_config(f"game_{chat_id}")
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "🎉¦ مبروك لقد ربحت نقطه\n"
                f"🔖¦ اصبح لديك {{ {points} }} نقطه 🍃️\n"
                "➖"
            ),
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Welcome new member
    if new_chat_member and not new_chat_member.get('is_bot'):
        new_member_id = new_chat_member.get('id')
        new_member_name = new_chat_member.get('first_name')
        
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                f"<a href='tg://user?id={new_member_id}'>{new_member_name}</a>\n\n"
                "🔖¦ مرحباً عزيزي\n"
                "🔖¦ نورت المجموعة \n"
                "💂🏼‍♀️"
            ),
            'reply_to_message_id': message_id,
            'parse_mode': "html",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
        
        # Delete join message
        bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})

    # Bot left group
    if left_chat_member and left_chat_member.get('id') == BOT_ID:
        db.remove_group(chat_id)
        chat_title = message.get('chat', {}).get('title', 'N/A')
        bot_request('sendMessage', {
            'chat_id': SUDO_ID,
            'text': (
                "\n📛| قام شخص بطرد البوت من المجموعه الاتيه : \n"
                f"🏷| ألايدي : {chat_id}\n"
                f"🗯| الـمجموعه : {chat_title}\n\n"
                "📮| تـم مسح كل بيانات المجموعه بنـجاح"
            ),
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Link command
    if text in ["/link", "الرابط"]:
        export_link_response = bot_request("exportChatInviteLink", {"chat_id": chat_id})
        if export_link_response and export_link_response.get("ok"):
            link = export_link_response["result"]
            chat_title = message.get('chat', {}).get('title', 'N/A')
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    "🔖¦رابـط مجمـــوعة: 💯\n"
                    f"🌿¦ {chat_title} :\n\n"
                    f"{link}"
                ),
                'disable_web_page_preview': True,
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "حدث خطأ عند جلب رابط المجموعة. تأكد من أن البوت مسؤول ويمكنه دعوة المستخدمين.",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # Kick myself
    if text == "اطردني":
        if group_status == "member":
            export_link_response = bot_request('exportChatInviteLink', {'chat_id': chat_id})
            invite_link = export_link_response['result'] if export_link_response and export_link_response.get('ok') else 'N/A'
            
            bot_request('kickChatMember', {'chat_id': chat_id, 'user_id': from_id})
            bot_request('unbanChatMember', {'chat_id': chat_id, 'user_id': from_id})
            
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "🚸| لقد تم طردك بنجاح , ارسلت لك رابط المجموعه في الخاص اذا وصلت لك تستطيع الرجوع متى شئت🏻",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
            bot_request('sendMessage', {
                'chat_id': from_id,
                'text': (
                    "👨🏼‍⚕️| اهلا عزيزي , لقد تم طردك من المجموعه بامر منك \n"
                    "🔖| اذا كان هذا بالخطأ او اردت الرجوع للمجموعه \n\n"
                    "🔖¦فهذا رابط المجموعه 💯\n\n"
                    f"🌿¦{invite_link} :"
                ),
                'parse_mode': "HTML",
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "📛¦ لا استطيع طرد المدراء والادمنيه والمنشئين  \n🚶",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # Time command
    if text in ["الساعة", "الزمن", "الساعه", "الوقت"]:
        current_time = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=3)))
        time_str = current_time.strftime("%H:%M")
        ampm = "ص" if current_time.strftime("%p") == "AM" else "م"
        
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"🎖*{time_str} {ampm}*",
            'parse_mode': 'MarkDown',
            'disable_web_page_preview': True,
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # My rank command
    if text in ["رتبتي", "رتبتى", "رتبه", "رتبة"]:
        # Check if group is activated
        if not db.is_group_active(chat_id) and from_id != SUDO_ID:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "⚠️¦ عذراً، البوت غير مفعل في هذه المجموعة\n🔧¦ يرجى تفعيل البوت أولاً",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
            return
        
        if from_id == SUDO_ID:
            rank_text = "مطور اساسي 👨🏻‍✈️"
        elif db.has_role(0, from_id, 'developer'):
            rank_text = "مطور البوت 🗳"
        elif db.has_role(chat_id, from_id, 'creator'):
            rank_text = "المنشئ  🗳"
        elif db.has_role(chat_id, from_id, 'manager'):
            rank_text = "المدير  🗳"
        elif db.has_role(chat_id, from_id, 'distinguished'):
            rank_text = "عضو مميز بالبوت 🗳"
        elif group_status == "creator":
            rank_text = "المنشىء 👷🏽"
        elif group_status == "administrator":
            rank_text = "ادمن في البوت 👨🏼‍🎓"
        else:
            rank_text = "فقط عضو 🙍🏼‍♂️"
        
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"🎫¦ رتبتك » {rank_text} \n🌿",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # "انجب" command
    if text == "انجب":
        if group_status == "creator":
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "حاظر تاج راسي انجبيت 😇",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        elif group_status == "administrator":
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "فوك ما مصعدك ادمن و تكلي انجب 😏 ",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        elif group_status == "member":
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "انجب انته لا تندفر 😒",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # "كله" and "كول" commands
    if text and text.startswith("كله ") and reply_to_message:
        reply_text = text.replace("كله ", "")
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': reply_text,
            'reply_to_message_id': re_msgid,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    if text and text.startswith("كول "):
        say_text = text.replace("كول ", "")
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': say_text,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # "كشف" command (user info by reply)
    if reply_to_message and text == "كشف":
        re_user_status = get_chat_member_status(chat_id, re_id)
        re_user_name = reply_to_message.get('from', {}).get('first_name')
        re_user_username = reply_to_message.get('from', {}).get('username')
        
        if re_id == SUDO_ID:
            actual_rank = "مطور اساسي 👨🏻‍⚕"
        elif db.has_role(0, re_id, 'developer'):
            actual_rank = "مطور البوت 🗳"
        elif db.has_role(chat_id, re_id, 'creator'):
            actual_rank = "المنشئ  🗳"
        elif db.has_role(chat_id, re_id, 'manager'):
            actual_rank = "المدير  🗳"
        elif db.has_role(chat_id, re_id, 'distinguished'):
            actual_rank = "عضو مميز بالبوت 🗳"
        elif re_user_status == "creator":
            actual_rank = "المنشىء 👷"
        elif re_user_status == "administrator":
            actual_rank = "ادمن في البوت 👨🏼‍🎓"
        else:
            actual_rank = "فقط عضو 🙍🏼‍♂️"
        
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                f"🤵🏼¦ الاسم » {{ {re_user_name} }}\n"
                f"🎫¦ الايدي » {{ {re_id} }} \n"
                f"🎟¦ المعرف »{{ @{re_user_username} }}\n"
                f"📮¦ الرتبه » {actual_rank}\n"
                "🕵🏻️‍♀️¦ نوع الكشف » بالرد\n"
                "➖"
            ),
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # List Admins
    if text == "الادمنيه":
        chat_administrators = bot_request('getChatAdministrators', {'chat_id': chat_id})
        admin_list = []
        if chat_administrators and chat_administrators.get('ok'):
            for admin in chat_administrators['result']:
                admin_name = admin['user']['first_name']
                admin_id = admin['user']['id']
                admin_list.append(f"- {admin_name} ({admin_id})")
        
        response_text = "قائمة المشرفين:\n" + "\n".join(admin_list) if admin_list else "لا يوجد مشرفون."
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': response_text,
            'parse_mode': 'MarkDown',
            'disable_web_page_preview': True,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Source command
    if text in ["السورس", "سورس", "السورص", "المصدر", "source"]:
        bot_request('sendMessage', {
        'chat_id': chat_id,
        'text': (
            "💠 ┇ *ســورس الإبــداع والتميّــز* ┇ 💠\n\n"
            "⚙️ السورس ليس مجرد كود، بل عالَم متكامل من الإبداع والدقة.\n"
            "تم تصميمه ليمنحك أفضل أداء وسرعة، مع مظهر أنيق وتحديثات مستمرة.\n\n"
            "🔹 يعتمد على أحدث تقنيات البرمجة.\n"
            "🔹 يدعم الأوامر الذكية والإدارة السلسة.\n"
            "🔹 آمن، سريع، ومفتوح للتطوير.\n\n"
            "💬│للتواصــل مع المطــور: [@Luai_shamer](https://t.me/Luai_shamer)\n"
            "📣│قنــاة الســورس: @boststot\n\n"
            "✨┇ *سـورسُنا يجمـع بين القـوة والجـمال، لأن الإتقـان هـو الهـدف.* ✨"
        ),
        'reply_to_message_id': message_id,
        'parse_mode': 'MARKDOWN',
        'disable_web_page_preview': True,
        'reply_markup': json.dumps(DEV_BUTTONS)
    })


    # Group Info
    if text == "/Group":
        group_info = bot_request('getChat', {'chat_id': chat_id})
        if group_info and group_info.get('ok'):
            group_title = group_info['result']['title']
            group_id = group_info['result']['id']
            member_count_res = bot_request('getChatMembersCount', {'chat_id': chat_id})
            member_count = member_count_res['result'] if member_count_res and member_count_res.get('ok') else 'N/A'
            
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    f"الاسم :⪼ {group_title}\n"
                    f"الايدي :⪼ {group_id}\n"
                    f"عدد الاعضاء :⪼ {member_count}"
                ),
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "حدث خطأ أثناء جلب معلومات المجموعة.",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # Menu commands
    if text in ["م1", "م ١", "اوامر الادارة", "أوامر الادارة", "اوامر الاداره"]:
        if is_admin_or_creator:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    "•⊱ {  آوآمر الرفع والتنزيل  } ⊰•\n\n\n"
                    "📿¦ رفع ادمن ‿ تنزيل ادمن  \n\n \n"
                    "⦅آوآمـر آلحظـر وآلطــرد وآلتقييـد  ⦆\n      \n"
                    "🔱¦ حظر (بالرد/بالمعرف) •⊱ لحظر العضو\n"
                    "⚜¦ طرد ( بالرد/بالمعرف) •⊱ لطرد العضو \n"
                    "🔅¦ كتم (بالرد/بالمعرف) •⊱ لكتم العضو \n"
                    "🌀¦ تقييد (بالرد/بالمعرف) •⊱ لتقييد العضو\n"
                    "🚸¦ الغاء الحظر (بالرد/بالمعرف) •⊱ لالغاء الحظر \n"
                    "🔆¦ الغاء الكتم (بالرد/بالمعرف) •⊱ لالغاء الكتم \n"
                    "〰¦ الغاء التقييد (بالرد/بالمعرف) •⊱ لالغاء تقييد العضو \n\n"
                    "🗯┇ راسلني للاستفسار 💡↭ @Luai_shamer"
                ),
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "📡¦ هذا الامر يخص الادمنيه فقط  🚶",
                'reply_to_message_id': message_id,
                'parse_mode': 'MARKDOWN',
                'disable_web_page_preview': True,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    if text in ["م2", "م ٢", "اوامر الاعدادات", "أوامر الاعدادات", "اوامر الإعدادات"]:
        if is_admin_or_creator:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    "👨🏽‍✈️¦  اوامر الوضع للمجموعه ::\n\n"
                    "📮¦ـ➖➖➖➖➖  \n"
                    "💭¦ ضع اسم  ↜ لوضع اسم المحموعة\n  \n"
                    "💭¦ الـرابـط :↜  لعرض الرابط  \n"
                    "📮¦ـ➖➖➖➖➖\n\n"
                    "👨🏽‍💻¦  اوامر رؤية الاعدادات ::\n\n"
                    "🗯¦ الادمنيه : لعرض  الادمنيه \n"
                    "🗯¦ المطور : لعرض معلومات المطور \n"
                    "🗯¦ موقعي :↜لعرض معلوماتك  \n\n"
                    "➖➖➖➖➖➖➖\n"
                    "🗯┇ راسلني للاستفسار 💡↭ @Luai_shamer"
                ),
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "📡¦ هذا الامر يخص الادمنيه فقط  🚶",
                'reply_to_message_id': message_id,
                'parse_mode': 'MARKDOWN',
                'disable_web_page_preview': True,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    if text in ["م3", "م ٣", "اوامر الحماية", "أوامر الحماية", "اوامر الحمايه"]:
        if is_admin_or_creator:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    "⚡️ اوامر حماية المجموعه ⚡️\n"
                    "🗯¦ـ➖➖➖➖\n"
                    "🗯¦️ قفل «» فتح •⊱ البصمات ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ الــفيديو ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ الـصــور ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ الملصقات ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ الروابط ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ التاك ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ البوتات ⊰•\n"
                    "🗯¦ ️قفل «» فتح •⊱ المعرفات ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ التوجيه ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ الجهات ⊰•\n"
                    "🔅¦ـ➖➖➖➖➖\n"
                    "🗯┇ راسلني للاستفسار 💡↭ @Luai_shamer"
                ),
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "📡¦ هذا الامر يخص الادمنيه فقط  🚶",
                'reply_to_message_id': message_id,
                'parse_mode': 'MARKDOWN',
                'disable_web_page_preview': True,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # Sudo menu
    if text == "م المطور":
        if from_id == SUDO_ID:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    "🎖¦ آهہ‏‏لآ عزيزي آلمـطـور 🍃\n"
                    "💰¦ آنتهہ‏‏ آلمـطـور آلآسـآسـي هہ‏‏نآ 🛠\n"
                    "...\n\n"
                    "🚸¦ تسـتطـيع‏‏ آلتحگم بگل آلآوآمـر آلمـمـوجودهہ‏‏\n\n"
                    "🔅¦ تفعيل : لتفعيل البوت \n"
                    "🔅¦ اذاعه : لنشر كلمه لكل المجموعات\n"
                    "🔅¦ استخدم /admin في خاص البوت فقط : لعرض كيبود الخاص بك 💯 \n"
                    "🔅¦ تحديث: لتحديث ملفات البوت\n"
                    "🔅¦ غادر : لمغادرة  البوت \n"
                    "🔅¦ حظر عام : لحظر العضو من البوت عام\n"
                    "🔅¦ـ➖➖➖➖➖\n"
                    "🗯¦ راسلني للاستفسار 💡↭ @Luai_shamer"
                ),
                'parse_mode': 'MarkDown',
                'disable_web_page_preview': True,
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "🔅¦ للمطور الاساسي فقط  🎖",
                'reply_to_message_id': message_id,
                'parse_mode': 'MARKDOWN',
                'disable_web_page_preview': True,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
    
    # Developer info command with photo
    if text in ["المطور", "مطور", "المطور الاساسي", "المطور الأساسي", "dev", "developer"]:
        # Get developer's real info from Telegram
        dev_id = SUDO_ID
        dev_info = bot_request("getChat", {"chat_id": dev_id})
        
        if dev_info and dev_info.get("ok"):
            dev_data = dev_info["result"]
            dev_name = dev_data.get("first_name", "المطور")
            if dev_data.get("last_name"):
                dev_name += " " + dev_data.get("last_name")
            dev_username = dev_data.get("username", "Unknown")
            dev_bio = dev_data.get("bio", "")
        else:
            # Fallback if API fails
            dev_name = "لؤي الشامري"
            dev_username = "Luai_shamer"
            dev_bio = ""
        
        # Beautiful formatted message
        caption_text = (
            "✦──────────────────✦\n"
            "⚡️『 *مـعلـومـات المـطور الأسـاسي* 』⚡️\n"
            "✦──────────────────✦\n\n"
            f"⟡ ⌜𝐍𝐚𝐦𝐞⌟ ↫ *{dev_name}*\n"
            f"⟡ ⌜𝐈𝐃⌟ ↫ `{dev_id}`\n"
            f"⟡ ⌜𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞⌟ ↫ @{dev_username}\n"
            f"⟡ ⌜𝐑𝐚𝐧𝐤⌟ ↫ *𝐌𝐚𝐢𝐧 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫* \n"
        )

        if dev_bio:
            caption_text += f"⟡ ⌜𝐁𝐢𝐨⌟ ↫ _{dev_bio}_\n"

        caption_text += (
            "\n✦──────────────────✦\n"
            f"⟡ ⌜𝐂𝐨𝐧𝐭𝐚𝐜𝐭⌟  ↫ @{dev_username}\n"
            "⟡ ⌜𝐅𝐨𝐫 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 & 𝐈𝐧𝐪𝐮𝐢𝐫𝐢𝐞𝐬⌟ \n"
            "⟡ ⌜𝐂𝐡𝐚𝐧𝐧𝐞𝐥 ⌟ ↫ @boststot\n"
            "✦──────────────────✦"
        )


        
        # Try to get developer's profile photo
        user_profile_photos = bot_request("getUserProfilePhotos", {"user_id": dev_id, "limit": 1, "offset": 0})
        file_id = user_profile_photos["result"]["photos"][0][0]["file_id"] if user_profile_photos and user_profile_photos.get("ok") and user_profile_photos["result"]["photos"] else None
        
        if file_id:
            bot_request("sendPhoto", {
                "chat_id": chat_id,
                "caption": caption_text,
                'parse_mode': "MarkDown",
                "photo": file_id,
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            # If no photo, send as message
            bot_request("sendMessage", {
                "chat_id": chat_id,
                "text": caption_text,
                'parse_mode': "MarkDown",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
    
    # Stats
    if text in ["الاحصائيات", "الإحصائيات", "احصائيات", "إحصائيات", "stats"]:
        members_pv = db.get_all_private_members()
        groups_count = len(db.get_all_groups())
        
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                " الاحصائيات : 📈 \n\n"
                f"📊¦ عدد المجموعات المفعله : {groups_count} \n"
                f"📊¦ عدد المشتركين في البوت : {len(members_pv)}\n"
                "📡 "
            ),
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Groups count
    if text in ["المجموعات", "☑️¦ المجموعات •"]:
        groups_count = len(db.get_all_groups())
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"📮¦ عدد المجموعات المفعلة » {groups_count}  ➼",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Members count
    if text in ["المشتركين", "💯¦ المشتركين •"]:
        members_pv = db.get_all_private_members()
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"عدد المشتركين :- {len(members_pv)}",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Private broadcast (SUDO only)
    if text == "اذاعه خاص" and from_id == SUDO_ID:
        db.set_broadcast_mode(from_id, "bc_private")
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "دز الاذاعة",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    elif message and db.get_broadcast_mode(from_id) == "bc_private" and from_id == SUDO_ID:
        members_pv = db.get_all_private_members()
        for member_id in members_pv:
            if member_id:
                bot_request('sendMessage', {
                    'chat_id': int(member_id),
                    'text': text,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"تم ارسال الرسالة الى {len(members_pv)} مشترك.",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
        db.clear_broadcast_mode(from_id)

    # Group broadcast (SUDO only)
    if text == "اذاعه" and from_id == SUDO_ID:
        db.set_broadcast_mode(from_id, "bc_groups")
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "دز الاذاعة",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    elif message and db.get_broadcast_mode(from_id) == "bc_groups" and from_id == SUDO_ID:
        groups_list = db.get_all_groups()
        for group_id in groups_list:
            if group_id:
                bot_request('sendMessage', {
                    'chat_id': int(group_id),
                    'text': text,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"تم ارسال الرسالة الى {len(groups_list)} مجموعة.",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
        db.clear_broadcast_mode(from_id)

    # Broadcast restriction message
    if text == "اذاعه" and from_id != SUDO_ID:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "📛¦ هذا الامر يخص {المطور} فقط  \n🚶",
            'reply_to_message_id': message_id,
            'parse_mode': 'MARKDOWN',
            'disable_web_page_preview': True,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Update command (SUDO only)
    if text == "تحديث ♻️":
        if from_id == SUDO_ID:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "🎖\n🗂¦ تم تحديث الملفات\n√",
                'parse_mode': 'MarkDown',
                'disable_web_page_preview': True,
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "📛¦ هذا الامر يخص {المطور الاساسي} فقط  \n🚶",
                'reply_to_message_id': message_id,
                'parse_mode': 'MARKDOWN',
                'disable_web_page_preview': True,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # Leave group (SUDO only)
    if text and text.startswith("غادر ") and from_id == SUDO_ID:
        target_chat_id = text.replace("غادر ", "").strip()
        try:
            target_chat_id = int(target_chat_id)
            bot_request('sendMessage', {
                'chat_id': target_chat_id,
                'text': "عذرا لا يمكنني حماية هذا المجموعة",
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
            bot_request('leaveChat', {'chat_id': target_chat_id})
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': f"تم الخروج من المجموعة\n—\nID : {target_chat_id}",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        except ValueError:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "معرف المجموعة غير صالح.",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # "بووتي" (SUDO only)
    if text == 'بووتي' and from_id == SUDO_ID:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': " نعم حبيبي المطور 🌝❤ ",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Admin keyboard in private chat (SUDO only)
    if text == '/admin' and from_id == SUDO_ID and chat_type == "private":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                '🎖¦ آهہ‏‏لآ عزيزي آلمـطـور 🍃\n'
                '💰¦ آنتهہ‏‏ آلمـطـور آلآسـآسـي هہ‏‏نآ 🛠\n'
                '...\n\n'
                '🚸¦ تسـتطـيع‏‏ آلتحگم بگل آلآوآمـر آلمـمـوجودهہ‏‏ بآلگيبورد\n'
                '⚖️¦ فقط آضـغط ع آلآمـر آلذي تريد تنفيذهہ‏‏'
            ),
            'reply_markup': json.dumps({
                'keyboard': [
                    [{'text': '🆔¦ ايديك •'}, {'text': '🚸¦ اسمك •'}],
                    [{'text': '💢¦ معرفك •'}, {'text': '📊¦ الاحصائيات •'}],
                    [{'text': '💯¦ المشتركين •'}, {'text': '☑️¦ المجموعات •'}],
                    [{'text': '🔂¦ اذاعة •'}, {'text': '📤¦ اذاعة خاص •'}],
                    [{'text': '🔄¦ تحديث •'}, {'text': '🚪¦ غادر •'}],
                    [{'text': '🔒¦ حظر عام •'}, {'text': '🔓¦ الغاء حظر عام •'}],
                    [{'text': '📋¦ المحظورين •'}, {'text': '🗑¦ مسح المحظورين •'}],
                    [{'text': '🛠¦ المطور •'}, {'text': '📡¦ قناة المطور •'}],
                    [{'text': '❌¦ اخفاء الكيبورد •'}],
                ],
                'resize_keyboard': True
            })
        })

    # Keyboard responses
    if text == "🆔¦ ايديك •":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f" {from_id} ",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    if text == "🚸¦ اسمك •":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f" {user_name} ",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    if text == "💢¦ معرفك •":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f" @{user_username} ",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    if text == "📊¦ الاحصائيات •":
        members_pv = db.get_all_private_members()
        groups_count = len(db.get_all_groups())
        
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                " الاحصائيات : 📈 \n\n"
                f"📊¦ عدد المجموعات المفعله : {groups_count} \n"
                f"📊¦ عدد المشتركين في البوت : {len(members_pv)}\n"
                "📡 "
            ),
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # Broadcast with keyboard
    if text == "🔂¦ اذاعة •" and from_id == SUDO_ID:
        db.set_broadcast_mode(from_id, "bc_keyboard")
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "📭¦ حسننا الان ارسل الكليشه للاذاعه للمجموعات \n🔛",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    elif message and db.get_broadcast_mode(from_id) == "bc_keyboard" and from_id == SUDO_ID:
        groups_list = db.get_all_groups()
        for group_id in groups_list:
            if group_id:
                bot_request('sendMessage', {
                    'chat_id': int(group_id),
                    'text': text,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
        db.clear_broadcast_mode(from_id)
    
    # اذاعة خاص button
    if text == "📤¦ اذاعة خاص •" and from_id == SUDO_ID:
        db.set_broadcast_mode(from_id, "bc_private")
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "📭¦ حسننا الان ارسل الكليشه للاذاعه للمشتركين في الخاص \n🔛",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    elif message and db.get_broadcast_mode(from_id) == "bc_private" and from_id == SUDO_ID:
        members_list = db.get_all_private_members()
        for member_id in members_list:
            if member_id:
                bot_request('sendMessage', {
                    'chat_id': int(member_id),
                    'text': text,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
        db.clear_broadcast_mode(from_id)
    
    # تحديث button
    if text == "🔄¦ تحديث •" and from_id == SUDO_ID:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "✅¦ تم تحديث البوت بنجاح",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # غادر button
    if text == "🚪¦ غادر •" and from_id == SUDO_ID:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "📝¦ ارسل ID المجموعة للمغادرة منها",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # حظر عام button
    if text == "🔒¦ حظر عام •" and from_id == SUDO_ID:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "📝¦ ارسل ID المستخدم لحظره عام",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # الغاء حظر عام button
    if text == "🔓¦ الغاء حظر عام •" and from_id == SUDO_ID:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "📝¦ ارسل ID المستخدم لالغاء حظره",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # المحظورين button
    if text == "📋¦ المحظورين •" and from_id == SUDO_ID:
        banned_users = db.get_all_banned_users()
        if banned_users:
            banned_list = "\n".join([f"• {uid}" for uid in banned_users])
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': f"📋¦ قائمة المحظورين عام:\n{banned_list}",
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "✅¦ لا يوجد محظورين",
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
    
    # مسح المحظورين button
    if text == "🗑¦ مسح المحظورين •" and from_id == SUDO_ID:
        db.clear_all_banned_users()
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "✅¦ تم مسح جميع المحظورين",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # المطور button
    if text == "🛠¦ المطور •":
        # Get developer's real info from Telegram
        dev_id = SUDO_ID
        dev_info = bot_request("getChat", {"chat_id": dev_id})
        
        if dev_info and dev_info.get("ok"):
            dev_data = dev_info["result"]
            dev_name = dev_data.get("first_name", "المطور")
            if dev_data.get("last_name"):
                dev_name += " " + dev_data.get("last_name")
            dev_username = dev_data.get("username", "Unknown")
            dev_bio = dev_data.get("bio", "")
        else:
            # Fallback if API fails
            dev_name = "لؤي الشامري"
            dev_username = "Luai_shamer"
            dev_bio = ""
        
        # Beautiful formatted message
        caption_text = (
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "⚡ *معلومات المطور الأساسي* ⚡\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👨‍💻 ¦ الاسم : *{dev_name}*\n"
            f"🆔 ¦ الايدي : `{dev_id}`\n"
            f"📮 ¦ المعرف : @{dev_username}\n"
            f"⚡ ¦ الرتبة : *المطور الأساسي* 👑\n"
        )
        
        if dev_bio:
            caption_text += f"📝 ¦ النبذة : _{dev_bio}_\n"
        
        caption_text += (
            "\n━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💬 ¦ للتواصل : @{dev_username}\n"
            "💡 ¦ راسلني للاستفسار والدعم الفني\n"
            "🔗 ¦ القناة : @boststot\n"
            "━━━━━━━━━━━━━━━━━━━━━━━"
        )
        
        user_profile_photos = bot_request("getUserProfilePhotos", {"user_id": dev_id, "limit": 1, "offset": 0})
        file_id = user_profile_photos["result"]["photos"][0][0]["file_id"] if user_profile_photos and user_profile_photos.get("ok") and user_profile_photos["result"]["photos"] else None
        
        if file_id:
            bot_request("sendPhoto", {
                "chat_id": chat_id,
                "caption": caption_text,
                'parse_mode': "MarkDown",
                "photo": file_id,
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request("sendMessage", {
                "chat_id": chat_id,
                "text": caption_text,
                'parse_mode': "MarkDown",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
    
    # قناة المطور button
    if text == "📡¦ قناة المطور •":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "📡¦ قناة المطور: @boststot",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # اخفاء الكيبورد button
    if text == "❌¦ اخفاء الكيبورد •":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "✅¦ تم اخفاء الكيبورد",
            'reply_markup': json.dumps({'remove_keyboard': True})
        })
    
    # المشتركين button
    if text == "💯¦ المشتركين •" and from_id == SUDO_ID:
        members_pv = db.get_all_private_members()
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"💯¦ عدد المشتركين في البوت: {len(members_pv)}",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # المجموعات button
    if text == "☑️¦ المجموعات •" and from_id == SUDO_ID:
        groups_count = len(db.get_all_groups())
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"☑️¦ عدد المجموعات المفعلة: {groups_count}",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })


    # ============ الأوامر الجديدة المضافة ============
    
    # أمر "الاوامر" - القائمة الرئيسية
    if text in ["الاوامر", "الأوامر", "اوامر", "أوامر", "الأوامر", "م", "الاومر"]:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "❂\n\n"
                " ‌‌‏❋¦ مـسـآرت آلآوآمـر آلعآمـهہ‌‏ ⇊\n\n"
                "👨‍⚖️¦ م1 » آوآمـر آلآدآرهہ‌‏\n"
                "📟¦ م2 » آوآمـر آعدآدآت آلمـجمـوعهہ‌‏\n"
                "🛡¦ م3 » آوآمـر آلحمـآيهہ‌‏\n"
                "🕹¦ م المطور »  آوآمـر آلمـطـور\n\n"
                "🗯┇ راسلني للاستفسار 💡↭ @Luai_shamer"
            ),
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # أمر "الالعاب"
    if text in ["الالعاب", "الألعاب", "العاب", "ألعاب", "games"]:
        # Check if group is activated
        if not db.is_group_active(chat_id) and from_id != SUDO_ID:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "⚠️¦ عذراً، البوت غير مفعل في هذه المجموعة\n🔧¦ يرجى تفعيل البوت أولاً",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
            return
        
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "👤¦ اهلا بك عزيزي \n"
                "🚸¦ اليك قائمه الالعاب\n"
                "📬¦ الاسرع » لعبه تطابق السمايلات\n"
                "📛¦ معاني » لعبه معاني السمايلات\n"
                "🎭¦ ترتيب » لعبه ترتيب الكلمات\n"
                "📮¦ نقاطي » لعرض نقاطك"
            ),
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # لعبة "الاسرع"
    if text in ["الاسرع", "الٲسرع", "اسرع", "أسرع", "الأسرع", "اسرع"]:
        import random
        fast_emoji_list = ['😈', '🏦', '🏥', '🐢', '🐀', '🐁', '🐱', '🐩', '😨', '😴', 
                        '🔧', '🏇', '🗼', '🔨', '🎈', '🔛', '⏳', '🚰', '⛎', '💮', 
                        '➿', '🗿', '💙', '🍖', '🍕', '🍟', '🍄', '🌜', '🌛', '🌎', '💧', '⚡']
        selected_emoji = random.choice(fast_emoji_list)
        db.set_config(f"game_fast_{chat_id}", selected_emoji)
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f'اسرع شخص يدز » {{ ️`{selected_emoji}` }} «',
            'parse_mode': 'MARKDOWN',
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # Check fast emoji answer
    fast_answer = db.get_config(f"game_fast_{chat_id}")
    if text and fast_answer and text == fast_answer:
        db.add_points(chat_id, from_id, 1)
        points = db.get_points(chat_id, from_id)
        db.delete_config(f"game_fast_{chat_id}")
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "🎉¦ مبروك لقد ربحت نقطه\n"
                f"🔖¦ اصبح لديك {{ {points} }} نقطه 🍃️\n"
                "➖"
            ),
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # لعبة "معاني"
    if text in ["معاني", "المعاني", "معأني", "معانى", "المعانى"]:
        import random
        emoji_meanings = [
            ('اسرع واحد يدز معنى السمايل يفوز » { 🚀 }', 'صاروخ'),
            ('اسرع واحد يدز معنى السمايل يفوز » { ⚽ }', 'كره'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 🐜 }', 'نمله'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 📙 }', 'كتاب'),
            ('اسرع واحد يدز معنى السمايل يفوز » { ⌚ }', 'ساعه'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 🐧 }', 'بطريق'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 🐍 }', 'ثعبان'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 🐈 }', 'قطه'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 🐒 }', 'قرد'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 💜 }', 'قلب'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 🐄 }', 'بقره'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 🍎 }', 'تفاحه'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 🐔 }', 'دجاجه'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 🐇 }', 'ارنب'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 🐟 }', 'سمكه'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 🐙 }', 'اخطبوط'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 🐝 }', 'نحله'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 🐅 }', 'نمر'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 🐫 }', 'جمل'),
            ('اسرع واحد يدز معنى السمايل يفوز » { 🐘 }', 'فيل'),
        ]
        selected = random.choice(emoji_meanings)
        db.set_config(f"game_meaning_{chat_id}", selected[1])
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': selected[0],
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # Check meaning answer
    meaning_answer = db.get_config(f"game_meaning_{chat_id}")
    emoji_meaning_solutions = ['قمر', 'دجاجه', 'قرد', 'قط', 'ثعبان', 'قطه', 'برج', 'ساعه', 
                        'كتاب', 'نمله', 'نملة', 'كره', 'كرة', 'صاروخ', 'اخطبوط', 
                        'فيل', 'جمل', 'نمر', 'نحله', 'قلب', 'بقره', 'بقرة', 'تفاحه', 
                        'بطريق', 'ارنب', 'سمكه', 'سمكة']
    if text and meaning_answer and text in emoji_meaning_solutions and text == meaning_answer:
        db.add_points(chat_id, from_id, 1)
        points = db.get_points(chat_id, from_id)
        db.delete_config(f"game_meaning_{chat_id}")
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "🎉¦ مبروك لقد ربحت نقطه\n"
                f"🔖¦ اصبح لديك {{ {points} }} نقطه 🍃️\n"
                "➖"
            ),
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # أمر "منع" - منع الكلمات
    if is_admin_or_creator and text and text.startswith("منع "):
        keyword = text.replace("منع ", "").strip()
        db.add_banned_word(chat_id, keyword)
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'parse_mode': "markdown",
            'text': f"تـم 🚷 منـ؏ الـ({keyword}) 💯",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # أمر "الغاء منع"
    if is_admin_or_creator and text and text.startswith("الغاء منع "):
        keyword = text.replace("الغاء منع ", "").strip()
        db.remove_banned_word(chat_id, keyword)
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'parse_mode': "markdown",
            'text': f"تـم 🚷 إلغـاء منـ؏ الـ({keyword}) 💯",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # أمر "قائمة المنع"
    if is_admin_or_creator and text == "قائمة المنع":
        banned_words = db.get_all_banned_words(chat_id)
        filter_list_content = "\n".join(banned_words) if banned_words else "لا توجد كلمات ممنوعة."
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'parse_mode': "markdown",
            'text': f"_قائمة الكلمات الممنوعة ☑️_\n{filter_list_content}\n\n]📡┊Channel Bots](https://t.me/boststot)",
            'disable_web_page_preview': True,
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # أمر "مسح قائمة المنع"
    if is_admin_or_creator and text == "مسح قائمة المنع":
        db.delete_all_banned_words(chat_id)
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "تـم 🚸 حـذف قائمـة المنـ؏ ‼️",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # Check for banned words
    if text and is_enabled and group_status == "member":
        banned_words = db.get_all_banned_words(chat_id)
        if text.strip() in banned_words:
            bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
    
    # الردود التلقائية
    auto_responses = {
        "السلام عليكم": "وعليكم السلام اغاتي🌝👋 ",
        "السلامو عليكم": "وعليكم السلام اغاتي🌝👋 ",
        "سلام عليكم": "وعليكم السلام اغاتي🌝👋 ",
        "سلام الله عليكم": "وعليكم السلام اغاتي🌝👋 ",
        "السلام  عليكم ورحمة الله": "وعليكم السلام اغاتي🌝👋 ",
        "السلام عليكم ورحمه الله": "وعليكم السلام اغاتي🌝👋 ",
        "السلام عليكم ورحمة الله وبركاته": "وعليكم السلام اغاتي🌝👋 ",
        "السلام عليكم ورحمة الله تعالى وبركاته": "وعليكم السلام اغاتي🌝👋 ",
        "سلام عليكم كيفكم": "وعليكم السلام اغاتي🌝👋 ",
        "رابط حذف": "🌿¦ رابط حذف حـساب التيليگرام ↯\n📛¦ لتتندم فڪر قبل ڪلشي  \n👨🏽‍⚖️¦ بالتـوفيـق عزيزي ...\n🚸 ¦ـ  https://telegram.org/deactivate",
        "رابط الحذف": "🌿¦ رابط حذف حـساب التيليگرام ↯\n📛¦ لتتندم فڪر قبل ڪلشي  \n👨🏽‍⚖️¦ بالتـوفيـق عزيزي ...\n🚸 ¦ـ  https://telegram.org/deactivate",
        "اريد احذف الحساب": "🌿¦ رابط حذف حـساب التيليگرام ↯\n📛¦ لتتندم فڪر قبل ڪلشي  \n👨🏽‍⚖️¦ بالتـوفيـق عزيزي ...\n🚸 ¦ـ  https://telegram.org/deactivate",
        "هلو": "هلووات 😊🌹",
        "شكرا": "{ •• الـّ~ـعـفو •• } ",
        "مشكور": "{ •• الـّ~ـعـفو •• } ",
        "مح": "محات حياتي🙈❤",
        "تف": "عيب ابني/بتي اتفل/ي اكبر منها شوية 😌😹",
        "تخليني": "اخليك بزاويه 380 درجه وانته تعرف الباقي 🐸",
        "اكرهك": "ديله شلون اطيق خلقتك اني😾🖖🏿🕷",
        "زاحف": "زاحف عله خالتك الشكره 🌝",
        "واو": "قميل 🌝🌿",
        "شكو ماكو": "غيرك/ج بل كلب ماكو يبعد كلبي😍❤️️",
        "شكو": "كلشي وكلاشي🐸تگـول عبالك احنـة بالشورجـة🌝",
        "معزوفه": "طرطاا طرطاا طرطاا 😂👌",
        "زاحفه": "لو زاحفتلك جان ماكلت زاحفه 🌝🌸",
        "حفلش": "افلش راسك 🤓",
        "ضوجه": "شي اكيد الكبل ماكو 😂 لو بعدك/ج مازاحف/ة 🙊😋",
        "😔": "ليش الحلو ضايج ❤️🍃",
        "😳": "ها بس لا شفت خالتك الشكره 😳😹🕷",
        "😭": "لتبجي حياتي 😭😭",
        "😡": "ابرد  🚒",
        "😍": "يَمـه̷̐ إآلُحــ❤ــب يَمـه̷̐ ❤️😍",
        "😉": "😻🙈",
        "😋": "طبب لسانك جوه عيب 😌",
        "☹️": "لضوج حبيبي 😢❤️🍃",
        "بوت": "أسمي العملاق 🌸",
    }
    
    if text in auto_responses:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': auto_responses[text],
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # رد "العملاق" عشوائي
    if text == "العملاق":
        import random
        random_responses = [
            'سويت هواي شغلات سخيفه بحياتي بس عمري مصحت على واحد وكلتله انجب 😑',
            'نعم حبي 😎',
            'اشتعلو اهل فير شتريد 😠',
            'لك فداك فير حبيبي انت اموووح 💋',
            'بوooooo 👻 ها ها فزيت شفتك شفتك لا تحلف 😂',
            'هياتني اجيت 🌚❤️',
            'راجع المكتب حبيبي عبالك فير سهل تحجي ويا 😒',
            'باقي ويتمدد 😎',
            'لك دبدل ملابسي اطلع برااااا 😵😡 ناس متستحي',
            'دا اشرب جاي تعال غير وكت 😌',
            'هوه غير يسكت عاد ها شتريد 😷',
            'انت مو اجيت البارحه تغلط عليه ✋🏿😒'
        ]
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': random.choice(random_responses),
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # أمر "الكروبات"
    if text in ["الكروبات", "الكروبات", "كروبات", "المجموعات", "groups"]:
        groups_count = len(db.get_all_groups())
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"📮¦ عدد المجموعات المفعلة » *{groups_count}*  ➼",
            'parse_mode': 'MARKDOWN',
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # أمر "جهاتي"
    if text in ["جهاتي", "جهاتى", "جهات", "contacts"]:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "عدد جهاتك المضافة 0",
            'reply_to_message_id': message_id,
            'parse_mode': "html",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # أمر "غنزدبليي"
    if text == "غنزدبليي":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "اللهم عذب المدرسين 😢 منهم الاحياء والاموات 😭🔥 اللهم عذب ام الانكليزي 😭💔 "
                "وكهربها بلتيار الرئيسي 😇 اللهم عذب ام الرياضيات وحولها الى غساله بطانيات 🙊 "
                "اللهم عذب ام الاسلاميه واجعلها بائعة الشاميه 😭🍃 اللهم عذب ام العربي وحولها الى بائعه البلبي "
                "اللهم عذب ام الجغرافيه واجعلها كلدجاجه الحافية اللهم عذب ام التاريخ وزحلقها بقشره من البطيخ "
                "وارسلها الى المريخ اللهم عذب ام الاحياء واجعلها كل مومياء اللهم عذب المعاون اقتله بلمدرسه بهاون 😂😂😂"
            ),
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # ============ نهاية الأوامر الجديدة ============

    # Delete messages by count (SUDO only)
    if text and text.startswith("مسح ") and from_id == SUDO_ID:
        try:
            count_to_delete = int(text.split("مسح ")[1])
            for h in range(message_id, message_id - count_to_delete, -1):
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': h})
        except (ValueError, IndexError):
            pass

    # Edited messages
    edited_message = update.get('edited_message')
    if edited_message:
        bot_request('sendMessage', {
            'chat_id': edited_message.get('chat', {}).get('id'),
            'text': "تم تعديل رسالة.",
            'reply_to_message_id': edited_message.get('message_id'),
            'reply_markup': json.dumps(DEV_BUTTONS)
        })


    else:
        # Check if member tried to use admin commands
        admin_commands_list = ["حظر", "طرد", "كتم", "الغاء الحظر", "الغاء كتم", "تقييد", "الغاء تقييد", "حذف"]
        if reply_to_message and text in admin_commands_list:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "⚠️¦ عذراً، هذا الأمر للأدمنية فقط\n👮‍♂️¦ يجب أن تكون أدمن لاستخدام أوامر الإدارة",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

def main():
    """Main bot loop using long polling"""
    offset = 0
    print("Bot started with database support...")
    print(f"Database file: bot_data.db")
    
    while True:
        try:
            updates = bot_request('getUpdates', {'offset': offset, 'timeout': 30})
            
            if updates and updates.get('ok'):
                for update in updates.get('result', []):
                    offset = update['update_id'] + 1
                    handle_message(update)
            
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nBot stopped by user")
            db.close()
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("Initializing bot...")
    main()
# -------------------------------
# ابقي البوت شغال دائماً على Render
# -------------------------------
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# تشغيل Flask في خيط منفصل
threading.Thread(target=run_flask).start()
