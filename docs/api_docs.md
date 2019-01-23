Junior Design Smartlock
=======================
Auto-generated API documentation for this project

**Version:** 0.1

### Security
---
**Authorization**  

|apiKey|*API Key*|
|---|---|
|Name|Authorization|
|In|header|

### /api/v1/admin/locks
---
##### ***POST***
**Description:** Creates a lock given an admin id token

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| body | body |  | Yes | [PostLocksArgs](#postlocksargs) |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | A AdminLocksResponse object | [AdminLocksResponse](#adminlocksresponse) |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

### /api/v1/locks
---
##### ***GET***
**Description:** Returns a list of locks owned by a user

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | A UserLockResponse object | [UserLockResponse](#userlockresponse) |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

##### ***POST***
**Description:** Adds a valid lock id to a user's account

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| body | body |  | Yes | [PostUserLockArgs](#postuserlockargs) |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | A UserLockResponse object | [UserLockResponse](#userlockresponse) |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

### /api/v1/locks/{lockId}/passwords
---
##### ***GET***
**Description:** Gets metadata about a lock's passwords. Passwords are passed as arguments to change the status or sensitive metadata of a lock. In addition, the user needs to own the lock as well

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lockId | path |  | Yes | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | A LockPasswordsResponse object | [LockPasswordsResponse](#lockpasswordsresponse) |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

##### ***POST***
**Description:** Adds a password to a lock. Passwords are passed as arguments to change the status or sensitive metadata of a lock. In addition, the user needs to own the lock as well

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lockId | path |  | Yes | string |
| body | body |  | Yes | [PostLockPasswordsArgs](#postlockpasswordsargs) |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | A LockPasswordResponse object | [LockPasswordResponse](#lockpasswordresponse) |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

### /api/v1/locks/{lockId}/passwords/{passwordId}
---
##### ***GET***
**Description:** Gets metadata on a lock password. Passwords are passed as arguments to change the status or sensitive metadata of a lock. In addition, the user needs to own the lock as well

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lockId | path |  | Yes | string |
| passwordId | path |  | Yes | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | A LockPasswordResponse object | [LockPasswordResponse](#lockpasswordresponse) |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

##### ***PUT***
**Description:** Changes a password. Passwords are passed as arguments to change the status or sensitive metadata of a lock. In addition, the user needs to own the lock as well

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lockId | path |  | Yes | string |
| passwordId | path |  | Yes | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | A LockPasswordResponse object | [LockPasswordResponse](#lockpasswordresponse) |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

### /api/v1/locks/{lockId}/status
---
##### ***GET***
**Description:** Gets the lock status of a user owned lock

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lockId | path |  | Yes | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | A UserLockStatusResponse object | [UserLockStatusResponse](#userlockstatusresponse) |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

##### ***PUT***
**Description:** Updates a lock status

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lockId | path |  | Yes | string |
| body | body |  | Yes | [PutLockStatusArgs](#putlockstatusargs) |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | A UserLockStatusResponse object | [UserLockStatusResponse](#userlockstatusresponse) |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

### /api/v1/user
---
##### ***GET***
**Description:** Returns user information

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | A UserResponse object | [UserResponse](#userresponse) |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

##### ***POST***
**Description:** Returns user information

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | A UserResponse object | [UserResponse](#userresponse) |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

### Models
---

### AdminLocksResponse  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| createdAt | string |  | Yes |
| id | string |  | Yes |
| nickname | string |  | Yes |
| status | string |  | Yes |

### LockPasswordResponse  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| createdAt | string |  | Yes |
| expires | string |  | No |
| id | string |  | Yes |
| status | string |  | Yes |
| type | string |  | Yes |

### LockPasswordsResponse  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| otp | [ [LockPasswordResponse](#lockpasswordresponse) ] |  | Yes |
| permanent | [ [LockPasswordResponse](#lockpasswordresponse) ] |  | Yes |

### PostLockPasswordsArgs  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| expiration | integer |  | No |
| password | string |  | Yes |
| type | string |  | Yes |

### PostLocksArgs  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| createdAt | integer |  | No |
| nickname | string |  | No |
| status | string |  | No |

### PostUserLockArgs  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| createdAt | integer |  | No |
| nickname | string |  | No |
| status | string |  | No |

### PutLockStatusArgs  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| password | string |  | No |
| status | string |  | Yes |

### UserLockResponse  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| ownedLockIds | [ string ] |  | Yes |

### UserLockStatusResponse  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| status | string |  | Yes |

### UserResponse  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| displayName | string |  | Yes |
| email | string |  | Yes |
| id | string |  | Yes |