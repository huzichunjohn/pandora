curl -X POST http://localhost:5000/api/token/ -d '{"username": "admin", "password": "admin123"}' -H 'Content-Type: application/json'

curl -X GET http://localhost:5000/api/users/ -H 'Authorization: Token ff13313be0b61f5ed520db59af5e3c94c8b98919'

