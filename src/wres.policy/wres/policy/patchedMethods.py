# coding=utf-8
#Arquivo usado para definição de funções custom chamadas pelo collective.monkeypatcher

#Solgema
def patchedGetCustomTitleFormat(self):
    if self.portal_language in ['fr']:
        return '{month: "MMMM yyyy", week: "d[ MMM][ yyyy]{ \'-\' d MMM yyyy}", day: \'dddd, d MMMM yyyy\'}'
    elif self.portal_language in ['de']:
        return '{month: \'MMMM yyyy\', week: "d[ yyyy].[ MMMM]{ \'- \'d. MMMM yyyy}", day: \'dddd, d. MMMM yyyy\'}'
    elif self.portal_language in ['pt']:
        return '{month: \'MMMM yyyy\', week: "d \'de\' MMMM{ \'- \'d \'de\' MMMM yyyy}", day: "dddd, d \'de\' MMMM yyyy"}'
    else:
        return '{month: \'MMMM yyyy\', week: "MMM d[ yyyy]{ \'-\'[ MMM] d yyyy}", day: \'dddd, MMM d, yyyy\'}'
        
def patchedColumnFormat(self):
    if self.portal_language in ['de']:
        return "{month: 'ddd', week: 'ddd d. MMM', day: 'dddd d. MMM'}"
    elif self.portal_language in ['pt']:
        return "{month: 'ddd', week: 'ddd dd/MM', day: 'ddd dd/MM'}"
    else: 
        return "{month: 'ddd', week: 'ddd M/d', day: 'dddd M/d'}"
        
def patchedGetHourFormat(self):
    if self.portal_language in ['fr', 'de', 'it', 'pt']:
        return 'HH:mm'
    else:
        return 'h(:mm)tt'