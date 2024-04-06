import re

class RegexProcessor:
    
    def find_amount_paper(self,text):
        pattern=r'Сумма:\s?(\d+)'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return 'Сумма сделки не найдена'
        
    def find_date_paper(self,text):
        pattern=r'от\s?(\d\d\.\d\d\.\d\d\d\d)г'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return 'Дата не найдена'
    
    def find_checking_account_paper(self,text):
        pattern=r'р/с:\s?(\d+)\s?'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return 'Расчетный счет не найден'

    def find_amount_card(self,text):
        pattern=r'(\d+)р'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return 'Сумма сделки не найдена'
        
    def find_checking_account_card(self,text):
        pattern=r'(MIR-\d+)'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return 'Сумма сделки не найдена'

    def find_lead_ids(self, text):
        pattern = r'\b(\d+)\b'
        matches = re.findall(pattern, text)
        if matches:
            return matches
        else:
            return ['Лид ID не найдены']

