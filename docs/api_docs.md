localhost
=========
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
| 200 | No response was specified | [AdminLocksResponse](#adminlocksresponse) |
| undefined | Description was not specified |  |

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
| 200 | No response was specified | [UserLockResponse](#userlockresponse) |
| undefined | Description was not specified |  |

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
| 200 | No response was specified | [UserLockResponse](#userlockresponse) |
| undefined | Description was not specified |  |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

### /api/v1/locks/{lock_id}/passwords
---
##### ***GET***
**Description:** Adds a password

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lock_id | path |  | Yes | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | No response was specified | [LockPasswordsResponse](#lockpasswordsresponse) |
| undefined | Description was not specified |  |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

### /api/v1/locks/{lock_id}/passwords/{password_id}
---
##### ***GET***
**Description:** Gets information on a lock password

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lock_id | path |  | Yes | string |
| password_id | path |  | Yes | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | No response was specified | [LockPasswordResponse](#lockpasswordresponse) |
| undefined | Description was not specified |  |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

##### ***PUT***
**Description:** Changes a password

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lock_id | path |  | Yes | string |
| password_id | path |  | Yes | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | No response was specified | [LockPasswordResponse](#lockpasswordresponse) |
| undefined | Description was not specified |  |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

### /api/v1/locks/{lock_id}/status
---
##### ***GET***
**Description:** Gets the lock status of a user owned lock

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lock_id | path | A lock id that the user owns | Yes | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | No response was specified | [UserLockStatusResponse](#userlockstatusresponse) |
| undefined | Description was not specified |  |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

##### ***PUT***
**Description:** Updates a lock status

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lock_id | path |  | Yes | string |
| body | body |  | Yes | [PutLockStatusArgs](#putlockstatusargs) |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | No response was specified | [UserLockStatusResponse](#userlockstatusresponse) |
| undefined | Description was not specified |  |

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
| 200 | No response was specified | [UserResponse](#userresponse) |
| undefined | Description was not specified |  |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

##### ***POST***
**Description:** Returns user information

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | No response was specified | [UserResponse](#userresponse) |
| undefined | Description was not specified |  |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

### Models
---

### AdminLocksResponse  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| createdAt | string |  | No |
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
| otp | [  ] |  | Yes |
| permanent | [  ] |  | Yes |

### PostLocksArgs  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| createdAt | integer |  | No |
| nickname | string |  | No |
| passwords | [ string ] |  | No |
| status | string |  | No |

### PostUserLockArgs  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| createdAt | integer |  | No |
| nickname | string |  | No |
| passwords | [ string ] |  | No |
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