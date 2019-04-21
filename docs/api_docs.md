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

### /api/v1/hardware/events
---
##### ***POST***
**Description:** Adds a hardware event to the server. The event can be one of ['NONE', 'LOCK_METADATA_CHANGED', 'LOCK_STATE_CHANGED', 'PASSWORD_CREATED', 'PASSWORD_DELETED', 'PASSWORD_METADATA_CHANGED', 'USER_LOCK_ADDED', 'USER_LOCK_DELETED', 'HARDWARE_LOCK_OPENED', 'HARDWARE_LOCK_CLOSED', 'HARDWARE_SUCCEEDED_PASSWORD', 'HARDWARE_FAILED_PASSWORD'].

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| body | body |  | Yes | [PostHardwareEventArgs](#posthardwareeventargs) |

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | No response was specified |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

### /api/v1/hardware/passwords
---
##### ***DELETE***
**Description:** Removes a list of lock password ids

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| body | body |  | Yes | [PostHardwareEventArgs](#posthardwareeventargs) |

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | No response was specified |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

### /api/v1/hardware/status
---
##### ***GET***
**Description:** Gets the lock status

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
| body | body |  | Yes | [PutHardwareLockStatusArgs](#puthardwarelockstatusargs) |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | A UserLockStatusResponse object | [UserLockStatusResponse](#userlockstatusresponse) |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

### /api/v1/hardware/sync
---
##### ***GET***
**Description:** Syncs passwords locally

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | A SyncLockPasswordsResponse object | [SyncLockPasswordsResponse](#synclockpasswordsresponse) |

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

### /api/v1/locks/{lockId}
---
##### ***DELETE***
**Description:** Deletes a lock id associated with a user's account

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lockId | path |  | Yes | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | A UserLockResponse object | [UserLockResponse](#userlockresponse) |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

### /api/v1/locks/{lockId}/history
---
##### ***GET***
**Description:** Resource that lets users retrieve events given a lock id. See `LockEvent` for the schema for each response. Note that status can be one of ['NONE', 'LOCK_METADATA_CHANGED', 'LOCK_STATE_CHANGED', 'PASSWORD_CREATED', 'PASSWORD_DELETED', 'PASSWORD_METADATA_CHANGED', 'USER_LOCK_ADDED', 'USER_LOCK_DELETED', 'HARDWARE_LOCK_OPENED', 'HARDWARE_LOCK_CLOSED', 'HARDWARE_SUCCEEDED_PASSWORD', 'HARDWARE_FAILED_PASSWORD'].

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lockId | path |  | Yes | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | A LockHistoryResponse object | [LockHistoryResponse](#lockhistoryresponse) |

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
##### ***DELETE***
**Description:** Gets metadata on a lock password. Passwords are passed as arguments to change the status or sensitive metadata of a lock. In addition, the user needs to own the lock as well

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lockId | path |  | Yes | string |
| passwordId | path |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | No response was specified |

**Security**

| Security Schema | Scopes |
| --- | --- |
| Authorization | |

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
| body | body |  | Yes | [PutLockPasswordArgs](#putlockpasswordargs) |

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
**Description:** Updates a lock status. If an inputted password is removed (as with OTP passwords), then the JSON payload will contain inputedPasswordDisabled: true

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lockId | path |  | Yes | string |
| body | body |  | Yes | [PutLockStatusArgs](#putlockstatusargs) |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | A PutUserLockStatusResponse object | [PutUserLockStatusResponse](#putuserlockstatusresponse) |

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
| createdAt | integer |  | Yes |
| id | string |  | Yes |
| nickname | string |  | Yes |
| status | string |  | Yes |
| timezone | string |  | No |

### DeleteHardwarePasswordsArgs  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| passwordIds | [ string ] |  | Yes |

### LockEvent  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| createdAt | integer |  | Yes |
| endpoint | string |  | Yes |
| lockId | string |  | Yes |
| status | string |  | Yes |
| userId | string |  | Yes |

### LockHistoryResponse  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| events | [  ] |  | Yes |

### LockPasswordResponse  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| activeDays | [ string ] |  | No |
| activeTimes | [ string ] |  | No |
| createdAt | integer |  | Yes |
| expiration | integer |  | No |
| id | string |  | Yes |
| type | string |  | Yes |

### LockPasswordsResponse  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| otp | [ [LockPasswordResponse](#lockpasswordresponse) ] |  | Yes |
| permanent | [ [LockPasswordResponse](#lockpasswordresponse) ] |  | Yes |

### PostHardwareEventArgs  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| event | string |  | Yes |

### PostLockPasswordsArgs  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| activeDays | [ string ] |  | No |
| activeTimes | [ string ] |  | No |
| expiration | integer |  | No |
| password | string |  | Yes |
| type | string |  | Yes |

### PostLocksArgs  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| nickname | string |  | No |
| secret | string |  | Yes |
| timezone | string |  | No |

### PostUserLockArgs  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| ownedLockIds | [ string ] |  | Yes |

### PutHardwareLockStatusArgs  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| status | string |  | Yes |

### PutLockPasswordArgs  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| activeDays | [ string ] |  | No |
| activeTimes | [ string ] |  | No |
| expiration | integer |  | No |
| password | string |  | No |

### PutLockStatusArgs  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| password | string |  | No |
| status | string |  | Yes |

### PutUserLockStatusResponse  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| providedPasswordDisabled | boolean |  | Yes |
| status | string |  | Yes |

### SyncLockPasswordResponse  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| activeDays | [ string ] |  | No |
| activeTimes | [ string ] |  | No |
| createdAt | integer |  | Yes |
| expiration | integer |  | No |
| hashedPassword | string |  | Yes |
| id | string |  | Yes |
| type | string |  | Yes |

### SyncLockPasswordsResponse  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| otp | [  ] |  | Yes |
| permanent | [  ] |  | Yes |

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