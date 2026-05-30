# MoMo Transactions API — Documentation

**Base URL:** `http://localhost:8080`  
**Authentication:** Basic Auth (username: `admin`, password: `password123`)  
**Content-Type:** `application/json`

---

## Authentication

Every endpoint requires a valid `Authorization` header using HTTP Basic Auth.

**Header format:**
```
Authorization: Basic <base64(username:password)>
```

In Postman, select **Authorization → Basic Auth** and enter the credentials.  
Using curl, pass `-u admin:password123`.

| Scenario | Response |
|---|---|
| Valid credentials | Request proceeds normally |
| Missing or wrong credentials | `401 Unauthorized` |

---

## Endpoints

### 1. List All Transactions

**`GET /transactions`**

Returns all transactions. Supports optional pagination.

**Query Parameters (optional):**

| Parameter | Type | Description |
|---|---|---|
| `limit` | integer | Max number of records to return |
| `offset` | integer | Number of records to skip |

**Request Example:**
```
GET /transactions?limit=5&offset=0
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
```

**Response Example (200 OK):**
```json
{
  "total": 25,
  "limit": 5,
  "offset": 0,
  "transactions": [
    {
      "id": 1,
      "transaction_type": "incoming",
      "amount": 2000.0,
      "sender": "Jane Smith",
      "receiver": null,
      "timestamp": "2024-05-10 16:30:51",
      "balance": 2000.0,
      "fee": null,
      "address": "M-Money"
    }
  ]
}
```

**Error Responses:**

| Code | Meaning |
|---|---|
| `401` | Missing or invalid credentials |

---

### 2. Get a Single Transaction

**`GET /transactions/{id}`**

Returns one transaction by its ID.

**Path Parameter:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | The transaction's unique ID |

**Request Example:**
```
GET /transactions/3
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
```

**Response Example (200 OK):**
```json
{
  "id": 3,
  "transaction_type": "payment",
  "amount": 3500.0,
  "sender": null,
  "receiver": "MTN Shop",
  "timestamp": "2024-05-11 10:05:11",
  "balance": 11500.0,
  "fee": 10.0,
  "address": "M-Money"
}
```

**Error Responses:**

| Code | Meaning |
|---|---|
| `400` | ID is not a valid integer |
| `401` | Missing or invalid credentials |
| `404` | No transaction found with that ID |

---

### 3. Create a Transaction

**`POST /transactions`**

Adds a new transaction. The `id` field is assigned automatically by the server.

**Request Example:**
```
POST /transactions
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
Content-Type: application/json

{
  "transaction_type": "incoming",
  "amount": 5000.0,
  "sender": "Alice Uwase",
  "receiver": null,
  "timestamp": "2024-05-28 09:00:00",
  "balance": 34600.0,
  "fee": null,
  "address": "M-Money"
}
```

**Response Example (201 Created):**
```json
{
  "message": "Transaction created.",
  "transaction": {
    "id": 26,
    "transaction_type": "incoming",
    "amount": 5000.0,
    "sender": "Alice Uwase",
    "receiver": null,
    "timestamp": "2024-05-28 09:00:00",
    "balance": 34600.0,
    "fee": null,
    "address": "M-Money"
  }
}
```

**Error Responses:**

| Code | Meaning |
|---|---|
| `400` | Request body is not valid JSON |
| `401` | Missing or invalid credentials |
| `404` | Wrong URL path |

---

### 4. Update a Transaction

**`PUT /transactions/{id}`**

Updates one or more fields of an existing transaction. Only the fields included in the request body are changed.

**Path Parameter:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | The transaction's unique ID |

**Request Example:**
```
PUT /transactions/3
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
Content-Type: application/json

{
  "amount": 4000.0,
  "fee": 15.0
}
```

**Response Example (200 OK):**
```json
{
  "message": "Transaction updated.",
  "transaction": {
    "id": 3,
    "transaction_type": "payment",
    "amount": 4000.0,
    "sender": null,
    "receiver": "MTN Shop",
    "timestamp": "2024-05-11 10:05:11",
    "balance": 11500.0,
    "fee": 15.0,
    "address": "M-Money"
  }
}
```

**Error Responses:**

| Code | Meaning |
|---|---|
| `400` | ID is not a valid integer, or body is not valid JSON |
| `401` | Missing or invalid credentials |
| `404` | No transaction found with that ID |

---

### 5. Delete a Transaction

**`DELETE /transactions/{id}`**

Permanently removes a transaction.

**Path Parameter:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | The transaction's unique ID |

**Request Example:**
```
DELETE /transactions/3
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
```

**Response Example (200 OK):**
```json
{
  "message": "Transaction 3 deleted."
}
```

**Error Responses:**

| Code | Meaning |
|---|---|
| `400` | ID is not a valid integer |
| `401` | Missing or invalid credentials |
| `404` | No transaction found with that ID |

---

## Error Code Summary

| Code | Meaning |
|---|---|
| `200` | Success |
| `201` | Resource created |
| `400` | Bad request (malformed ID or invalid JSON) |
| `401` | Unauthorized (missing or wrong credentials) |
| `404` | Resource or endpoint not found |

---

## Security Note — Basic Auth Limitations

Basic Auth encodes credentials in base64, which is **not encryption**. Anyone who intercepts the request can decode the header and read the username and password. Key weaknesses:

- Credentials are sent with **every single request**
- base64 is trivially reversible — it provides no real protection
- No token expiry — stolen credentials remain valid indefinitely
- No mechanism to revoke access without changing the password

**Stronger alternatives:**

| Method | Why it's better |
|---|---|
| **JWT (JSON Web Tokens)** | Short-lived signed tokens; credentials are only sent once at login; tokens can be expired or revoked |
| **OAuth 2.0** | Industry standard; supports delegated access; never exposes the user's password to third-party clients |
| **API Keys + HTTPS** | Simple to implement; key can be rotated without changing user passwords; always paired with TLS |

For any production deployment, Basic Auth should be replaced with JWT or OAuth 2.0, and the API must run over **HTTPS** (TLS).
