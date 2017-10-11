import dropbox
import datetime

time = datetime.datetime.now().time()
client = dropbox.client.DropboxClient('[[CLIENT_ID]]')
print 'linked account: ', client.account_info()

f = open('./foto.jpg', 'rb')
response = client.put_file('/foto-'+str(time)+'.jpg', f)
print 'uploaded: ', response

