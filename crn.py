import re

company_registration_no_regex = "([1-9]\d{6,7}|\d{6,7}|(SC|NI|AC|FC|GE|GN|GS|IC|IP|LP|NA|NF|NL|NO|NP|NR|NZ|OC|R|RC|SA|SF|SI|SL|SO|SP|SR|SZ|ZC|)\d{6,8})"
crn_england = r"[0-9]{8}"
crn_scotland = "[SC]{2}[0-9]{6}"
crn = r"([a-zA-z]{2}\d{6})|(\d{8})"

s = '''K & M Accountants is trading name of K&M Accountants Limited | Registered in England No. 07643156
Registered Office: 55 Dewsbury Road | Luton | Bedfordshire | LU3 2HH |AML Reg No: 12953412
Website: www.kandmaccountants.co.uk | Email: info@kandmaccountants.co.uk
Facebook: http://www.facebook.com/KMaccountants | Twitter: @KAM Accountants
Telephone: 01582 943371 | Mobile: 07886 456674'''

print(s)
print(re.findall(crn, s))
