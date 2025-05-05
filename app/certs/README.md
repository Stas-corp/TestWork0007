# RSA key pairing gyneration

openssl genrsa -out jwt_privet.pem 2048

openssl rsa -in jwt_privet.pem -pubout -out jwt_public.pem
