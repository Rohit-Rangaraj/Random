import zipfile

charlist = "abcdefghijklmnopqrstuvwxyz"
complete = []

print("Running...")

for current in range(4):
    a = [i for i in charlist]
    for x in range(current):
        a = [y + i for i in charlist for y in a]
        complete = complete + a

z = zipfile.ZipFile("secret.zip")

tries = 0

for password in complete:
    try:
        tries += 1
        z.setpassword(password.encode('ascii'))
        z.extract('secret.txt')
        print(f'Password was cracked successfully!! It was : "{password}" It was cracked in {tries} tries.')
        break
    except:
        pass