"""Валидаторы для проверки входящих данных"""

def is_reminder_command(text: str) -> bool:
    """
    Проверяет, является ли сообщение командой на создание напоминания.
    Возвращает True, если сообщение похоже на запрос напоминания.
    """
    if not text or not isinstance(text, str):
        return False
    
    text = text.lower().strip()
    
    # Ключевые слова, с которых может начинаться напоминание
    reminder_keywords = [
        'напомни', 'напомнить', 'напоминание',
        'через', 'в ', 'завтра', 'послезавтра'
    ]
    
    for keyword in reminder_keywords:
        if text.startswith(keyword) or f' {keyword}' in text:
            return True
    
    # Если сообщение содержит время в формате ЧЧ:ММ
    import re
    if re.search(r'\d{1,2}[:.]\d{2}', text):
        return True
    
    return False