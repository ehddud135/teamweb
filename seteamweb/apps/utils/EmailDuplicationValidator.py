class EmailDuplicationValidator():
    def __init__(self, contact_list):
        self.contact_list = contact_list

    def check_email_duplication(self):
        email_list = []
        for i in self.contact_list:
            contact_email = i['Email']
            if ',' in contact_email:
                e_list = contact_email.split(', ')
                for email in e_list:
                    email_list.append(email)
            else:
                email_list.append(contact_email)
        seen = set()
        duplicates = set()

        for email in email_list:
            if email in seen:
                duplicates.add(email)
            seen.add(email)

        if duplicates:
            print("중복된 이메일:", duplicates)
        else:
            print("중복된 이메일이 없습니다.")
