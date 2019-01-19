localhost
=========
**Version:** 0.1

### /api/v1/admin/locks
---
##### ***POST***
**Description:** Creates a lock given an admin id token

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| passwords | body | A list of passwords to initialize the lock with | No | [ string ] |
| nickname | body | A readable nickname for the lock | No | string |
| status | body | A lock status to initialize the lock to | No | string |
| createdAt | body | The unix milliseconds since epoch in which the lock was registered | No | integer |

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | No response was specified |

### /api/v1/locks/{lock_id}/lockStatus
---
##### ***GET***
**Description:** Gets the lock status of a user owned lock

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lock_id | path | A lock id that the user owns | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | No response was specified |

##### ***PUT***
**Description:** Updates a lock status

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| lock_id | path |  | Yes | string |
| status | body |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | No response was specified |

### /api/v1/user
---
##### ***GET***
**Description:** Returns user information

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | No response was specified |

##### ***POST***
**Description:** Returns user information

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| email | body |  | No | string |
| name | body |  | No | string |

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | No response was specified |

### /api/v1/userLocks
---
##### ***GET***
**Description:** Returns a list of locks owned by a user

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | No response was specified |

##### ***POST***
**Description:** Adds a valid lock id to a user's account

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| ownedLockIds | body |  | No | [ string ] |

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | No response was specified |
