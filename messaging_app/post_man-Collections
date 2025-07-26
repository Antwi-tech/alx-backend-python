{
  "info": {
    "name": "Messaging App API Tests",
    "_postman_id": "abc1234-defg-5678-hijk-lmnopqrstuv",
    "description": "Test login, messaging, and filtering in the messaging app",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Login - Get JWT Token",
      "request": {
        "method": "POST",
        "header": [
          { "key": "Content-Type", "value": "application/json" }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"username\": \"alice\",\n  \"password\": \"yourpassword\"\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/token/",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "token", ""]
        }
      }
    },
    {
      "name": "Send Message",
      "request": {
        "method": "POST",
        "header": [
          { "key": "Content-Type", "value": "application/json" },
          { "key": "Authorization", "value": "Bearer {{access_token}}" }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"recipient\": \"bob\",\n  \"content\": \"Hello Bob!\"\n}"
        },
        "url": {
          "raw": "http://localhost:8000/messages/",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["messages", ""]
        }
      }
    },
    {
      "name": "Fetch Messages with Filters",
      "request": {
        "method": "GET",
        "header": [
          { "key": "Authorization", "value": "Bearer {{access_token}}" }
        ],
        "url": {
          "raw": "http://localhost:8000/messages/?user=bob&page=1",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["messages", ""],
          "query": [
            { "key": "user", "value": "bob" },
            { "key": "page", "value": "1" }
          ]
        }
      }
    },
    {
      "name": "Fetch Messages Without Token (Unauthorized)",
      "request": {
        "method": "GET",
        "url": {
          "raw": "http://localhost:8000/messages/",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["messages", ""]
        }
      }
    }
  ],
  "event": [
    {
      "listen": "prerequest",
      "script": { "exec": [], "type": "text/javascript" }
    },
    {
      "listen": "test",
      "script": { "exec": [], "type": "text/javascript" }
    }
  ],
  "variable": [
    {
      "key": "access_token",
      "value": ""
    }
  ]
}
