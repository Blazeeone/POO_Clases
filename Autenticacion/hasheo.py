import bcrypt 

incoming_password = input("Ingrese su contraseña: ").encode("UTF-8")
salt = bcrypt.gensalt(rounds=12)
hashed_password = bcrypt.hashpw(password=incoming_password, salt=salt)
print("Contraña hasheada", hashed_password)
confirm_password = input("Ingrese nuevamente la contraseña: ").encode("UTF-8")
if bcrypt.checkpw(confirm_password, hashed_password):
    print("Contraseña correcta")
else:
    print("Contraseña Incorrecta")
