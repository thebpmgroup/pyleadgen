from siteclassifier import SiteClassifier
from pprint import pprint
from collections import Counter

s = SiteClassifier('https://kandmaccountants.co.uk')
s.gohome()
'''
s.findemailaddresses()
s.findcompanyregno()
print("Emails")
print("======")
pprint(s.emails)
print("Sitelinks")
print("=========")
pprint(s.sitelinks)
print("Exludedlinks")
print("############")
pprint(s.excludedlinks)
print("SocialMediaLinks")
print("################")
pprint(s.socialmedialinks)
print("Company Registration Numbers")
print("############################")
print(s.crns)
print("About Page")
print("##########")
#s.readallaboutit()
print(s.about)
'''
s.entityextraction()
print(Counter(s.ent_labels))
pprint([(X.text, X.label_) for X in s.doc.ents])