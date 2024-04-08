import re
from datetime import datetime

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
        pattern = r'(\d+)(?:[,;/](\d+))?' # Making the second group optional
        matches = re.findall(pattern, text)
        if matches:
            return [match for groups in matches for match in groups if match]
        else:
            return ['Лид ID не найдены']
        
    def process_paper_text(self, text):
        result = {}
        result['amount'] = self.find_amount_paper(text)
        result['date'] = self.find_date_paper(text)
        result['checking_account'] = self.find_checking_account_paper(text)
        
        if result['amount']:
            return result
        else:
            return False

    def process_card_text(self, text):
        result = {}
        result['amount'] = self.find_amount_card(text)
        result['date'] = datetime.today().strftime('%d.%m.%Y')
        result['checking_account'] = self.find_checking_account_card(text)
        
        if result['amount']:
            return result
        else:
            return False
        
    def handle_text(self, text):
        
        pattern=r'MIR'
        card = re.search(pattern, text)

        if card:
            paper_result = self.process_card_text(text)
            return paper_result
        else:
            paper_result = self.process_paper_text(text)
            return paper_result
            
