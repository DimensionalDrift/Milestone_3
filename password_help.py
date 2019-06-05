from werkzeug.security import generate_password_hash, check_password_hash

password = "test"
password_hash = "pbkdf2:sha256:150000$I2rXpqmy$07af882f2cfb037f20b4e1851cefe23b3002d688d2b10e8de96e1c037eb3469e"

print(generate_password_hash(password))
print(check_password_hash(password_hash, password))
