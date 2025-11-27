APIKEY="cisco|gM6O9XicReXxOau-2liH_CQPbcjP_RAgUlsTsmkTIlc"
curl -X PUT "http://library.demo.local/api/v1/books/1" \
-H "accept: application/json" \
-H "X-API-KEY: cisco|gM6O9XicReXxOau-2liH_CQPbcjP_RAgUlsTsmkTIlc" \
-H "Content-Type: application/json" \
-d "{ \"id\": 1, \"title\": \"python for dummies test\", \"author\": \"Stef Maruch Aahnz Maruch (Test)\"}"